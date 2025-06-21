import json
from groq import Groq

# Read JSON content from file
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file_path}'.")
        return None

# Initialize Groq client
client = Groq(
    api_key="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"
)

# Specify your JSON file path
json_file_path = "results.json"  # Replace with your actual file path

# Read JSON data from file
json_data = read_json_file(json_file_path)

if json_data:
    # Convert JSON data to string for the API call
    json_content = json.dumps(json_data, ensure_ascii=False, indent=2)
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Analyze this JSON file and provide only the analysis content. First determine what type of file this represents from these categories: CSV of statistics, PDF file of information (which could be a CV, informational document, etc.), or document like PDF. If it's an invoice, analyze it in invoice style. Then provide a concise analysis of the content without any introductory phrases, categorization statements, or AI explanatory text. Start directly with the analysis."
            },
            {
                "role": "user",
                "content": json_content
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    # If streaming, iterate over the chunks
    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")
else:
    print("Failed to read JSON file. Please check the file path and format.")