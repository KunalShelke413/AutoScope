const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const csv = require('csvtojson');
const XLSX = require('xlsx');

const app = express();
const PORT = 3000;

app.use(cors());

// ------------------------------
// CLEAR UPLOAD FOLDER
// ------------------------------
function clearUploadFolder() {
  const directory = path.join(__dirname, 'uploads');

  fs.readdir(directory, (err, files) => {
    if (err) return console.error("Failed to read upload folder:", err);

    for (const file of files) {
      fs.unlink(path.join(directory, file), err => {
        if (err) console.error("Failed to delete file:", file, err);
      });
    }
  });
}

// ------------------------------
// MULTER STORAGE
// ------------------------------
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, 'uploads/'),

  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    cb(null, "data" + ext);   // <-- change file name here
  }
});

const upload = multer({ storage });

// ------------------------------
// FILE PROCESSING ROUTE
// ------------------------------
app.post('/upload', (req, res, next) => {
  clearUploadFolder();
  next();
}, upload.single('file'), async (req, res) => {

  if (!req.file) return res.status(400).json({ error: "No file uploaded" });

  const filePath = path.join(__dirname, "uploads", req.file.filename);
  const ext = path.extname(req.file.filename).toLowerCase();

  try {
    let rawData;

    if (ext === '.csv') {
      const fileContent = fs.readFileSync(filePath, 'utf8');
      rawData = await csv().fromString(fileContent);
    }
    else if (ext === '.xlsx') {
      const workbook = XLSX.readFile(filePath);
      const sheetName = workbook.SheetNames[0];
      rawData = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
    }
    else if (ext === '.json') {
      const fileContent = fs.readFileSync(filePath, 'utf8');
      rawData = JSON.parse(fileContent);
    }
    else if (ext === '.txt') {
      const fileContent = fs.readFileSync(filePath, 'utf8');
      rawData = fileContent.split('\n').map(line => line.trim());
    }
    else {
      return res.status(400).json({ error: "Unsupported file format" });
    }

    res.status(200).json({
      message: "File processed successfully",
      rawData
    });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "File processing failed" });
  }
});
// ------------------------------
// START SERVER
// ------------------------------
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
