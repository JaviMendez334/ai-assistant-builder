import os
from pathlib import Path
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from backend.tools.base import BaseTool
from backend.tools.registry import registry

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = str(BASE_DIR / "config" / "google_credentials.json")


def _obtener_worksheet(client: gspread.Client, tenant_id: int | None = None):
    """Resuelve la hoja según el tenant_id o usa la predeterminada."""
    base_sheet_name = os.getenv("GOOGLE_SHEET_NAME", "Control de Ventas y Abonos")
    
    # Si viene un tenant_id, busca primero si existe una hoja dedicada (ej: "Control de Ventas y Abonos_1")
    if tenant_id:
        tenant_specific_name = f"{base_sheet_name}_{tenant_id}"
        try:
            return client.open(tenant_specific_name).sheet1
        except Exception:
            pass  # Si no existe archivo independiente, abre el principal

    spreadsheet = client.open(base_sheet_name)
    
    # Si existe una pestaña nombrada con el tenant (ej: "Tenant_1") la usa, si no, usa la primera
    if tenant_id:
        try:
            return spreadsheet.worksheet(f"Tenant_{tenant_id}")
        except Exception:
            pass

    return spreadsheet.sheet1


class RecordTransactionTool(BaseTool):
    """
    Registra compras nuevas o actualiza abonos y saldos de clientes existentes en Google Sheets.
    """

    @property
    def name(self) -> str:
        return "record_transaction"

    @property
    def description(self) -> str:
        return (
            "Registra una compra o abono en la hoja contable. "
            "Si el cliente ya existe, actualiza su fila sumando el abono y recalculando su deuda. "
            "Si es nuevo, crea una nueva fila con su compra total y abono inicial."
        )

    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_name": {
                            "type": "string",
                            "description": "Nombre del cliente."
                        },
                        "concept": {
                            "type": "string",
                            "description": "Producto comprado o motivo del abono (ej. 'Perfume Invictus', 'Abono a saldo')."
                        },
                        "total_amount": {
                            "type": "number",
                            "description": "Valor total de la compra si es un cliente nuevo. Si es un abono a deuda existente, enviar 0 o el valor previo."
                        },
                        "paid_amount": {
                            "type": "number",
                            "description": "Monto que el cliente está abonando o pagando en esta operación."
                        },
                        "payment_type": {
                            "type": "string",
                            "enum": ["Abono", "Pago Total", "Anticipo", "Liquidación"],
                            "description": "Tipo de operación."
                        },
                        "notes": {
                            "type": "string",
                            "description": "Detalles adicionales, método de pago u observaciones."
                        }
                    },
                    "required": ["customer_name", "concept", "paid_amount", "payment_type"]
                }
            }
        }

    def execute(
        self,
        customer_name: str,
        concept: str,
        paid_amount: float,
        total_amount: float = 0.0,
        payment_type: str = "Abono",
        notes: str = "Sin observaciones",
        tenant_id: int | None = None,
        **kwargs
    ) -> dict:
        try:
            if not os.path.exists(CREDENTIALS_PATH):
                return {"success": False, "error": "No se encontraron credenciales de Google."}

            creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
            client = gspread.authorize(creds)
            worksheet = _obtener_worksheet(client, tenant_id)

            all_values = worksheet.get_all_values()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            fila_cliente = None
            for idx, row in enumerate(all_values[1:], start=2):
                if len(row) > 1 and row[1].strip().lower() == customer_name.strip().lower():
                    fila_cliente = (idx, row)
                    break

            if fila_cliente:
                row_idx, row_data = fila_cliente
                
                try:
                    abono_anterior = float(str(row_data[3]).replace(",", "").replace("$", "").strip() or 0)
                except (IndexError, ValueError):
                    abono_anterior = 0.0

                try:
                    compra_total = float(str(row_data[6]).replace(",", "").replace("$", "").strip() or 0)
                except (IndexError, ValueError):
                    compra_total = float(total_amount) if total_amount > 0 else 0.0

                nuevo_abono_acumulado = abono_anterior + float(paid_amount)
                nueva_deuda = max(0.0, compra_total - nuevo_abono_acumulado)

                worksheet.update_cell(row_idx, 1, now)
                worksheet.update_cell(row_idx, 4, nuevo_abono_acumulado)
                worksheet.update_cell(row_idx, 5, payment_type)
                worksheet.update_cell(row_idx, 6, notes)
                worksheet.update_cell(row_idx, 8, nueva_deuda)

                return {
                    "success": True,
                    "message": (
                        f"Fila de {customer_name} actualizada: Se sumó un abono de ${paid_amount:,.0f}. "
                        f"Total abonado acumulado: ${nuevo_abono_acumulado:,.0f}. "
                        f"Deuda pendiente restante: ${nueva_deuda:,.0f}."
                    )
                }

            else:
                compra = float(total_amount) if total_amount > 0 else float(paid_amount)
                deuda = max(0.0, compra - float(paid_amount))

                worksheet.append_row([
                    now,
                    customer_name,
                    concept,
                    paid_amount,
                    payment_type,
                    notes,
                    compra,
                    deuda
                ])

                return {
                    "success": True,
                    "message": (
                        f"Nuevo cliente registrado: {customer_name}. Compra Total: ${compra:,.0f}, "
                        f"Abono inicial: ${paid_amount:,.0f}, Deuda inicial: ${deuda:,.0f}."
                    )
                }

        except Exception as e:
            return {"success": False, "error": f"Error al interactuar con Google Sheets: {str(e)}"}


class GetCustomerBalanceTool(BaseTool):
    """
    Herramienta para consultar el historial financiero y saldo de un cliente.
    """

    @property
    def name(self) -> str:
        return "get_customer_balance"

    @property
    def description(self) -> str:
        return (
            "Consulta cuánto debe un cliente, sus compras realizadas, saldo pendiente y fechas de abonos. "
            "ÚSALA SIEMPRE que pregunten por deudas, saldos, historial de pagos o compras de una persona."
        )

    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_name": {
                            "type": "string",
                            "description": "Nombre del cliente a consultar."
                        }
                    },
                    "required": ["customer_name"]
                }
            }
        }

    def execute(self, customer_name: str, tenant_id: int | None = None, **kwargs) -> dict:
        try:
            if not os.path.exists(CREDENTIALS_PATH):
                return {"success": False, "error": "No se encontraron credenciales de Google."}

            creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
            client = gspread.authorize(creds)
            worksheet = _obtener_worksheet(client, tenant_id)

            records = worksheet.get_all_records()
            if not records:
                return {"success": True, "message": "No hay transacciones registradas todavía en la hoja."}

            customer_records = [
                r for r in records
                if customer_name.strip().lower() in str(r.get("Cliente", "")).lower()
            ]

            if not customer_records:
                return {
                    "success": True,
                    "message": f"No se encontraron transacciones previas para el cliente '{customer_name}'."
                }

            return {
                "success": True,
                "customer": customer_name,
                "history": customer_records
            }

        except Exception as e:
            return {"success": False, "error": f"Error al consultar Google Sheets: {str(e)}"}


registry.register(RecordTransactionTool())
registry.register(GetCustomerBalanceTool())
