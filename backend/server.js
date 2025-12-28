const express = require("express");
const multer = require("multer");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const csv = require("csvtojson");
const XLSX = require("xlsx");

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// ------------------------------
// GLOBAL STATE (last upload info)
// ------------------------------
let lastUploadedFileName = "";
let lastUploadedExt = "";
let lastUploadedAt = "";

// ------------------------------
// ENSURE UPLOADS FOLDER EXISTS
// ------------------------------
const uploadDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

// ------------------------------
// CLEAR UPLOAD FOLDER
// ------------------------------
function clearUploadFolder() {
  fs.readdir(uploadDir, (err, files) => {
    if (err) return;

    for (const file of files) {
      fs.unlink(path.join(uploadDir, file), () => {});
    }
  });
}

// ------------------------------
// MULTER STORAGE
// ------------------------------
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),

  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    cb(null, "data" + ext); // stored name
  }
});

const upload = multer({ storage });

// ------------------------------
// UPLOAD & PROCESS FILE
// ------------------------------
app.post(
  "/upload",
  (req, res, next) => {
    clearUploadFolder();
    next();
  },
  upload.single("file"),
  async (req, res) => {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const filePath = path.join(uploadDir, req.file.filename);
    const ext = path.extname(req.file.filename).toLowerCase();

    try {
      let rawData;

      if (ext === ".csv") {
        const content = fs.readFileSync(filePath, "utf8");
        rawData = await csv().fromString(content);
      } else if (ext === ".xlsx") {
        const workbook = XLSX.readFile(filePath);
        const sheet = workbook.SheetNames[0];
        rawData = XLSX.utils.sheet_to_json(workbook.Sheets[sheet]);
      } else if (ext === ".json") {
        const content = fs.readFileSync(filePath, "utf8");
        rawData = JSON.parse(content);
      } else if (ext === ".txt") {
        const content = fs.readFileSync(filePath, "utf8");
        rawData = content
          .split("\n")
          .map(line => line.trim())
          .filter(Boolean);
      } else {
        return res.status(400).json({ error: "Unsupported file format" });
      }

      // Store metadata
      lastUploadedFileName = req.file.originalname;
      lastUploadedExt = ext;
      lastUploadedAt = new Date().toISOString();

      res.status(200).json({
        message: "File processed successfully",
        fileName: lastUploadedFileName,
        rawData
      });
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: "File processing failed" });
    }
  }
);

// ------------------------------
// DASHBOARD SAFE METADATA ROUTE
// ------------------------------
app.get("/uploaded-file-info", (req, res) => {
  res.json({
    fileName: lastUploadedFileName,
    extension: lastUploadedExt,
    uploadedAt: lastUploadedAt
  });
});

// ------------------------------
// HEALTH CHECK
// ------------------------------
app.get("/", (req, res) => {
  res.send("AutoScope upload server running");
});

// ------------------------------
// START SERVER
// ------------------------------
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
