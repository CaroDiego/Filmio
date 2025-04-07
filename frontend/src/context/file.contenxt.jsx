import { createContext, useState } from "react";
import api from "../api.js";
import { formatBytes } from "../utils/files.js";

const FileContext = createContext();

function FileProviderWrapper(props) {
  const [files, setFiles] = useState([]);
  const [fileName, setFileName] = useState("");
  const [fileSize, setFileSize] = useState("");
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/uploadfile", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setFiles(response.data.file_list);
      setFileName(response.data.file_name);
      const size = formatBytes(response.data.file_size, 2);
      setFileSize(size);
      setError(null);
    } catch (error) {
      if (error.response) {
        setError(error.response.data.detail);
      } else if (error.request) {
        setError("No response from server");
      } else {
        setError("Error: " + error.message);
      }
    }
  };


  const getSimpleData = async () => {
    try {
      const response = await api.get("/simpledata");  
      setData(response.data.data);
      setError(null);
    } catch (error) {
      setError("Failed to fetch simple data");
      console.error(error);
    }
   }

  return (
    <FileContext.Provider
      value={{
        uploadFile,
        files,
        fileName,
        fileSize,
        error,
        data,
        getSimpleData,
      }}
    >
      {props.children}
    </FileContext.Provider>
  );
}

export { FileContext, FileProviderWrapper };
