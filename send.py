from groq import Groq

client = Groq(
    api_key="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"
)

completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
      {
        "role": "system",
        "content": "\"Good Day, *name of conversation person/company*\nI hope my message finds you well.\n*main idea*\n*body of response*\n*Call to action* \nPlease receives and give a feedback. \nBest regards, \"\n\nHere it is the template of response of message what you need to post after analyses of message. Write only the what i need to send. Without message *Here is the template of response to the message.*"
      },
      {
        "role": "user",
        "content": "  {\n    \"id\": \"11\",\n    \"folder\": \"INBOX\",\n    \"subject\": \"Re: Welcome message from Veltrix Foods\",\n    \"from\": \"Алина Конончук <akononciuc@gmail.com>\",\n    \"to\": \"Dimas Pro <test.server.composer@gmail.com>\",\n    \"date\": \"Sat, 21 Jun 2025 18:26:59 +0300\",\n    \"body\": \"Dear Dimas Pro,\\r\\n\\r\\nI think it's perfect!\\r\\nLet's schedule the meeting on wednesday 25.06.2025 at 4 pm.\\r\\n\\r\\nPlease let us know if this works for you.\\r\\n\\r\\nBest regards,\\r\\nMaria Iscariot\\r\\nProcurement Manager\\r\\nVeltrix Foods\\r\\n\\r\\nсб, 21 июн. 2025 г. в 18:22, Dimas Pro <test.server.composer@gmail.com>:\\r\\n>\\r\\n> Here's the response template:\\r\\n>\\r\\n> Dear Maria,\\r\\n>\\r\\n> Thank you for reaching out to NordTrail Logistics about collaborating as your logistics partner. We're excited to learn more about Veltrix Foods and explore how we can help support your expanding supply chain needs.\\r\\n>\\r\\n> To address your requests, we'd be happy to provide detailed information regarding our delivery terms and timelines, warehousing and storage solutions, handling of various types of cargo, pricing structure, potential cooperation models, and additional services such as shipment tracking, documentation support, etc.\\r\\n>\\r\\n> Here's some specific information about our services:\\r\\n>\\r\\n> - Delivery terms and timelines: We offer door-to-door delivery services, both local and international, with reliable timelines and tracking options.\\r\\n> - Warehousing and storage solutions: Our state-of-the-art warehouse facilities in Moldova offer secure storage spaces for various types of cargo, with climate control and handling equipment for fragile or perishable items.\\r\\n> - Handling of various types of cargo: Our experienced team is trained to handle a wide range of cargo types, including fragile or perishable items, using specialized equipment and procedures.\\r\\n> - Pricing structure and potential cooperation models: We offer competitive pricing and flexible cooperation models tailored to the needs of each client. Please let us know if you'd like to discuss more about this.\\r\\n> - Additional services: Our comprehensive logistics services include shipment tracking, documentation support, and customs clearance.\\r\\n>\\r\\n> We'd be delighted to send you a commercial proposal and schedule a call or meeting to discuss our services in more detail. Would you be available this week or next for a call?\\r\\n>\\r\\n> Thank you for your attention to this opportunity. We look forward to discussing how we can collaborate to meet the logistics needs of Veltrix Foods.\\r\\n>\\r\\n> Best regards,\\r\\n> Dimas Pro\\r\\n>\\r\\n>\\r\\n> On Sat, Jun 21, 2025 at 6:15 PM Алина Конончук <akononciuc@gmail.com> wrote:\\r\\n>>\\r\\n>> Dear NordTrail Logistics Team,\\r\\n>> I hope this message finds you well.\\r\\n>>\\r\\n>> My name is Maria, and I am reaching out on behalf of Veltrix Foods.\\r\\n>> As our operations continue to grow, we are currently looking for a\\r\\n>> reliable logistics partner to support our expanding supply chain\\r\\n>> needs.\\r\\n>>\\r\\n>> We are particularly interested in logistics solutions that can ensure\\r\\n>> efficient and timely delivery of goods across Moldova, including both\\r\\n>> domestic and international transportation, if available.\\r\\n>>\\r\\n>> At this stage, we would appreciate it if you could provide us with\\r\\n>> detailed information regarding:\\r\\n>>\\r\\n>> -Delivery terms and timelines (local and international)\\r\\n>> -Availability of warehousing and storage solutions\\r\\n>> -Handling of various types of cargo (including fragile or perishable items)\\r\\n>> -Pricing structure and potential cooperation models\\r\\n>> -Additional services such as shipment tracking, documentation support, etc.\\r\\n>>\\r\\n>> We would be grateful to receive your commercial proposal and are also\\r\\n>> open to scheduling a call or meeting to discuss your services further.\\r\\n>>\\r\\n>> Thank you for your time and attention. We look forward to your response.\\r\\n>>\\r\\n>> Best regards,\\r\\n>> Maria Iscariot\\r\\n>> Procurement Manager\\r\\n>> Veltrix Foods\\r\\n\"\n  }"
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