import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { FileProviderWrapper } from "./context/file.contenxt.jsx";
import { ComunicationProviderWrapper } from "./context/comunication.context.jsx";
import { DataProviderWrapper } from "./context/data.context.jsx";
import { RatingDataProviderWrapper } from "./context/rating.context.jsx";
import { YearDataProviderWrapper } from "./context/year.context.jsx";
import { LikeDataProviderWrapper } from "./context/like.context.jsx";

createRoot(document.getElementById("root")).render(
  // <StrictMode>
  <FileProviderWrapper>
    <DataProviderWrapper>
      <RatingDataProviderWrapper>
        <YearDataProviderWrapper>
          <LikeDataProviderWrapper>
            <ComunicationProviderWrapper>
              <App />
            </ComunicationProviderWrapper>
          </LikeDataProviderWrapper>
        </YearDataProviderWrapper>
      </RatingDataProviderWrapper>
    </DataProviderWrapper>
  </FileProviderWrapper>
  // </StrictMode>
);
