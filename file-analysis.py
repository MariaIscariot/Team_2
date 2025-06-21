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
                "content": "Analyze this JSON file and provide only the analysis content. First determine what type of file this represents from these categories: CSV of statistics, PDF file of information (which could be a CV, informational document, etc.)CV you need to analyses based on this template \"Orange Moldovais part of Orange Group with a total customer base of 252 million customers on 5 continents. Our mission is to be always in touch to connect what’s essential in our clients’ life and to offer a unique experience to each client.\n\nOrange Moldova is looking for a new colleague to fill in the position of Finance Data Solutions Analyst.\nThe objective of the job is to play a pivotal part in transforming our finance operations through automation and digitalization initiatives. You will be responsible for identifying opportunities, implementing solutions, and driving efficiency and improvements.\n\nwhat you will be doing:\n\nconduct a detailed examination of every aspect of our finance flows and collaborate with cross-functional teams, collect and analyze relevant data to identify bottlenecks, inefficiencies, weaknesses, and opportunities for optimization\nidentify areas where automation and digitization can bring efficiencies, cost savings, and process improvements\nprepare \"as-is\" and “to-be” analysis and present it to the stakeholders\ncollaborate with internal and /or Group teams for the redesign and optimization of processes and tools\nprepare functional and user specifications\nplan and implement optimization projects, ensuring they are delivered on time and within budget\nbuild some automations and reports independently\nmonitor and report progress to management and other involved stakeholders\nprovide training and guidance to team members and end-users on new automation tools and processes\nwhat we are looking for:\n\nbachelor's degree in a relevant field (e.g., Information Technology, Finance, Accounting, Supply Chain Management, Business Administration); a master's degree is a plus\nstrong understanding of operations and best practices in finance\nproven experience in automation, process improvement, and digitization projects\nproficiency in automation tools and technologies, such as RPA platforms, data analytics (Excel, Power Query, VBA, etc.), and workflow automation\nexperience in using specific software tools, such as ERP, WMS, TMS and visualization tools (Power BI, Qlik view, etc.)\nproject management skills\nstrong analytical and data interpretation skills\neffective communication skills and the ability to collaborate with cross-functional teams\nresults-driven mindset with a focus on delivering measurable business improvements\ncreativity, actively seek to improve, offer new and different options to solve problems, think “outside the box”, take an interest in new ideas and new ways of doing things\ngood knowledge of Business English\nWe invite you to join Orange for a unique learning and working experience, with great potential for growth in an innovative environment.\n\nWorking for Orange is one of a kind experience. Come check it out!\nOrange Moldova\nStr. Alba Iulia 75, Chişinău, Moldova\" , or document like PDF. If it's an invoice, analyze it in invoice style. Then provide a concise analysis of the content without any introductory phrases, categorization statements, or AI explanatory text. Start directly with the analysis."
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