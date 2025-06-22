import sys
import json
from groq import Groq

client = Groq(
    api_key="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"
)

def main():
    if len(sys.argv) < 2:
        print("Usage: python resume.py <path_to_json_file>")
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
            "content": "You are a helpful assistant that summarizes conversations. Provide a concise summary of the following email thread."
          },
          {
            "role": "user",
            "content": user_content
          }
        ],
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    print(completion.choices[0].message.content)

if __name__ == "__main__":
    main() 