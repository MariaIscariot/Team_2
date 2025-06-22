# File Analysis API

A comprehensive file analysis and processing system with a Flask REST API backend.

## Project Structure

```
Team_2/
├── backend/                           # Flask API server
│   ├── app.py                        # Main Flask application
│   ├── requirements.txt              # Python dependencies
│   ├── start_server.py               # Server startup script
│   ├── test_api.py                   # API test script
│   ├── test_summarize_conversation.py # Conversation endpoint test
│   ├── File_Analysis_API.postman_collection.json # Postman collection
│   ├── POSTMAN_REQUESTS.txt          # Postman requests guide
│   └── README.md                     # Backend documentation
├── attachments/                       # Sample files for testing
├── main.py                           # File processing functionality
├── analysis.py                       # JSON analysis with Groq AI
├── file-analysis.py                  # Detailed file analysis
├── imap.py                           # Email loading functionality
├── resume_parsing.py                 # PDF text extraction
├── resume.py                         # Conversation summary
├── send.py                           # Response generation
├── start_backend.py                  # Quick backend startup
└── README.md                         # This file
```

## Quick Start

### 1. Start the Backend Server
```bash
python start_backend.py
```

Or manually:
```bash
cd backend
python start_server.py
```

The server will start on `http://localhost:5000`

### 2. Test the API
```bash
cd backend
python test_api.py
```

### 3. Use Postman
Import the collection: `backend/File_Analysis_API.postman_collection.json`

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

## Features

- **File Processing**: Support for PDF, DOCX, TXT, and XLSX files
- **AI Analysis**: Integration with Groq AI for intelligent analysis
- **Email Integration**: Gmail inbox loading with attachments
- **PDF Extraction**: Text extraction from PDF files
- **Conversation Analysis**: Summarize and generate responses to conversations
- **REST API**: Full REST API with proper error handling

## Configuration

### Email Settings
- Email: `test.server.composer@gmail.com`
- Password: `vigd xbrg ofcp zqma`

### File Paths
- Uploads: `backend/uploads/`
- Attachments: `attachments/`
- Results: `results.json`

## Documentation

- **Backend Documentation**: See `backend/README.md`
- **API Guide**: See `backend/POSTMAN_REQUESTS.txt`
- **Postman Collection**: `backend/File_Analysis_API.postman_collection.json`

## Development

### Adding New Functionality
1. Create Python script in root directory
2. Add endpoint in `backend/app.py`
3. Update test scripts
4. Update Postman collection

### Testing
```bash
cd backend
python test_api.py
```

## Troubleshooting

- **Server won't start**: Check dependencies in `backend/requirements.txt`
- **Import errors**: Make sure you're in the correct directory
- **File not found**: Check file paths in `backend/app.py`
- **Gmail connection**: Verify email credentials and internet connection
