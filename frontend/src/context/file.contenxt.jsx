import { createContext, useState } from "react";
import api from "../api.js";
import { formatBytes } from "../utils/files.js";

const FileContext = createContext();

function FileProviderWrapper(props) {
  const [files, setFiles] = useState([]);
  const [fileName, setFileName] = useState("");
  const [fileSize, setFileSize] = useState("");
  const [error, setError] = useState(null);

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

  return (
    <FileContext.Provider
      value={{ uploadFile, files, fileName, fileSize, error }}
    >
      {props.children}
    </FileContext.Provider>
  );
}

export { FileContext, FileProviderWrapper };
