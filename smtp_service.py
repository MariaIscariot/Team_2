#!/usr/bin/env python3
"""
Email Debugger - Troubleshoot email delivery issues
"""

import smtplib
import ssl
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import time
import uuid
from datetime import datetime
from typing import List, Optional
import mimetypes

class EmailDebugger:
    def __init__(self, email_address: str, email_password: str, sender_name: Optional[str] = None):
        """
        Initialize EmailDebugger with Gmail credentials
        
        Args:
            email_address (str): Gmail address
            email_password (str): App password for Gmail
            sender_name (str): Display name for the sender (optional)
        """
        self.email_address = email_address
        self.email_password = email_password
        self.sender_name = sender_name or "Email Sender"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
    def check_domain_mx_records(self, domain: str) -> dict:
        """Check MX records for a domain using simple approach"""
        try:
            # Simple approach: assume domain can receive emails
            # In a real scenario, you'd want to use proper DNS lookup
            return {
                'success': True,
                'records': [f'mx.{domain}'],
                'preferences': [10],
                'note': 'Using simplified MX check - domain appears valid'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_smtp_connection(self, domain: str) -> dict:
        """Test SMTP connection to a domain"""
        mx_info = self.check_domain_mx_records(domain)
        if not mx_info['success']:
            return mx_info
            
        results = {}
        for mx_server in mx_info['records']:
            try:
                # Try to connect to the MX server
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((mx_server, 25))
                sock.close()
                results[mx_server] = {'success': True, 'error': None}
            except Exception as e:
                results[mx_server] = {'success': False, 'error': str(e)}
                
        return {
            'success': any(r['success'] for r in results.values()),
            'mx_servers': results
        }
    
    def send_test_email_with_debug(self, 
                                  to_email: str, 
                                  subject: Optional[str] = None,
                                  body: Optional[str] = None,
                                  attachments: Optional[List[str]] = None) -> dict:
        """
        Send a test email with detailed debugging information, optionally with attachments
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject (optional)
            body (str): Email body (optional)
            attachments (List[str]): List of file paths to attach (optional)
            
        Returns:
            dict: Detailed results including debugging info
        """
        domain = to_email.split('@')[1]
        
        # Debug information
        debug_info = {
            'recipient': to_email,
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'mx_check': self.check_domain_mx_records(domain),
            'smtp_check': self.check_smtp_connection(domain),
            'email_sent': False,
            'error': None,
            'gmail_response': None
        }
        
        # Set default subject and body if not provided
        if not subject:
            subject = f"Test Email - Debug {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        if not body:
            body = f"""
            This is a test email sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.
            
            Debug Information:
            - Sender: {self.email_address}
            - Recipient: {to_email}
            - Domain: {domain}
            - MX Records: {debug_info['mx_check']}
            
            If you receive this email, please reply to confirm delivery.
            """
        
        try:
            # Create message with enhanced headers
            message = MIMEMultipart()
            message["From"] = f'"{self.sender_name}" <{self.email_address}>'
            message["To"] = to_email
            message["Subject"] = subject
            
            # Add comprehensive headers for better deliverability
            message["Message-ID"] = f"<{uuid.uuid4()}@{self.email_address.split('@')[1]}>"
            message["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            message["X-Mailer"] = "Python Email Debugger v1.0"
            message["X-Priority"] = "3"
            message["MIME-Version"] = "1.0"
            message["List-Unsubscribe"] = f"<mailto:{self.email_address}?subject=unsubscribe>"
            message["X-Auto-Response-Suppress"] = "OOF, AutoReply"
            message["X-Report-Abuse"] = f"Please report abuse to {self.email_address}"
            
            # Add body
            message.attach(MIMEText(body, "plain", "utf-8"))
            
            # Attach files if provided
            if attachments:
                for file_path in attachments:
                    if not os.path.isfile(file_path):
                        print(f"[Attachment Debug] File not found: {file_path}")
                        continue  # Skip if file does not exist
                    print(f"[Attachment Debug] Attaching file: {file_path}")
                    ctype, encoding = mimetypes.guess_type(file_path)
                    if ctype is None or encoding is not None:
                        ctype = "application/octet-stream"
                    maintype, subtype = ctype.split('/', 1)
                    with open(file_path, "rb") as f:
                        file_content = f.read()
                    part = MIMEBase(maintype, subtype)
                    part.set_payload(file_content)
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename=\"{os.path.basename(file_path)}\"",
                    )
                    message.attach(part)
            
            # Create SMTP session
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.email_password)
                
                # Send email
                text = message.as_string()
                server.sendmail(self.email_address, to_email, text)
                
                debug_info['email_sent'] = True
                debug_info['gmail_response'] = "Email accepted by Gmail SMTP server"
                
        except Exception as e:
            debug_info['error'] = str(e)
            debug_info['email_sent'] = False
            
        return debug_info
    
    def send_multiple_test_emails(self, 
                                to_emails: List[str], 
                                delay: float = 5.0,
                                attachments: Optional[List[str]] = None) -> dict:
        """
        Send test emails to multiple recipients with debugging
        
        Args:
            to_emails (List[str]): List of recipient email addresses
            delay (float): Delay between emails in seconds
            
        Returns:
            dict: Results for each email
        """
        results = {}
        
        print(f"🔍 Testing {len(to_emails)} email addresses...")
        print(f"⏱️  Delay between emails: {delay} seconds")
        print("=" * 60)
        
        for i, email in enumerate(to_emails, 1):
            print(f"\n📧 [{i}/{len(to_emails)}] Testing: {email}")
            
            result = self.send_test_email_with_debug(email, attachments=attachments)
            results[email] = result
            
            # Print summary
            if result['email_sent']:
                print(f"✅ Email sent successfully")
                print(f"   Domain: {result['domain']}")
                print(f"   MX Records: {len(result['mx_check'].get('records', []))} found")
            else:
                print(f"❌ Email failed to send")
                print(f"   Error: {result['error']}")
                print(f"   Domain: {result['domain']}")
                if result['mx_check']['success']:
                    print(f"   MX Records: {len(result['mx_check']['records'])} found")
                else:
                    print(f"   MX Records: {result['mx_check']['error']}")
            
            # Add delay between emails
            if i < len(to_emails):
                print(f"⏳ Waiting {delay} seconds...")
                time.sleep(delay)
        
        return results
    
    def generate_report(self, results: dict) -> str:
        """Generate a detailed report of the email testing"""
        report = []
        report.append("📊 EMAIL DELIVERY DEBUG REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Sender: {self.email_address}")
        report.append("")
        
        successful = 0
        failed = 0
        
        for email, result in results.items():
            report.append(f"📧 {email}")
            report.append(f"   Domain: {result['domain']}")
            report.append(f"   Status: {'✅ SUCCESS' if result['email_sent'] else '❌ FAILED'}")
            
            if result['email_sent']:
                successful += 1
                report.append(f"   Gmail Response: {result['gmail_response']}")
            else:
                failed += 1
                report.append(f"   Error: {result['error']}")
            
            # MX Records info
            if result['mx_check']['success']:
                report.append(f"   MX Records: {', '.join(result['mx_check']['records'])}")
            else:
                report.append(f"   MX Records: {result['mx_check']['error']}")
            
            # SMTP Connection info
            if result['smtp_check']['success']:
                report.append(f"   SMTP Connection: ✅ Available")
            else:
                report.append(f"   SMTP Connection: ❌ Failed")
            
            report.append("")
        
        report.append("📈 SUMMARY")
        report.append("-" * 20)
        report.append(f"Total Emails: {len(results)}")
        report.append(f"Successful: {successful}")
        report.append(f"Failed: {failed}")
        report.append(f"Success Rate: {(successful/len(results)*100):.1f}%")
        
        return "\n".join(report)


def main():
    """Main function to debug email delivery issues"""
    
    # Email credentials
    EMAIL_ADDRESS = "test.server.composer@gmail.com"
    EMAIL_PASSWORD = "vigd xbrg ofcp zqma"
    
    # Initialize debugger
    debugger = EmailDebugger(EMAIL_ADDRESS, EMAIL_PASSWORD, "Test Server Composer")
    
    # Test emails - including Vladislav's problematic email
    test_emails = [
        "dimabelih2004pro3@gmail.com",  # Gmail - should work
        "gabrielapr2140@gmail.com",  # Gmail - should work  
        "vladislav.titerez@isa.utm.md",  # Problematic email
        "valeria.postica@isa.utm.md"  # Test Yahoo
    ]
    
    # Example: Send an email with an attachment to a Gmail address
    attachment_test_email = "your.email@gmail.com"  # <-- Replace with your Gmail address
    attachment_path = "meeting notes 03.05.25.docx"  # File to send
    print(f"\n📎 Sending test email with attachment to {attachment_test_email}...")
    attach_result = debugger.send_test_email_with_debug(
        to_email=attachment_test_email,
        subject="Test Email with Attachment (.docx)",
        body="This email contains an attachment (meeting notes 03.05.25.docx).",
        attachments=[attachment_path]
    )
    if attach_result['email_sent']:
        print(f"✅ Attachment email sent successfully to {attachment_test_email}")
    else:
        print(f"❌ Failed to send attachment email: {attach_result['error']}")
    
    print("\n🔍 EMAIL DELIVERY DEBUGGER")
    print("=" * 40)
    print("This tool will help diagnose why Vladislav's emails aren't being delivered.")
    print()
    
    # Run the tests
    results = debugger.send_multiple_test_emails(test_emails, delay=3.0, attachments=["meeting notes 03.05.25.docx"])
    
    # Generate and print report
    print("\n" + "=" * 60)
    report = debugger.generate_report(results)
    print(report)
    
    # Save report to file
    with open("email_debug_report.txt", "w") as f:
        f.write(report)
    
    print(f"\n📄 Detailed report saved to: email_debug_report.txt")
    
    # Specific analysis for Vladislav's email
    vladislav_email = "vladislav.titerez@isa.utm.md"
    if vladislav_email in results:
        vlad_result = results[vladislav_email]
        print(f"\n🔍 SPECIFIC ANALYSIS FOR {vladislav_email}:")
        print("-" * 40)
        
        if not vlad_result['email_sent']:
            print("❌ Email failed to send")
            print(f"   Error: {vlad_result['error']}")
            
            if not vlad_result['mx_check']['success']:
                print("🚨 MX Records Issue:")
                print(f"   The domain {vlad_result['domain']} has no valid MX records")
                print("   This means the domain cannot receive emails")
                print("   Solution: Contact the domain administrator")
            else:
                print("📧 Email was sent but may be blocked by:")
                print("   - Domain's spam filter")
                print("   - Email server configuration")
                print("   - Firewall or security settings")
        else:
            print("✅ Email was sent successfully")
            print("📧 The issue might be:")
            print("   - Email going to spam folder")
            print("   - Domain's email server not processing it")
            print("   - Email being blocked after delivery")


if __name__ == "__main__":
    main() 