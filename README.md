# 📊 Farmgate Dashboard – JAMIS Data Explorer

<<<<<<< HEAD
=======
🌐 **Live Dashboard:** Visit the Farmgate JAMIS Dashboard here 👉 [https://jcs-da-farmgate.streamlit.app/](https://jcs-da-farmgate.streamlit.app/)

---

>>>>>>> 1fd1d84 (Initial commit)
Welcome to the **Farmgate Dashboard**, a powerful data visualization tool built with **Streamlit** that transforms raw PDF data from the **JAMIS website** into interactive insights.

## 🔍 Project Overview

This dashboard extracts and analyzes agricultural and market data from the **Jamaica Agricultural Marketing Information System (JAMIS)**. It combines real-time PDF data scraping with an elegant web interface to help users understand pricing trends, volumes, and regional patterns across Jamaica.

---

## 🛠️ How It Works

### 🧱 Tech Stack
- **Streamlit**: Frontend dashboard interface
- **FastAPI**: Backend API to manage data fetching and routing
- **pdfplumber**: Extracts structured tables and content from JAMIS PDF reports

---

### 📡 Data Flow

1. **PDF Collection**: The system fetches market reports published on JAMIS.
2. **PDF Parsing**: `pdfplumber` extracts structured data from complex tables in the PDF files.
3. **API Exposure**: A lightweight `FastAPI` backend serves parsed data via REST endpoints.
4. **Dashboard Visualization**: Streamlit dynamically loads the data into charts, tables, and filterable views.

---

## 🚀 Features

- 📈 Interactive charts and data tables
- 🔍 Filter by product, parish, or market location
- 🗂 Downloadable CSVs of parsed data
- 🧠 Automatic parsing of new PDF uploads
- ☁️ FastAPI endpoint integration for future extensibility

---

## 📂 Folder Structure

```bash
farmgate/
├── data/              # CSVs and cleaned outputs
├── images/            # Charts, logos, and other visuals
├── pages/             # Multi-page Streamlit dashboard code
├── style/             # Custom CSS for dashboard styling
├── Home.py            # Main entry point for the app
├── requirements.txt   # Python dependencies
└── README.md          # You're here!
