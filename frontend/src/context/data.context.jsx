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

  const getSimpleDataCategory = async (category) => {
    try {
      const response = await api.get(`/simpledata/${category}`);
      setData(response.data.data);
      setError(null);
    } catch (error) {
      setError("Failed to fetch simple data for category: " + category);
      console.error(error);
    }
  };

  return (
    <DataContext.Provider
      value={{
        data,
        error,
        getSimpleData,
        getSimpleDataCategory,
      }}
    >
      {props.children}
    </DataContext.Provider>
  );
}

export { DataContext, DataProviderWrapper };
