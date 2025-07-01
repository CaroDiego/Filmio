import { createContext, useState } from "react";
import api from "../api";

const RatingContext = createContext();

function RatingDataProviderWrapper(props) {
  const [rating, setRating] = useState(null);
  const [error, setError] = useState(null);
  const category = "Rating";

  const getSimpleDataRating = async () => {
    try {
      const response = await api.get(`/simpledata/${category}`);
      setRating(response.data.data);
      setError(null);
    } catch (error) {
      setError("Failed to fetch simple data for category: " + category);
      console.error(error);
    }
  };

  return (
    <RatingContext.Provider
      value={{
        rating,
        error,
        getSimpleDataRating,
      }}
    >
      {props.children}
    </RatingContext.Provider>
  );
}

export { RatingContext, RatingDataProviderWrapper };
