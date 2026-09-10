import {
  User,
  Building2,
  Shield,
  Bell
} from "lucide-react";


export default function Settings(){


return (

<div>


<div className="mb-10">

<h1 className="
text-3xl
font-bold
text-white
">

Configuración

</h1>


<p className="
text-slate-400
mt-3
">

Administra tu cuenta y preferencias del sistema.

</p>


</div>




<div className="
grid
grid-cols-1
lg:grid-cols-2
gap-6
">





<Card
icon={<User/>}
title="Perfil"
text="Actualiza tu información personal."
/>



<Card
icon={<Building2/>}
title="Empresa"
text="Configura los datos de tu organización."
/>



<Card
icon={<Shield/>}
title="Seguridad"
text="Gestiona contraseñas y accesos."
/>



<Card
icon={<Bell/>}
title="Notificaciones"
text="Controla alertas y avisos."
/>



</div>


</div>

)

}




function Card({icon,title,text}){


return (

<div className="
bg-slate-900
border
border-slate-800
rounded-2xl
p-6
hover:border-blue-500
transition
">


<div className="
bg-blue-600/20
text-blue-400
p-3
rounded-xl
w-fit
">

{icon}

</div>



<h2 className="
text-xl
font-semibold
text-white
mt-5
">

{title}

</h2>



<p className="
text-slate-400
mt-2
">

{text}

</p>



<button

className="
mt-5
text-blue-400
hover:text-blue-300
"

>

Configurar →

</button>


</div>

)

}
