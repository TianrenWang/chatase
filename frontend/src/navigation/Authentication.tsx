import "../css/form.css";
import React, { useContext, useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import httpclient from "../helpers/httpRequestClient";
import { AuthContext } from "../contexts/AuthContext";

export default function Authentication() {
  const { setUser } = useContext(AuthContext);
  const [registrationToggle, setRegistrationToggle] = useState(false);
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  function update_form_btn() {
    const formButton = document.getElementById("form_btn");
    if (registrationToggle && formButton) {
      formButton.innerHTML = "Register";
      setRegistrationToggle(false);
    } else if (formButton) {
      formButton.innerHTML = "Log in";
      setRegistrationToggle(true);
    }
  }

  function submitRegistration(e: React.FormEvent) {
    e.preventDefault();
    httpclient
      .post("/api/register", {
        email: email,
        username: username,
        password: password,
      })
      .then((res) => {
        httpclient
          .post("/api/login", {
            email: email,
            password: password,
          })
          .then((res) => {
            setUser(res.data.user);
          });
      });
  }

  function submitLogin(e: React.FormEvent) {
    e.preventDefault();
    httpclient
      .post("/api/login", {
        email: email,
        password: password,
      })
      .then(function (res) {
        setUser(res.data);
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
              <Button id="form_btn" onClick={update_form_btn} variant="light">
                Register
              </Button>
            </Navbar.Text>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      {registrationToggle ? (
        <div className="center">
          <Form onSubmit={(e) => submitRegistration(e)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <Form.Text className="text-muted">
                We'll never share your email with anyone else.
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicUsername">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </div>
      ) : (
        <div className="center">
          <Form onSubmit={(e) => submitLogin(e)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <Form.Text className="text-muted">
                We'll never share your email with anyone else.
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </div>
      )}
    </div>
  );
}
