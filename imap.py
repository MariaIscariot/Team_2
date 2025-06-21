import imaplib
import email
from email.header import decode_header
import json
import time

class SimpleGmailInboxLoader:
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
            try:
                self.mail.close()
            except:
                pass
            self.mail.logout()
    
    def decode_mime_words(self, s):
        """Декодирование MIME заголовков"""
        if not s:
            return ""
        decoded_string = ""
        for word, encoding in decode_header(s):
            if isinstance(word, bytes):
                try:
                    decoded_string += word.decode(encoding or 'utf-8')
                except:
                    decoded_string += word.decode('utf-8', errors='replace')
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
                            try:
                                body = part.get_payload(decode=True).decode('utf-8', errors='replace')
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
                    try:
                        body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
                    except:
                        body = str(msg.get_payload(decode=True))
        
        return body
    
    def load_inbox_messages(self):
        """Загружает ВСЕ сообщения только из папки INBOX"""
        messages = []
        folder_name = "INBOX"
        
        try:
            # Выбираем папку INBOX
            status, messages_count = self.mail.select(folder_name)
            
            if status != 'OK':
                print(f"Не удалось выбрать папку {folder_name} (статус: {status})")
                return []
            
            total_messages = int(messages_count[0])
            print(f"Всего сообщений в {folder_name}: {total_messages}")
            
            if total_messages == 0:
                print(f"Папка {folder_name} пуста")
                return []
            
            # Ищем ВСЕ сообщения в INBOX
            status, message_ids = self.mail.search(None, "ALL")
            if status != 'OK':
                print(f"Ошибка поиска сообщений в {folder_name}")
                return []
            
            message_ids = message_ids[0].split()
            print(f"Начинаем загрузку {len(message_ids)} сообщений из {folder_name}...")
            
            # Счетчик успешно обработанных сообщений
            processed_count = 0
            
            # Обрабатываем каждое сообщение
            for i, msg_id in enumerate(message_ids):
                try:
                    print(f"[{folder_name}] Загружаем сообщение {i+1}/{len(message_ids)}")
                    
                    status, msg_data = self.mail.fetch(msg_id, "(RFC822)")
                    if status == 'OK' and msg_data[0] is not None:
                        email_body = msg_data[0][1]
                        email_message = email.message_from_bytes(email_body)
                        
                        # Извлекаем информацию
                        subject = self.decode_mime_words(email_message.get("Subject", ""))
                        sender = self.decode_mime_words(email_message.get("From", ""))
                        receiver = self.decode_mime_words(email_message.get("To", ""))
                        date = email_message.get("Date", "")
                        body = self.get_message_body(email_message)
                        
                        message_info = {
                            "id": msg_id.decode(),
                            "folder": folder_name,
                            "subject": subject,
                            "from": sender,
                            "to": receiver,
                            "date": date,
                            "body": body
                        }
                        
                        messages.append(message_info)
                        processed_count += 1
                        
                        # Небольшая задержка для избежания перегрузки сервера
                        time.sleep(0.1)
                        
                    else:
                        print(f"Не удалось загрузить сообщение {i+1} из {folder_name}")
                        
                except Exception as e:
                    print(f"Ошибка обработки сообщения {i+1} из {folder_name}: {e}")
                    continue
            
            print(f"✅ Успешно обработано {processed_count} из {len(message_ids)} сообщений из {folder_name}")
            return messages
            
        except Exception as e:
            print(f"Общая ошибка загрузки из {folder_name}: {e}")
            return []


def main():
    # Ваши данные для подключения
    EMAIL = "test.server.composer@gmail.com"
    PASSWORD = "vigd xbrg ofcp zqma"  # Пароль приложения
    
    # Создаем загрузчик
    loader = SimpleGmailInboxLoader(EMAIL, PASSWORD)
    
    # Подключаемся
    if not loader.connect():
        print("Не удалось подключиться к Gmail")
        return
    
    try:
        # Загружаем ВСЕ сообщения только из INBOX
        print("Загружаем все сообщения из INBOX...")
        inbox_messages = loader.load_inbox_messages()
        
        if inbox_messages:
            # Сохраняем в JSON файл
            filename = "inbox_messages.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(inbox_messages, f, ensure_ascii=False, indent=2)
            
            print(f"\n🎉 ГОТОВО! Загружено и сохранено {len(inbox_messages)} сообщений из INBOX")
            print(f"💾 Все сообщения сохранены в файл: {filename}")
            
            # Дополнительная проверка
            print(f"\n🔍 ПРОВЕРКА: В JSON файле содержится {len(inbox_messages)} записей")
            
            # Показываем примеры первых нескольких сообщений
            if len(inbox_messages) > 0:
                print(f"\n📧 Примеры загруженных сообщений:")
                for i, msg in enumerate(inbox_messages[:3]):  # Показываем первые 3
                    print(f"   {i+1}. От: {msg['from']}")
                    print(f"      Тема: {msg['subject']}")
                    print(f"      Дата: {msg['date']}")
                    print()
            
        else:
            print("❌ Не удалось загрузить сообщения из INBOX")
    
    finally:
        # Отключаемся
        loader.disconnect()
        print("Программа завершена")


if __name__ == "__main__":
    main()