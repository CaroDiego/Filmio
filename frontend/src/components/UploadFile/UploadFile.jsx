import React, { useContext, useEffect, useState } from "react";
import { FileContext } from "../../context/file.contenxt";
import BarChartComponent from "../charts/Rating/RatingBarVertical";
import { RatingContext } from "../../context/rating.context";
import YearBarVertical from "../charts/Year/YearBarVertical";
import { YearContext } from "../../context/year.context";
import { LikeContext } from "../../context/like.context";
import LikesPieChart from "../charts/Likes/LikesPieChart";
import Uploader from "./uploader";

function UploadFile() {
  const { uploadFile, files, fileName, fileSize, error } =
    useContext(FileContext);

  // const { getSimpleDataCategory, data } = useContext(DataContext);
  const { getSimpleDataRating, rating } = useContext(RatingContext);
  const { getSimpleDataYear, year } = useContext(YearContext);
  const { getSimpleDataLike, like } = useContext(LikeContext);
  const [file, setFile] = useState();

  const handleChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await uploadFile(file);
    await getSimpleDataRating();
    await getSimpleDataYear();
    await getSimpleDataLike();
  };

  return (
    <div>
      <Uploader />
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
        {rating && (
          <>
            <BarChartComponent />
            <YearBarVertical />
            <LikesPieChart />
          </>
        )}
      </div>
    </div>
  );
}

export default UploadFile;
