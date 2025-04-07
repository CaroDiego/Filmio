import React, { useContext, useEffect, useState } from "react";
import { FileContext } from "../../context/file.contenxt";

function UploadFile() {
  const { uploadFile, files, fileName, fileSize, error, getSimpleData, data } =
    useContext(FileContext);
  const [file, setFile] = useState();

  useEffect(() => { 
    if (data) {
      data.forEach((item, i) => {
        console.log(`Item ${i + 1}:`, item);
      })
    }
  }, [data]);

  const handleChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await uploadFile(file);
    await getSimpleData();
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
          <ul>
            <strong>Error:</strong> {error}
          </ul>
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
