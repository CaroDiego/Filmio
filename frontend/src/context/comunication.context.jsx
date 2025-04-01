import { createContext, useState } from "react";
import api from "../api.js";

const ComunicationContext = createContext();

function ComunicationProviderWrapper(props) {
  const [test, setTest] = useState("");

  const fetchTest = async () => {
    try {
      const response = await api.get("/test");
      setTest(response.data.test);
    } catch (error) {
        console.error("Error fetching test", error);
        setTest("Error fetching test, check the console for details.");
    }
  };

  return (
    <ComunicationContext.Provider value={{ test, fetchTest }}>
      {props.children}
    </ComunicationContext.Provider>
  );
}

export { ComunicationContext, ComunicationProviderWrapper };
