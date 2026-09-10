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
