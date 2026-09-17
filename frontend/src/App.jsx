import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import DashboardLayout from "./layouts/DashboardLayout";
import ProtectedRoute from "./components/ProtectedRoute";

import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Assistants from "./pages/Assistants";
import AssistantDetail from "./pages/AssistantDetail";
import Importer from "./pages/Importer"; // <-- 1. Importa la nueva página

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/assistants"
            element={<Assistants />}
          />

          <Route
            path="/assistants/:assistantId"
            element={<AssistantDetail />}
          />

          {/* <-- 2. Añade la ruta del importador dentro del layout protegido */}
          <Route
            path="/importer"
            element={<Importer />}
          />
        </Route>

        <Route
          path="*"
          element={<Navigate to="/" />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
