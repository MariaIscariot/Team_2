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
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "Translate the following text entirely into English if needed, then summarize it using this exact structure without adding or removing anything: Topic: Key Points: Conclusion: Relevant Quotes (if applicable): respond only in English and in this structure, without extra commentary or original language."
            },
            {
                "role": "user",
                "content": json_content
            }
        ],
        temperature=0.2,
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