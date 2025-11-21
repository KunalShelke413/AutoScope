import axios from 'axios';
import { ChangeEvent, useState } from 'react';

type UploadStatus = 'idle' | 'uploading' | 'success' | 'error';

const Upload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<UploadStatus>('idle');
  const [uploadProgress, setUploadProgress] = useState(0);

  function handleFileChange(e: ChangeEvent<HTMLInputElement>) {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  }

  async function handleFileUpload() {
    if (!file) return;

    setStatus('uploading');
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post("http://localhost:3000/upload", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const total = progressEvent.total || 1;
          const current = progressEvent.loaded;
          setUploadProgress(Math.round((current / total) * 100));
        },
      });

      setStatus('success');
      setUploadProgress(100);
    } catch {
      setStatus('error');
      setUploadProgress(0);
    }
  }

  return (
    <div>
      <form>
        <div className="mb-3">
          <label htmlFor="fileInput" className="form-label">Select a file</label>
          <input type="file" className="form-control" onChange={handleFileChange} id="fileInput" required />
        </div>

        {file && (
          <div className="mb-3">
            <p>File name: {file.name}</p>
            <p>File size: {(file.size / 1024).toFixed(2)} KB</p>
            <p>File type: {file.type}</p>
          </div>
        )}

        {status === 'uploading' && (
          <div className="mb-3">
            <p>Uploading: {uploadProgress}%</p>
            <progress value={uploadProgress} max="100" className="w-full"></progress>
          </div>
        )}

        {file && status !== 'uploading' && (
          <button
            style={{ color: "black" }}
            onClick={(e) => {
              e.preventDefault();
              handleFileUpload();
            }}
          >
            Upload
          </button>
        )}

        {status === 'success' && (
          <p className="text-sm text-green-600">File uploaded successfully!</p>
        )}
        {status === 'error' && (
          <p className="text-sm text-red-600">Upload failed. Please try again.</p>
        )}
      </form>
    </div>
  );
};

export default Upload;



