// Auth.tsx
import React, { useState, FormEvent } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import UserService from "./Services/userService";

const Auth: React.FC = () => {
  // mode can be "login" or "signup"
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>("");

  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from: { pathname: string } } | undefined)
    ?.from?.pathname;

  // Check if 'from' is the login page; if so, redirect to dashboard
  const redirectTo = from && from !== "/login" ? from : "/dashboard";

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    // Use the appropriate endpoint based on mode
    const endpoint =
      mode === "login"
        ? "http://localhost:5000/login"
        : "http://localhost:5000/signup";

    try {
      const response = await UserService.login(username, password);
      // Assuming the signup endpoint returns a token as well.
      localStorage.setItem("token", response.data.access_token);
      navigate(redirectTo, { replace: true });
    } catch (err) {
      console.error(`${mode} error:`, err);
      setError("Invalid credentials or sign-up failed. Please try again.");
    }
  };

  return (
    <div className="auth-container">
      <h2>{mode === "login" ? "Login" : "Sign Up"}</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">{mode === "login" ? "Login" : "Sign Up"}</button>
      </form>
      <div style={{ marginTop: "1rem" }}>
        {mode === "login" ? (
          <p>
            Don't have an account?{" "}
            <button onClick={() => setMode("signup")}>Sign Up</button>
          </p>
        ) : (
          <p>
            Already have an account?{" "}
            <button onClick={() => setMode("login")}>Login</button>
          </p>
        )}
      </div>
    </div>
  );
};

export default Auth;
