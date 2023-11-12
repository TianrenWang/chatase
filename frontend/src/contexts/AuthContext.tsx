import { ReactElement, createContext, useEffect, useState } from "react";
import httpclient from "../helpers/httpRequestClient";

interface User {
  username: string;
  id: string;
}

export const AuthContext = createContext({
  user: undefined,
  setUser: () => {},
} as {
  user: User | undefined;
  setUser: React.Dispatch<React.SetStateAction<User | undefined>>;
});

export const AuthProvider = ({ children }: { children: ReactElement }) => {
  const [user, setUser] = useState<User>();

  useEffect(() => {
    httpclient
      .get("/api/user")
      .then((res) => {
        setUser(res.data.user);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};
