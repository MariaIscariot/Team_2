import imaplib
import email
from email.header import decode_header
import json
import time

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
    
    def load_messages_from_folder(self, folder_name):
        """Загружает все сообщения из указанной папки"""
        messages = []
        
        try:
            # Пытаемся выбрать папку с разными кодировками
            folder_to_select = folder_name
            
            # Для Gmail папок пробуем использовать UTF-7 кодировку
            if folder_name.startswith('[Gmail]'):
                try:
                    # Пробуем с кавычками
                    status, messages_count = self.mail.select(f'"{folder_name}"')
                    if status != 'OK':
                        # Пробуем без кавычек
                        status, messages_count = self.mail.select(folder_name)
                except:
                    # Пробуем альтернативные названия для Gmail папок
                    gmail_folders = {
                        '[Gmail]/All Mail': 'INBOX',  # Альтернатива
                        '[Gmail]/Sent Mail': 'INBOX.Sent',
                        '[Gmail]/Drafts': 'INBOX.Drafts',
                        '[Gmail]/Spam': 'INBOX.Spam',
                        '[Gmail]/Trash': 'INBOX.Trash'
                    }
                    if folder_name in gmail_folders:
                        try:
                            status, messages_count = self.mail.select(gmail_folders[folder_name])
                        except:
                            status = 'NO'
                    else:
                        status = 'NO'
            else:
                status, messages_count = self.mail.select(folder_name)
            
            if status != 'OK':
                print(f"Не удалось выбрать папку {folder_name} (статус: {status})")
                return []
            
            total_messages = int(messages_count[0])
            print(f"Всего сообщений в {folder_name}: {total_messages}")
            
            if total_messages == 0:
                print(f"Папка {folder_name} пуста")
                return []
            
            # Ищем ВСЕ сообщения
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

    def get_all_folders(self):
        """Получить список всех доступных папок"""
        try:
            status, folders = self.mail.list()
            if status == 'OK':
                folder_list = []
                for folder in folders:
                    try:
                        # Декодируем название папки
                        folder_str = folder.decode('utf-8')
                        # Извлекаем название папки (последняя часть в кавычках)
                        parts = folder_str.split('"')
                        if len(parts) >= 4:
                            folder_name = parts[3]
                            folder_list.append(folder_name)
                        elif len(parts) >= 2:
                            # Альтернативный формат
                            folder_name = parts[1]
                            folder_list.append(folder_name)
                    except Exception as e:
                        print(f"Ошибка декодирования папки {folder}: {e}")
                        continue
                return folder_list
            return []
        except Exception as e:
            print(f"Ошибка получения списка папок: {e}")
            return []

    def load_all_messages(self):
        """Загружает ВСЕ сообщения из ВСЕХ доступных папок"""
        all_messages = []
        
        # Получаем список всех папок
        print("🔍 Ищем все доступные папки...")
        all_folders = self.get_all_folders()
        
        print(f"📁 Найдено папок: {len(all_folders)}")
        for i, folder in enumerate(all_folders):
            print(f"   {i+1}. {folder}")
        
        # Загружаем сообщения из всех папок
        print(f"\n📥 Начинаем загрузку из {len(all_folders)} папок...")
        
        total_processed = 0
        total_saved = 0
        
        for i, folder in enumerate(all_folders):
            print(f"\n📁 [{i+1}/{len(all_folders)}] Обрабатываем папку: {folder}")
            try:
                folder_messages = self.load_messages_from_folder(folder)
                if folder_messages:
                    all_messages.extend(folder_messages)
                    total_saved += len(folder_messages)
                    print(f"✅ Сохранено {len(folder_messages)} сообщений из {folder}")
                else:
                    print(f"📭 Папка {folder} пуста или недоступна")
            except Exception as e:
                print(f"❌ Ошибка обработки папки {folder}: {e}")
                continue
        
        print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
        print(f"💾 Всего сохранено сообщений: {total_saved}")
        
        return all_messages


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
        # Загружаем ВСЕ сообщения из ВСЕХ папок
        print("Загружаем все сообщения из Gmail (из всех доступных папок)...")
        all_messages = loader.load_all_messages()
        
        if all_messages:
            # Сохраняем в JSON файл
            filename = "all_gmail_messages.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_messages, f, ensure_ascii=False, indent=2)
            
            # Показываем детальную статистику по папкам
            folder_stats = {}
            for msg in all_messages:
                folder = msg.get('folder', 'Unknown')
                folder_stats[folder] = folder_stats.get(folder, 0) + 1
            
            print(f"\n🎉 ГОТОВО! Загружено и сохранено {len(all_messages)} сообщений всего")
            print("📊 Подробная статистика по папкам:")
            for folder, count in sorted(folder_stats.items()):
                print(f"   📁 {folder}: {count} сообщений")
            print(f"\n💾 Все сообщения сохранены в файл: {filename}")
            
            # Дополнительная проверка
            print(f"\n🔍 ПРОВЕРКА: В JSON файле содержится {len(all_messages)} записей")
            
        else:
            print("❌ Не удалось загрузить сообщения")
    
    finally:
        # Отключаемся
        loader.disconnect()
        print("Программа завершена")


if __name__ == "__main__":
    main()