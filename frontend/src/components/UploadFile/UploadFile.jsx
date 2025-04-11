import React, { useContext, useEffect, useState } from "react";
import { FileContext } from "../../context/file.contenxt";
import { DataContext } from "../../context/data.context";
import BarChartComponent from "../charts/Rating/RatingBarVertical";


function UploadFile() {
  const { uploadFile, files, fileName, fileSize, error } =
    useContext(FileContext);

  const { getSimpleDataCategory, data } =
    useContext(DataContext);
  const [file, setFile] = useState();

  useEffect(() => {
    if (data) {
      console.log("Data available:", data);
    } else {
      console.log("No data available yet.");
    }
  }, [data]);

  const handleChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await uploadFile(file);
    await getSimpleDataCategory("Rating");
  };

  // const printFiles = () => {
  //   return files.map((file, index) => (
  //     <li key={index}>
  //       <strong>Filename:</strong> {file} <br />
  //     </li>
  //   ));
  // };

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
      <div style={{ width: "100%", height: "400px" }}>
        {data && <BarChartComponent />}
      </div>
    </div>
  );
}

export default UploadFile;
