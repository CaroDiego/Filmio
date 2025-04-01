import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { FileProviderWrapper } from "./context/file.contenxt.jsx";
import { ComunicationProviderWrapper } from "./context/comunication.context.jsx";

createRoot(document.getElementById("root")).render(
  // <StrictMode>
  <FileProviderWrapper>
    <ComunicationProviderWrapper>
      <App />
    </ComunicationProviderWrapper>
  </FileProviderWrapper>
  // </StrictMode>
);
