import {
  Send,
  Bot,
  User,
  Plus,
  MessageSquare
} from "lucide-react";

import { useState } from "react";


export default function Conversations(){


const [message,setMessage] = useState("");



const conversations = [
  {
    title:"Consulta ventas",
    date:"Hoy"
  },
  {
    title:"Soporte clientes",
    date:"Ayer"
  }
];



const messages = [

{
role:"assistant",
text:"Hola Javier 👋 Soy tu asistente IA empresarial. ¿En qué puedo ayudarte?"
},

{
role:"user",
text:"Necesito información sobre mis productos."
},

{
role:"assistant",
text:"Claro, puedo ayudarte usando los documentos cargados."
}

];




return (

<div className="
flex
h-[calc(100vh-120px)]
bg-slate-950
rounded-2xl
overflow-hidden
border
border-slate-800
">



{/* SIDEBAR CHAT */}


<div className="
w-72
bg-slate-900
border-r
border-slate-800
p-5
">


<button

className="
w-full
bg-blue-600
hover:bg-blue-700
text-white
rounded-xl
py-3
flex
items-center
justify-center
gap-2
"

>

<Plus size={18}/>

Nueva conversación

</button>



<div className="
mt-6
space-y-3
">


{
conversations.map((item,index)=>(


<div

key={index}

className="
p-4
rounded-xl
bg-slate-800
cursor-pointer
hover:bg-slate-700
"

>


<div className="
flex
items-center
gap-2
text-white
">

<MessageSquare size={18}/>

{item.title}

</div>


<p className="
text-xs
text-slate-400
mt-2
">

{item.date}

</p>


</div>


))

}



</div>


</div>





{/* CHAT */}


<div className="
flex-1
flex
flex-col
">


{/* HEADER */}


<div className="
p-5
border-b
border-slate-800
flex
items-center
gap-3
">


<div className="
bg-blue-600/20
p-3
rounded-xl
text-blue-400
">

<Bot/>

</div>


<div>

<h2 className="
text-white
font-bold
">

Asistente IA

</h2>


<p className="
text-sm
text-slate-400
">

Ventas empresarial

</p>


</div>


</div>





{/* MENSAJES */}


<div className="
flex-1
p-6
space-y-5
overflow-y-auto
">


{
messages.map((msg,index)=>(


<div

key={index}

className={`

flex

${msg.role==="user"
?
"justify-end"
:
"justify-start"
}

`}

>


<div

className={`

max-w-xl
px-5
py-4
rounded-2xl
flex
gap-3

${msg.role==="user"

?

"bg-blue-600 text-white"

:

"bg-slate-800 text-slate-200"

}

`}

>


{
msg.role==="user"

?

<User size={20}/>

:

<Bot size={20}/>

}



<p>

{msg.text}

</p>



</div>


</div>


))

}


</div>






{/* INPUT */}


<div className="
p-5
border-t
border-slate-800
flex
gap-3
">


<input

value={message}

onChange={(e)=>setMessage(e.target.value)}

placeholder="Escribe un mensaje..."

className="
flex-1
bg-slate-900
border
border-slate-700
rounded-xl
px-5
text-white
outline-none
"


/>



<button

className="
bg-blue-600
hover:bg-blue-700
text-white
px-5
rounded-xl
"

>


<Send size={20}/>


</button>



</div>



</div>


</div>

)

}
