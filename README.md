# Intelligent Web Crawler and Real-Time Data Extraction System Using Python

## 📌 Project Overview

The Intelligent Web Crawler is a Python-based application that automates data collection from multiple websites and web APIs. It extracts useful information from HTML pages and processes structured JSON responses.

The system implements sequential and asynchronous crawling techniques to compare their execution times. A FastAPI backend connects the crawling modules with a web interface that displays the extracted results.

## 🎯 Objectives

- Automate data extraction from multiple URLs.
- Extract titles, hyperlinks, text, and response details from HTML pages.
- Parse structured JSON data from APIs.
- Implement and compare sequential and asynchronous crawling.
- Display extracted information and execution times through a web interface.
- Handle request failures and errors.

## 🛠️ Technologies Used

- **Python** – Core programming language
- **Requests** – Synchronous HTTP requests
- **BeautifulSoup** – HTML parsing and data extraction
- **aiohttp** – Asynchronous HTTP requests
- **asyncio** – Concurrent execution of network requests
- **FastAPI** – Backend API development
- **HTML, CSS, JavaScript** – Frontend development
- **pytest** – Automated testing

## 📂 Project Structure

```text
Intelligent-Web-Crawler/
├── src/
│   ├── basic_crawler.py
│   ├── crawler.py
│   ├── url_manager.py
│   ├── async_crawler.py
│   └── api.py
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/
├── data/
├── results/
├── main.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Intelligent-Web-Crawler.git
cd Intelligent-Web-Crawler
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m uvicorn src.api:app --reload
```

### 6. Open the application

Visit `http://127.0.0.1:8000` in your browser.

## 🔄 Working Process

1. The user enters one or more URLs through the web interface.
2. The frontend sends the URLs to the FastAPI backend.
3. The sequential crawler processes URLs one by one.
4. The asynchronous crawler processes network requests concurrently.
5. The system extracts HTML content or parses JSON responses.
6. The results and execution times are displayed on the interface.

## 📊 Output

The application displays:

- URL and HTTP status code
- Content type (HTML or JSON)
- Page title
- Number of hyperlinks found
- Response size
- Extracted text or JSON data
- Sequential and asynchronous execution times

## 🚀 Future Enhancements

- Export extracted results to CSV or JSON files.
- Support automatic URL discovery and multi-page crawling.
- Improve support for JavaScript-rendered websites.
- Add database storage for crawling results.
- Deploy the application to a cloud platform.

## 👩‍💻 Author

**Katari Thanmai**

## 📄 License

This project is developed for educational and academic purposes.
