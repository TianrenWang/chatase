import React, { useContext } from "react";
import axios from "axios";
import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import Button from "react-bootstrap/Button";
import { AuthContext } from "../contexts/AuthContext";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.withCredentials = true;

const client = axios.create();

export default function Playground() {
  const { setUser } = useContext(AuthContext);
  function submitLogout(e: React.FormEvent) {
    e.preventDefault();
    client.post("/api/logout", { withCredentials: true }).then(() => {
      setUser(undefined);
    });
  }
  return (
    <div>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand>Authentication App</Navbar.Brand>
          <Navbar.Toggle />
          <Navbar.Collapse className="justify-content-end">
            <Navbar.Text>
              <form onSubmit={(e) => submitLogout(e)}>
                <Button type="submit" variant="light">
                  Log out
                </Button>
              </form>
            </Navbar.Text>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <div className="center">
        <h2>You're logged in!</h2>
      </div>
    </div>
  );
}
