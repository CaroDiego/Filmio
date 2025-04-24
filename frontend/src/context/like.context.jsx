import { createContext, useState } from "react";
import api from "../api";

const LikeContext = createContext();

function LikeDataProviderWrapper(props) {
  const [like, setLike] = useState(null);
  const category = "Like";

  const getSimpleDataLike = async () => {
    try {
      const response = await api.get(`/simpledata/${category}`);
      setLike(response.data.data);
    } catch (error) {
      console.error("Failed to fetch simple data for category: Like", error);
    }
  };

  return (
    <LikeContext.Provider
      value={{
        like,
        getSimpleDataLike,
      }}
    >
      {props.children}
    </LikeContext.Provider>
  );
}

export { LikeContext, LikeDataProviderWrapper };
