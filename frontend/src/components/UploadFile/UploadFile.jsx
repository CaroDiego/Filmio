import React, { useContext, useState } from "react";
import { FileContext } from "../../context/file.contenxt";

function UploadFile() {
  const { uploadFile, files, fileName, fileSize, error } =
    useContext(FileContext);
  const [file, setFile] = useState();

  const handleChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    uploadFile(file);
  };

  const printFiles = () => {
    return files.map((file, index) => (
      <li key={index}>
        <strong>Filename:</strong> {file} <br />
      </li>
    ));
  };

  return (
    <div>
      <ul>
        {fileName && (
          <ul>
            <strong>Filename:</strong> {fileName} <br />
            <strong>File size:</strong> {fileSize} <br />
          </ul>
        )}
        {error && (
          <li>
            <strong>Error:</strong> {error}
          </li>
        )}
      </ul>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleChange} />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}

export default UploadFile;
