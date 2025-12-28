# 🚀 AutoScope

AutoScope is an **automated data analysis web application** that allows users to upload files (CSV, Excel, PDF, text, etc.) and automatically generates **cleaned data, visualizations, insights, and dashboards**.
The goal of this project is to reduce manual effort in data analysis and help users quickly understand their data through charts and summaries.

> ⚠️ **Disclaimer**: The results shown are automatically generated and may contain inaccuracies. Use them as guidance only, not as final conclusions.

---

## 📌 Features

* Upload multiple file formats (CSV, Excel, JSON, Text, PDF)
* Automatic data cleaning and preprocessing
* Smart chart generation based on column types
* Multiple chart types:

  * Bar chart
  * Line chart
  * Pie chart
  * Area chart
  * Scatter plot
  * Box plot
  * Heatmap
* Automatic insights (Top values, trends, comparisons)
* Interactive dashboards using Plotly
* Modern responsive UI

---

## 🛠️ Tech Stack

### Frontend

* **React.js**
* **Plotly.js** (interactive charts)
* CSS (responsive design for mobile & desktop)

### Backend

* **Python**
* **Pandas** (data processing & analysis)
* **NumPy**
* **FastAPI / Flask** (API layer)

---

## 🔄 Project Workflow

1. **File Upload**
   User uploads a data file from the frontend.

2. **Backend Processing**

   * File is read using Pandas
   * Data cleaning (null handling, type detection)
   * Column classification (categorical / numerical)

3. **Chart Selection Logic**
   Based on column types, suitable charts are automatically selected.

4. **Visualization Generation**
   Charts are generated using Plotly (both Python & JS).

5. **Insights Generation**
   AutoScope generates basic insights such as:

   * Top 3 and bottom 3 values
   * Trends
   * Distributions

6. **Dashboard Display**
   The frontend displays charts and insights in an interactive dashboard.

---

## ▶️ How to Run the Project Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/KunalShelke413/AutoScope.git
cd AutoScope
```

---

### 2️⃣ Backend Setup (Python)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
npm start
```

Run python server:

```bash
cd python_api
uvicorn processor:app --reload
```

---

### 3️⃣ Frontend Setup (React)

```bash
cd AutoScope
npm install
npm run dev
```

Frontend will start on:

```
http://localhost:5173
```

---

## 📂 Project Structure

```
AutoScope/
│
├── src/
│   └── public/
│
├── backend/           
│   ├── uploads/
│   └── server.js
│   
├── python_api/
│   └──processer.py
│
│
├── README.md
└── requirements.txt
```

---

## 🎯 Future Enhancements

* Advanced statistical insights
* Machine learning-based predictions
* User authentication
* Saved dashboards
* Export charts as PDF/PNG
* Improved accuracy with smarter analysis rules

---

## 🙌 Acknowledgement

This is my **first major project using Python and React**.
More features and improvements will be added in future updates.

If you are still here, **thank you for checking out AutoScope!** ⭐

---

## 🔗 GitHub Repository

All source code and future updates are available here:

👉 [https://github.com/KunalShelke413/AutoScope](https://github.com/KunalShelke413/AutoScope)

---

**Developed by:** Kunal Shelke
