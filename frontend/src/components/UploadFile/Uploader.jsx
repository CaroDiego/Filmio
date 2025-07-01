import React, { useRef, useState, useContext } from "react";
import { FileContext } from "../../context/file.contenxt";

import "./Uploader.css";
import { MdFileUpload, MdClose } from "react-icons/md";
import { FaFileArchive } from "react-icons/fa";

function Uploader() {
  const inputRef = useRef();
  const { uploadFile, files, fileName, fileSize, error } =
    useContext(FileContext);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("select"); // "select", "uploading", "done"

  const onChooseFile = () => {
    inputRef.current.click();
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const clearFileInput = () => {
    inputRef.current.value = "";
    setSelectedFile(null);
    setUploadStatus("select");
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    await uploadFile(selectedFile);
  };

  return (
    <div>
      <input
        ref={inputRef}
        type="file"
        onChange={handleFileChange}
        style={{ display: "none" }}
      />
      {!selectedFile && (
        <button className="file-btn" onClick={onChooseFile}>
          {/* TODO add upload symbol*/}
          <span className="material-symbols-outlined">
            <MdFileUpload />{" "}
          </span>{" "}
          Upload File
        </button>
      )}

      {selectedFile && (
        <>
          <div className="file-card">
            <span className="material symbols-outlined icon">
              <FaFileArchive />
            </span>
            <div className="file-info">
              <div style={{ flex: 1 }}>
                <h6>{selectedFile.name}</h6>
                <div className="progress-bg">
                  <div className="progress" style={{ width: `40%` }} />
                </div>
              </div>

              <button onClick={clearFileInput}>
                <span className="material-symbols-outlined close-icon">
                  {" "}
                  <MdClose />
                </span>
              </button>
            </div>
          </div>
          <button className="upload-btn" onClick={handleUpload}>
            Upload
          </button>
        </>
      )}
    </div>
  );
}

export default Uploader;
