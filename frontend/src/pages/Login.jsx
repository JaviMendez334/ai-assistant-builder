import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Bot } from "lucide-react";
import { loginUser } from "../services/api";


export default function Login(){


const [email,setEmail] = useState("");
const [password,setPassword] = useState("");

const [error,setError] = useState("");
const [loading,setLoading] = useState(false);

const navigate = useNavigate();




async function handleSubmit(e){

e.preventDefault();


try{


setLoading(true);
setError("");



const response = await loginUser({

username: email,
password: password

});



localStorage.setItem(
"token",
response.access_token
);



navigate("/");



}catch(err){


setError(err.message);



}finally{


setLoading(false);


}


}




return (


<div className="
min-h-screen
flex
items-center
justify-center
bg-slate-950
px-6
">


<div className="
w-full
max-w-md
bg-slate-900
border
border-slate-800
rounded-3xl
p-8
shadow-2xl
">



<div className="
flex
flex-col
items-center
mb-8
">


<div className="
bg-blue-600/20
text-blue-400
p-4
rounded-2xl
mb-4
">

<Bot size={38}/>

</div>



<h1 className="
text-3xl
font-bold
text-white
">

AI Assistant Builder

</h1>



<p className="
text-slate-400
mt-2
text-center
">

Crea asistentes IA para empresas

</p>



</div>





<form
onSubmit={handleSubmit}
className="
space-y-5
"
>



<div>


<label className="
text-sm
text-slate-300
">

Correo electrónico

</label>



<input

type="email"

value={email}

onChange={(e)=>setEmail(e.target.value)}

placeholder="correo@empresa.com"

className="
w-full
mt-2
bg-slate-950
border
border-slate-700
rounded-xl
px-4
py-3
text-white
outline-none
focus:border-blue-500
"

required

/>


</div>





<div>


<label className="
text-sm
text-slate-300
">

Contraseña

</label>



<input

type="password"

value={password}

onChange={(e)=>setPassword(e.target.value)}

placeholder="********"

className="
w-full
mt-2
bg-slate-950
border
border-slate-700
rounded-xl
px-4
py-3
text-white
outline-none
focus:border-blue-500
"

required

/>


</div>





<button

type="submit"

disabled={loading}

className="
w-full
bg-blue-600
hover:bg-blue-700
disabled:opacity-50
text-white
font-semibold
py-3
rounded-xl
transition
"

>


{loading ? "Ingresando..." : "Ingresar"}


</button>



</form>




{error && (

<p className="
text-red-400
text-center
mt-4
text-sm
">

{error}

</p>

)}






<div className="
text-center
mt-6
text-slate-400
text-sm
">


¿No tienes una cuenta?


<Link

to="/register"

className="
text-blue-400
hover:text-blue-300
ml-2
"

>

Crear cuenta

</Link>



</div>




</div>


</div>


)

}
