import { useContext } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { AuthContext } from "../contexts/AuthContext";
import Playground from "./Playground";
import Authentication from "./Authentication";

const loggedInRouter = createBrowserRouter([
  {
    path: "/",
    element: <Playground />,
  },
]);

const loggedOutRouter = createBrowserRouter([
  {
    path: "/",
    element: <Authentication />,
  },
]);

export default function Root() {
  const { user } = useContext(AuthContext);
  if (user) return <RouterProvider router={loggedInRouter} />;
  else return <RouterProvider router={loggedOutRouter} />;
}
