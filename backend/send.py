import sys
import json
from groq import Groq

client = Groq(
    api_key="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"
)

def main():
    if len(sys.argv) < 2:
        print("Usage: python send.py <path_to_json_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            message_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing JSON file: {e}")
        sys.exit(1)
        
    user_content = json.dumps(message_data, indent=2)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
          {
            "role": "system",
            "content": "\"Good Day, *name of conversation person/company*\\nI hope my message finds you well.\\n*main idea*\\n*body of response*\\n*Call to action* \\nPlease receives and give a feedback. \\nBest regards, \"\\n\\nHere it is the template of response of message what you need to post after analyses of message. Write only the what i need to send. Without message *Here is the template of response to the message.*"
          },
          {
            "role": "user",
            "content": user_content
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

if __name__ == "__main__":
    main()