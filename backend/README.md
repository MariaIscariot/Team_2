# Backend - File Analysis API Server

This directory contains the Flask API server and all related files for the File Analysis API.

## Directory Structure

```
backend/
├── app.py                              # Main Flask server
├── requirements.txt                    # Python dependencies
├── start_server.py                     # Server startup script
├── test_api.py                         # API test script
├── test_summarize_conversation.py      # Conversation endpoint test
├── File_Analysis_API.postman_collection.json  # Postman collection
├── POSTMAN_REQUESTS.txt                # Postman requests guide
└── README.md                           # This file
```

## Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### 3. Start the Server
```bash
python start_server.py
```

The server will start on `http://localhost:5000`

## Usage

### Quick Start
```bash
cd backend
python start_server.py
```

### Manual Start
```bash
cd backend
python app.py
```

### Testing
```bash
cd backend
python test_api.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API documentation |
| GET | `/health` | Health check |
| POST | `/process-file` | Process files (PDF, DOCX, TXT, XLSX) |
| POST | `/analyze-json` | Analyze JSON with Groq AI |
| POST | `/file-analysis` | Detailed file analysis |
| GET | `/load-emails` | Load Gmail emails |
| POST | `/extract-pdf` | Extract PDF text |
| POST | `/summarize-conversation` | Generate conversation summary |
| POST | `/generate-response` | Generate response to messages |

## Configuration

### Email Credentials
The server uses hardcoded Gmail credentials:
- Email: `test.server.composer@gmail.com`
- Password: `vigd xbrg ofcp zqma`

### File Paths
- Upload folder: `uploads/` (created automatically)
- Original Python scripts: `../` (parent directory)
- Attachments: `../attachments/` (parent directory)

## Testing

### Run All Tests
```bash
python test_api.py
```

### Test Specific Endpoint
```bash
python test_summarize_conversation.py
```

### Postman Collection
Import `File_Analysis_API.postman_collection.json` into Postman for easy testing.

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the backend directory
2. **File not found**: Check that original Python files are in parent directory
3. **Port already in use**: Change port in `app.py` or kill existing process
4. **Gmail connection failed**: Check internet and Gmail settings

### Dependencies
Make sure all dependencies are installed:
```bash
pip install flask flask-cors werkzeug pandas PyMuPDF python-docx spacy groq requests openpyxl
```

## Development

### Adding New Endpoints
1. Add route in `app.py`
2. Update test script
3. Update Postman collection
4. Update documentation

### File Structure
- `app.py`: Main Flask application
- `start_server.py`: Automated setup and startup
- `test_*.py`: Test scripts for endpoints
- `*.json`: Postman collections and configurations

## Notes

- The server runs the original Python scripts from the parent directory
- All file uploads are stored temporarily in `uploads/` folder
- Results are saved to `../results.json` in parent directory
- The server supports CORS for cross-origin requests 