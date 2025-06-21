import requests

def extract_pdf_text(api_key: str, file_path: str):
    url = "https://pdf-text-extractor.p.rapidapi.com/extract_text"
    
    with open(file_path, 'rb') as file:
        files = {'file': (file_path, file, 'application/pdf')}
        
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "pdf-text-extractor.p.rapidapi.com"
        }
       
        response = requests.post(url, files=files, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

API_KEY = "0f768371d9msh8b71d92e108c519p1f2d8ejsn0ab1202db481" 
PDF_FILE = "attachments\CV_Cononciuc_Alina_Analyst_Rose_EN_1.pdf"  

result = extract_pdf_text(API_KEY, PDF_FILE)
if result:
    print("Extraction successful!")
    print(result)