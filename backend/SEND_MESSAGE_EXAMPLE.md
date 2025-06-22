# Send Message Endpoint Documentation

## Overview
The `/send-message` endpoint allows you to send emails to multiple recipients using the SMTP service.

## Endpoint
- **URL**: `POST /send-message`
- **Content-Type**: `application/json`

## Request Body
```json
{
  "recipients": ["email1@example.com", "email2@example.com"],
  "message": "Your message content here"
}
```

### Fields
- `recipients` (array, required): List of email addresses to send the message to
- `message` (string, required): The message content to send

## Response

### Success (200)
All emails sent successfully:
```json
{
  "message": "Email sending completed. 2 successful, 0 failed.",
  "total_recipients": 2,
  "successful_sends": 2,
  "failed_sends": 0,
  "results": {
    "email1@example.com": {
      "recipient": "email1@example.com",
      "domain": "example.com",
      "timestamp": "2024-01-15T10:30:00",
      "email_sent": true,
      "gmail_response": "Email accepted by Gmail SMTP server"
    },
    "email2@example.com": {
      "recipient": "email2@example.com",
      "domain": "example.com",
      "timestamp": "2024-01-15T10:30:05",
      "email_sent": true,
      "gmail_response": "Email accepted by Gmail SMTP server"
    }
  }
}
```

### Partial Success (207)
Some emails failed to send:
```json
{
  "message": "Email sending completed. 1 successful, 1 failed.",
  "total_recipients": 2,
  "successful_sends": 1,
  "failed_sends": 1,
  "results": {
    "email1@example.com": {
      "recipient": "email1@example.com",
      "domain": "example.com",
      "timestamp": "2024-01-15T10:30:00",
      "email_sent": true,
      "gmail_response": "Email accepted by Gmail SMTP server"
    },
    "invalid@example.com": {
      "recipient": "invalid@example.com",
      "domain": "example.com",
      "timestamp": "2024-01-15T10:30:05",
      "email_sent": false,
      "error": "Connection timeout"
    }
  }
}
```

### Error (400/500)
```json
{
  "error": "Missing 'recipients' field"
}
```

## Examples

### cURL Example
```bash
curl -X POST http://localhost:5000/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": ["user1@example.com", "user2@example.com"],
    "message": "Hello! This is a test message from the API."
  }'
```

### JavaScript Example
```javascript
const response = await fetch('http://localhost:5000/send-message', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    recipients: ['user1@example.com', 'user2@example.com'],
    message: 'Hello! This is a test message from the API.'
  })
});

const result = await response.json();
console.log(result);
```

### Python Example
```python
import requests

data = {
    "recipients": ["user1@example.com", "user2@example.com"],
    "message": "Hello! This is a test message from the API."
}

response = requests.post(
    "http://localhost:5000/send-message",
    json=data,
    headers={"Content-Type": "application/json"}
)

result = response.json()
print(result)
```

## Error Codes
- `400`: Bad Request (missing fields, invalid email format)
- `415`: Unsupported Media Type (wrong Content-Type)
- `500`: Internal Server Error (SMTP errors, etc.)
- `207`: Multi-Status (partial success)

## Notes
- Emails are sent with a 2-second delay between each recipient to avoid rate limiting
- The endpoint uses the hardcoded Gmail credentials from the application
- Each email includes debug information and delivery status
- Invalid email addresses will be rejected before sending 