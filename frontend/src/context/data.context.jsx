import { createContext, useState } from "react";
import api from "../api.js";

const DataContext = createContext();

function DataProviderWrapper(props) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const getSimpleData = async () => {
    try {
      const response = await api.get("/simpledata");
      setData(response.data.data);
      setError(null);
    } catch (error) {
      setError("Failed to fetch simple data");
      console.error(error);
    }
  };

  return (
    <DataContext.Provider
      value={{
        data,
        error,
        getSimpleData,
      }}
    >
      {props.children}
    </DataContext.Provider>
  );
}

export { DataContext, DataProviderWrapper };
