from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import tempfile
from werkzeug.utils import secure_filename
import traceback
import subprocess
import sys

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'xlsx', 'json'}

# Hardcoded email credentials
EMAIL_ADDRESS = "test.server.composer@gmail.com"
EMAIL_PASSWORD = "vigd xbrg ofcp zqma"

# Get the parent directory (Team_2) to access the original Python files
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        "message": "File Analysis API",
        "endpoints": {
            "/process-file": "POST - Process and analyze files (PDF, DOCX, TXT, XLSX)",
            "/analyze-json": "POST - Analyze JSON data using Groq AI",
            "/file-analysis": "POST - Detailed file analysis using Groq AI",
            "/load-emails": "GET - Load emails from Gmail inbox",
            "/extract-pdf": "POST - Extract text from PDF using RapidAPI",
            "/summarize-conversation": "POST - Generate conversation summary",
            "/generate-response": "POST - Generate response to messages",
            "/get-subjects": "GET - Get only subject field from inbox messages"
        }
    })

@app.route('/process-file', methods=['POST'])
def process_file_endpoint():
    """Process and analyze files (PDF, DOCX, TXT, XLSX)"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed"}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Run the main.py script with the file path (from parent directory)
        main_script = os.path.join(PARENT_DIR, 'main.py')
        result = subprocess.run([sys.executable, main_script], 
                              input=filepath + '\n', 
                              text=True, 
                              capture_output=True)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        if result.returncode == 0:
            # Read the results.json file (from parent directory)
            results_file = os.path.join(PARENT_DIR, 'results.json')
            try:
                with open(results_file, 'r', encoding='utf-8') as f:
                    results = json.load(f)
                return jsonify({
                    "results": results,
                    "output": result.stdout,
                    "message": "File processed successfully"
                })
            except FileNotFoundError:
                return jsonify({
                    "output": result.stdout,
                    "message": "File processed but results.json not found"
                })
        else:
            return jsonify({
                "error": "Failed to process file",
                "stderr": result.stderr
            }), 500
        
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/analyze-json', methods=['POST'])
def analyze_json_endpoint():
    """Analyze JSON data using Groq AI"""
    try:
        # Check Content-Type header
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json",
                "message": "Please set the Content-Type header to 'application/json'"
            }), 415
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Save JSON data to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            temp_file_path = f.name
        
        # Run the analysis.py script (from parent directory)
        analysis_script = os.path.join(PARENT_DIR, 'analysis.py')
        result = subprocess.run([sys.executable, analysis_script], 
                              capture_output=True, 
                              text=True)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        if result.returncode == 0:
            return jsonify({
                "output": result.stdout,
                "message": "JSON analysis completed successfully"
            })
        else:
            return jsonify({
                "error": "Failed to analyze JSON",
                "stderr": result.stderr
            }), 500
        
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/file-analysis', methods=['POST'])
def file_analysis_endpoint():
    """Detailed file analysis using Groq AI"""
    try:
        # Check Content-Type header
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json",
                "message": "Please set the Content-Type header to 'application/json'"
            }), 415
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Save JSON data to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            temp_file_path = f.name
        
        # Run the file-analysis.py script (from parent directory)
        file_analysis_script = os.path.join(PARENT_DIR, 'file-analysis.py')
        result = subprocess.run([sys.executable, file_analysis_script], 
                              capture_output=True, 
                              text=True)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        if result.returncode == 0:
            return jsonify({
                "output": result.stdout,
                "message": "File analysis completed successfully"
            })
        else:
            return jsonify({
                "error": "Failed to analyze file",
                "stderr": result.stderr
            }), 500
        
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/load-emails', methods=['GET'])
def load_emails_endpoint():
    """Load emails from Gmail inbox using hardcoded credentials"""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(app_dir, 'credentials.json')
    
    try:
        # Use hardcoded credentials
        data = {
            "email": EMAIL_ADDRESS,
            "password": EMAIL_PASSWORD,
            "attachments_folder": "attachments"
        }
        
        # Save credentials to a known file name in the same directory as the script
        with open(credentials_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Define the correct, absolute path to the imap.py script
        imap_script = os.path.join(app_dir, 'imap.py')
        
        # Run the imap.py script with its own directory as the working directory
        result = subprocess.run(
            [sys.executable, imap_script],
            capture_output=True,
            text=True,
            cwd=app_dir  # Set the correct working directory
        )
        
        if result.returncode == 0:
            return jsonify({
                "output": result.stdout,
                "message": "Emails loaded successfully",
                "email": EMAIL_ADDRESS
            })
        else:
            return jsonify({
                "error": "Failed to load emails",
                "stderr": result.stderr,
                "email": EMAIL_ADDRESS
            }), 500
        
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500
    finally:
        # Ensure the credentials file is always cleaned up
        if os.path.exists(credentials_path):
            os.remove(credentials_path)

@app.route('/extract-pdf', methods=['POST'])
def extract_pdf_endpoint():
    """Extract text from PDF using RapidAPI"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Only PDF files are supported"}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Run the resume_parsing.py scnript (from parent directory)
        resume_parsing_script = os.path.join(PARENT_DIR, 'resume_parsing.py')
        result = subprocess.run([sys.executable, resume_parsing_script], 
                              capture_output=True, 
                              text=True)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        if result.returncode == 0:
            return jsonify({
                "output": result.stdout,
                "message": "PDF text extraction completed successfully"
            })
        else:
            return jsonify({
                "error": "Failed to extract text from PDF",
                "stderr": result.stderr
            }), 500
        
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/summarize-conversation', methods=['POST'])
def summarize_conversation_endpoint():
    """Generate conversation summary"""
    try:
        # Check Content-Type header
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json",
                "message": "Please set the Content-Type header to 'application/json'",
                "example": {
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": {
                        "id": "11",
                        "subject": "Test conversation",
                        "from": "test@example.com",
                        "body": "This is a test conversation for summarization."
                    }
                }
            }), 415
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No conversation data provided"}), 400
        
        # Save data to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            temp_file_path = f.name
        
        # Run the resume.py script (from parent directory)
        resume_script = os.path.join(PARENT_DIR, 'resume.py')
        result = subprocess.run([sys.executable, resume_script, temp_file_path],
                              capture_output=True, 
                              text=True)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        if result.returncode == 0:
            return jsonify({
                "output": result.stdout,
                "message": "Conversation summary generated successfully"
            })
        else:
            return jsonify({
                "error": "Failed to generate summary",
                "stderr": result.stderr
            }), 500
        
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/generate-response', methods=['POST'])
def generate_response_endpoint():
    """Generate response to messages"""
    try:
        # Check Content-Type header
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json",
                "message": "Please set the Content-Type header to 'application/json'",
                "example": {
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": {
                        "id": "11",
                        "subject": "Test message",
                        "from": "test@example.com",
                        "body": "This is a test message for response generation."
                    }
                }
            }), 415
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No message data provided"}), 400
        
        # Save data to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            temp_file_path = f.name
        
        # Run the send.py script (from backend directory)
        send_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'send.py')
        result = subprocess.run([sys.executable, send_script, temp_file_path],
                              capture_output=True, 
                              text=True)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        if result.returncode == 0:
            return jsonify({
                "output": result.stdout,
                "message": "Response generated successfully"
            })
        else:
            return jsonify({
                "error": "Failed to generate response",
                "stderr": result.stderr
            }), 500
        
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "API is running"
    })

@app.route('/get-subjects', methods=['GET'])
def get_subjects_endpoint():
    """Get only subject field from inbox messages"""
    try:
        # Path to the inbox messages JSON file
        json_file_path = 'inbox_messages_with_attachments.json'
        
        # Check if file exists
        if not os.path.exists(json_file_path):
            return jsonify({
                "error": "inbox_messages_with_attachments.json file not found"
            }), 404
        
        # Read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as f:
            messages = json.load(f)
        
        # Extract and format the data to match frontend structure
        formatted_messages = []
        for message in messages:
            # Extract sender name from "from" field
            from_field = message.get("from", "")
            sender = from_field.split('<')[0].strip() if '<' in from_field else from_field
            
            # Extract receiver name from "to" field
            to_field = message.get("to", "")
            receiver = to_field.split('<')[0].strip() if '<' in to_field else to_field
            
            # Format date
            date_str = message.get("date", "")
            # Simple date formatting - you might want to improve this
            time = date_str.split(',')[0] if ',' in date_str else date_str[:10]
            
            formatted_messages.append({
                "id": message.get("id", ""),
                "sender": sender,
                "to": message.get("to", ""),
                "receiver": receiver,
                "subject": message.get("subject", ""),
                "description": message.get("body", ""),
                "time": time,
                "seen": False,  # Default to False, you can modify this logic as needed
                "attachments": message.get("attachments", []),
                "attachments_count": message.get("attachments_count", 0)
            })
        
        return jsonify({
            "message": "Messages retrieved successfully",
            "count": len(formatted_messages),
            "messages": formatted_messages
        })
        
    except json.JSONDecodeError as e:
        return jsonify({
            "error": "Invalid JSON format in inbox_messages_with_attachments.json",
            "details": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 