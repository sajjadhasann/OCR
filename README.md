# OCR API - FastAPI + Mistral

**Optical Character Recognition (OCR) API** that receives PDF, JPG, or PNG files and returns extracted text in JSON format.

---

## Features

- Accepts **PDF, JPG, JPEG, PNG** files.
- Uses **Mistral OCR** to extract text.
- Returns results as JSON:
```json
{
  "status": "success",
  "pages": ["Page 1 text", "Page 2 text", ...]
}
```
Handles unsupported file types gracefully:

```json
{
  "status": "failed",
  "error": "Mistral OCR could not process this file type",
  "details": "Error details from API"
}
```
No files are stored on the server; processing happens in memory.

## Requirements
- Python 3.10+
- FastAPI
- MistralAI Python SDK

## Installation
* Clone the repository:
```bash
git clone https://github.com/sajjadhasann/OCR.git
cd OCR
```

* Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

* Install dependencies:
```bash
pip install -r requirements.txt
```

* Set Mistral API key in environment variable:
```bash
export MISTRAL_API_KEY="your_api_key_here"   # Linux/macOS
set MISTRAL_API_KEY="your_api_key_here"      # Windows
```

## Usage
Run the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Send a POST request to /extract-text with your file:
```bash
curl -X POST "http://localhost:8000/extract-text" -F "file=@document.pdf"
```

## Notes
- This project uses Mistral OCR, which requires a valid API key.
- Mistral API is not open source and may have usage limits.
- All files are processed in memory; no PDF or image is stored on the server.

## License
This project is licensed under the MIT License. See LICENSE for details.
