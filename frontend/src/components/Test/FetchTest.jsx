import { useContext } from "react";
import { ComunicationContext } from "../../context/comunication.context";


function FetchTest() {
  const { fetchTest, test } = useContext(ComunicationContext);

  const handleFetch = async () => {
    fetchTest();
  };
  return (
    <div>
      <button onClick={handleFetch}>Test Fetch</button>
      <p>{test}</p>
    </div>
  );
}

export default FetchTest;
