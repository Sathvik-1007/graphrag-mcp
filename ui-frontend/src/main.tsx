import { createRoot } from "react-dom/client";
import "./styles/globals.css";
import App from "./App";

// No StrictMode — prevents double-mount issues with canvas animation loop
createRoot(document.getElementById("root")!).render(<App />);
