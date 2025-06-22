import imaplib
import email
from email.header import decode_header
import json
import time
import os
import re
from pathlib import Path

class SimpleGmailInboxLoader:
    def __init__(self, email_address, password, attachments_folder="attachments"):
        self.email_address = email_address
        self.password = password
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
        self.mail = None
        self.attachments_folder = attachments_folder
        
        # Создаем папку для вложений если её нет
        Path(self.attachments_folder).mkdir(exist_ok=True)
    
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
    
    def sanitize_filename(self, filename):
        """Очистка имени файла от недопустимых символов"""
        if not filename:
            return "unknown_file"
        
        # Убираем недопустимые символы для имен файлов
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip('. ')
        
        # Ограничиваем длину имени файла
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:200-len(ext)] + ext
        
        return filename if filename else "unknown_file"
    
    def save_attachment(self, part, message_id, attachment_index):
        """Сохранение вложения"""
        try:
            filename = part.get_filename()
            if filename:
                filename = self.decode_mime_words(filename)
                filename = self.sanitize_filename(filename)
            else:
                # Если имя файла не указано, создаем его на основе типа содержимого
                content_type = part.get_content_type()
                ext = content_type.split('/')[-1] if '/' in content_type else 'bin'
                filename = f"attachment_{attachment_index}.{ext}"
            
            # Создаем уникальное имя файла для избежания конфликтов
            base_filename = filename
            counter = 1
            while os.path.exists(os.path.join(self.attachments_folder, filename)):
                name, ext = os.path.splitext(base_filename)
                filename = f"{name}_{counter}{ext}"
                counter += 1
            
            filepath = os.path.join(self.attachments_folder, filename)
            
            # Сохраняем файл
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))
            
            print(f"    💾 Сохранено вложение: {filename}")
            return filepath
        
        except Exception as e:
            print(f"    ❌ Ошибка сохранения вложения: {e}")
            return None
    
    def get_message_body_and_attachments(self, msg, message_id):
        """Извлечение тела сообщения и обработка вложений"""
        body = ""
        attachments = []
        attachment_index = 0
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Обрабатываем текстовую часть
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode('utf-8')
                    except:
                        try:
                            body = part.get_payload(decode=True).decode('cp1251')
                        except:
                            try:
                                body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                            except:
                                body = str(part.get_payload(decode=True))
                
                # Обрабатываем вложения
                elif "attachment" in content_disposition or part.get_filename():
                    attachment_index += 1
                    filepath = self.save_attachment(part, message_id, attachment_index)
                    if filepath:
                        attachments.append({
                            "filename": os.path.basename(filepath),
                            "filepath": filepath,
                            "content_type": content_type,
                            "size": len(part.get_payload(decode=True)) if part.get_payload(decode=True) else 0
                        })
        else:
            # Для не-multipart сообщений
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
        
        # Добавляем информацию о вложениях в тело сообщения
        if attachments:
            body += "\n\n📎 ВЛОЖЕНИЯ:\n"
            for att in attachments:
                size_kb = att['size'] / 1024 if att['size'] > 0 else 0
                body += f"  • {att['filename']} ({size_kb:.1f} KB)\n"
                body += f"    Путь: {att['filepath']}\n"
                body += f"    Тип: {att['content_type']}\n"
        
        return body, attachments
    
    def load_inbox_messages(self):
        """Загружает ВСЕ сообщения только из папки INBOX с вложениями"""
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
            
            # Счетчики
            processed_count = 0
            total_attachments = 0
            
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
                        
                        # Извлекаем тело сообщения и обрабатываем вложения
                        body, attachments = self.get_message_body_and_attachments(email_message, msg_id.decode())
                        
                        message_info = {
                            "id": msg_id.decode(),
                            "folder": folder_name,
                            "subject": subject,
                            "from": sender,
                            "to": receiver,
                            "date": date,
                            "body": body,
                            "attachments_count": len(attachments),
                            "attachments": attachments
                        }
                        
                        messages.append(message_info)
                        processed_count += 1
                        total_attachments += len(attachments)
                        
                        if attachments:
                            print(f"    📎 Найдено {len(attachments)} вложений")
                        
                        # Небольшая задержка для избежания перегрузки сервера
                        time.sleep(0.1)
                        
                    else:
                        print(f"Не удалось загрузить сообщение {i+1} из {folder_name}")
                        
                except Exception as e:
                    print(f"Ошибка обработки сообщения {i+1} из {folder_name}: {e}")
                    continue
            
            print(f"✅ Успешно обработано {processed_count} из {len(message_ids)} сообщений из {folder_name}")
            print(f"📎 Всего загружено вложений: {total_attachments}")
            return messages
            
        except Exception as e:
            print(f"Общая ошибка загрузки из {folder_name}: {e}")
            return []


def main():
    """Главная функция для выполнения скрипта"""
    credentials_file = 'credentials.json'
    output_file = 'inbox_messages_with_attachments.json'
    
    # Загружаем данные из файла
    try:
        with open(credentials_file, 'r') as f:
            credentials = json.load(f)
        
        email_address = credentials.get("email")
        password = credentials.get("password")
        attachments_folder = credentials.get("attachments_folder", "attachments")
        
        if not email_address or not password:
            print("❌ Ошибка: email и password должны быть указаны в credentials.json")
            return
            
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл {credentials_file} не найден. Создайте его с вашими данными.")
        return
    except json.JSONDecodeError:
        print(f"❌ Ошибка: Неверный формат JSON в файле {credentials_file}.")
        return

    # Создаем экземпляр класса и запускаем загрузку
    loader = SimpleGmailInboxLoader(email_address, password, attachments_folder)
    
    if loader.connect():
        messages = loader.load_inbox_messages()
        loader.disconnect()
        
        # Сохраняем сообщения в JSON файл
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            print(f"✅ Все сообщения ({len(messages)}) были успешно сохранены в {output_file}")
        except Exception as e:
            print(f"❌ Ошибка сохранения сообщений в файл: {e}")


if __name__ == "__main__":
    main()