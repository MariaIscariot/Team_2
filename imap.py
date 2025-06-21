import imaplib
import email
from email.header import decode_header
import json

class SimpleGmailLoader:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
        self.mail = None
    
    def connect(self):
        """Подключение к Gmail IMAP серверу"""
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.mail.login(self.email_address, self.password)
            print(f"Подключен к {self.email_address}")
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False
    
    def disconnect(self):
        """Отключение от сервера"""
        if self.mail:
            self.mail.close()
            self.mail.logout()
    
    def decode_mime_words(self, s):
        """Декодирование MIME заголовков"""
        if not s:
            return ""
        decoded_string = ""
        for word, encoding in decode_header(s):
            if isinstance(word, bytes):
                decoded_string += word.decode(encoding or 'utf-8')
            else:
                decoded_string += word
        return decoded_string
    
    def get_message_body(self, msg):
        """Извлечение тела сообщения"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode('utf-8')
                        break
                    except:
                        try:
                            body = part.get_payload(decode=True).decode('cp1251')
                            break
                        except:
                            body = str(part.get_payload(decode=True))
                            break
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8')
            except:
                try:
                    body = msg.get_payload(decode=True).decode('cp1251')
                except:
                    body = str(msg.get_payload(decode=True))
        
        return body
    
    def load_all_messages(self):
        """Загружает ВСЕ сообщения из INBOX и сохраняет в JSON"""
        messages = []
        
        try:
            # Выбираем папку INBOX
            status, messages_count = self.mail.select("INBOX")
            if status != 'OK':
                print("Не удалось выбрать папку INBOX")
                return []
            
            total_messages = int(messages_count[0])
            print(f"Всего сообщений в INBOX: {total_messages}")
            
            # Ищем ВСЕ сообщения
            status, message_ids = self.mail.search(None, "ALL")
            if status != 'OK':
                print("Ошибка поиска сообщений")
                return []
            
            message_ids = message_ids[0].split()
            print(f"Начинаем загрузку {len(message_ids)} сообщений...")
            
            # Обрабатываем каждое сообщение
            for i, msg_id in enumerate(message_ids):
                try:
                    print(f"Загружаем сообщение {i+1}/{len(message_ids)}")
                    
                    status, msg_data = self.mail.fetch(msg_id, "(RFC822)")
                    if status == 'OK':
                        email_body = msg_data[0][1]
                        email_message = email.message_from_bytes(email_body)
                        
                        # Извлекаем информацию
                        subject = self.decode_mime_words(email_message["Subject"])
                        sender = self.decode_mime_words(email_message["From"])
                        receiver = self.decode_mime_words(email_message["To"])
                        date = email_message["Date"]
                        body = self.get_message_body(email_message)
                        
                        message_info = {
                            "id": msg_id.decode(),
                            "subject": subject,
                            "from": sender,
                            "to": receiver,
                            "date": date,
                            "body": body
                        }
                        
                        messages.append(message_info)
                        
                except Exception as e:
                    print(f"Ошибка обработки сообщения {i+1}: {e}")
                    continue
            
            return messages
            
        except Exception as e:
            print(f"Общая ошибка загрузки: {e}")
            return []


def main():
    # Ваши данные для подключения
    EMAIL = "test.server.composer@gmail.com"
    PASSWORD = "vigd xbrg ofcp zqma"  # Пароль приложения
    
    # Создаем загрузчик
    loader = SimpleGmailLoader(EMAIL, PASSWORD)
    
    # Подключаемся
    if not loader.connect():
        print("Не удалось подключиться к Gmail")
        return
    
    try:
        # Загружаем ВСЕ сообщения
        print("Загружаем все сообщения из Gmail...")
        all_messages = loader.load_all_messages()
        
        if all_messages:
            # Сохраняем в JSON файл
            filename = "all_gmail_messages.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_messages, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ Готово! Загружено {len(all_messages)} сообщений")
            print(f"Сообщения сохранены в файл: {filename}")
        else:
            print("❌ Не удалось загрузить сообщения")
    
    finally:
        # Отключаемся
        loader.disconnect()
        print("Программа завершена")


if __name__ == "__main__":
    main()