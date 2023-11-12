import { AuthProvider } from "./contexts/AuthContext";
import Root from "./navigation/Root";

export default function App() {
  return (
    <AuthProvider>
      <Root />
    </AuthProvider>
  );
}
