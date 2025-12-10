import { Link } from 'react-router-dom';
import { useContext, useState } from "react";
import { UploadContext } from "../UploadContext";

const Detail = () => {
  const { isUploaded } = useContext(UploadContext);

  // ➜ NEW STATE to disable button after first click
  const [started, setStarted] = useState(false);

  function handleClick(e) {
    if (!isUploaded) {
      e.preventDefault();
      alert("Please upload a file before getting started!");
      return;
    }

    // Disable button after successful click
    setStarted(true);
  }

  return (
    <div className="my_content">
      <h3>Welcome to</h3>
      <h1>AutoScope</h1>
      <p>Your one-stop solution for automated code analysis and insights.</p>

      <Link to={isUploaded ? "/dashboard" : "#"}>
        <button
          className="btn btn-primary"
          disabled={!isUploaded || started}   // <-- disable after click
          onClick={handleClick}
        >
          {started ? "Processing..." : "Get Started"}
        </button>
      </Link>
    </div>
  );
};

export default Detail;
