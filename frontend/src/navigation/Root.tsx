import { useContext } from "react";
import {
  createBrowserRouter,
  Navigate,
  RouterProvider,
} from "react-router-dom";

import { AuthContext } from "../contexts/AuthContext";
import Dashboard from "./Dashboard/Dashboard";
import Authentication from "./Authentication/Authentication";
import TabWithHeader from "./Dashboard/TabWithHeader";
import AccountForm from "./Dashboard/AccountForm";
import APIKeysManager from "./Dashboard/APIKeysManager";

const loggedInRouter = createBrowserRouter([
  {
    path: "/",
    element: <Dashboard />,
    children: [
      {
        path: "/",
        element: (
          <TabWithHeader tabTitle="Account" tabDescription="">
            <AccountForm />
          </TabWithHeader>
        ),
      },
      {
        path: "api",
        element: (
          <TabWithHeader tabTitle="API" tabDescription="">
            <APIKeysManager />
          </TabWithHeader>
        ),
      },
      {
        path: "admin",
        element: null,
      },
      {
        path: "*",
        element: <Navigate to="/" />,
      },
    ],
  },
]);

const loggedOutRouter = createBrowserRouter([
  {
    path: "/",
    element: <Authentication />,
  },
  {
    path: "admin",
    element: null,
  },
  {
    path: "*",
    element: <Navigate to="/" />,
  },
]);

export default function Root() {
  const { user } = useContext(AuthContext);
  if (user) return <RouterProvider router={loggedInRouter} />;
  else return <RouterProvider router={loggedOutRouter} />;
}
