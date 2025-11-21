const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const csv = require('csvtojson'); // for CSV parsing

const app = express();
const PORT = 3000;

app.use(cors());

const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('file'), async (req, res) => {
  if (!req.file) return res.sendStatus(400);

  const originalPath = path.join(__dirname, req.file.path);
  const jsonPath = path.join(__dirname, 'uploads', `${req.file.filename}.json`);

  try {
    const fileContent = fs.readFileSync(originalPath, 'utf8');

    // Convert CSV to JSON (optional, if CSV file)
    const jsonArray = await csv().fromString(fileContent);

    // Save JSON file
    fs.writeFileSync(jsonPath, JSON.stringify(jsonArray, null, 2), 'utf8');

    console.log(`Saved JSON to ${jsonPath}`);
    res.status(200).json({ message: 'File uploaded and saved as JSON successfully', jsonFile: `${req.file.originalPath}.json` });
  } catch (err) {
    console.error("Error handling file:", err);
    res.status(500).json({ error: 'Failed to convert and save file as JSON' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
