import { createContext, useState } from "react";
import api from "../api";

const YearContext = createContext();

function YearDataProviderWrapper(props) {
  const [year, setYear] = useState([]);
  const [error, setError] = useState(null);
  const category = "Year";

  const getSimpleDataYear = async () => {
    try {
      const response = await api.get(`/simpledata/${category}`);
      setYear(response.data.data);
      setError(null);
    } catch (error) {
      setError("Failed to fetch simple data for category:" + category);
      console.error(error);
    }
  };

  const groupedByDecade = year?.reduce((acc, item) => {
    const decade = Math.floor(item.key / 10) * 10; // Group by decade (e.g., 2000, 2010, etc.)
    if (!acc[decade]) {
      acc[decade] = { key: decade, value: 0 };
    }
    acc[decade].value += item.value; // Sum the values for each decade
    return acc;
  }, {}) || {};

  return (
    <YearContext.Provider
      value={{
        year,
        error,
        getSimpleDataYear,
        groupedByDecade,
      }}
    >
      {props.children}
    </YearContext.Provider>
  );
}

export { YearContext, YearDataProviderWrapper };
