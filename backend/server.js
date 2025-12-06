const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const csv = require('csvtojson');
const XLSX = require('xlsx');
const axios = require('axios');  // <--- Added to call Python API

const app = express();
const PORT = 3000;

app.use(cors());

// --------------------------------
// CLEAR UPLOAD FOLDER
// --------------------------------
function clearUploadFolder() {
  const directory = path.join(__dirname, 'uploads');
  fs.readdir(directory, (err, files) => {
    if (err) return;
    files.forEach(file => fs.unlink(path.join(directory, file), () => {}));
  });
}

// --------------------------------
// Multer upload system
// --------------------------------
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, 'uploads/'),
  filename: (req, file, cb) => cb(null, file.originalname)
});
const upload = multer({ storage });

// --------------------------------
// Upload Route
// --------------------------------
app.post('/upload', (req, res, next) => {
  clearUploadFolder();
  next();
}, upload.single('file'), async (req, res) => {

  if (!req.file) return res.status(400).json({ error: "No file uploaded" });

  const filePath = path.join(__dirname, 'uploads', req.file.originalname);
  const ext = path.extname(req.file.originalname).toLowerCase();

  let rawData;

  try {
    // 📌 CSV
    if (ext === ".csv") {
      const content = fs.readFileSync(filePath, "utf8");
      rawData = await csv().fromString(content);
    }
    // 📌 TXT
    else if (ext === ".txt") {
      const content = fs.readFileSync(filePath, "utf8");
      rawData = content.split("\n").map(line => line.trim());
    }
    // 📌 XLSX
    else if (ext === ".xlsx") {
      const workbook = XLSX.readFile(filePath);
      const sheet = workbook.Sheets[workbook.SheetNames[0]];
      rawData = XLSX.utils.sheet_to_json(sheet);
    }
    // 📌 JSON
    else if (ext === ".json") {
      rawData = JSON.parse(fs.readFileSync(filePath, "utf8"));
    }

    // --------------------------------------------
    // SEND rawData → PYTHON SERVER FOR PROCESSING
    // --------------------------------------------
    const pythonResponse = await axios.post(
      "http://localhost:5000/process",
      { rawData }
    );

    return res.json({
      message: "Processed successfully",
      result: pythonResponse.data   // <--- Python output
    });

  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Processing failed" });
  }
});

app.listen(PORT, () => {
  console.log(`Node server running at http://localhost:${PORT}`);
});
