import os
import json
import mimetypes

import pandas as pd
import fitz  # PyMuPDF
import docx
import spacy

from pathlib import Path


# === Настройка spaCy ===
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


# === Считывание текста из файлов ===
def read_pdf(path):
    try:
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()  # type: ignore
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")


def read_docx(path):
    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        raise Exception(f"Error reading DOCX file: {str(e)}")


def read_txt(path):
    try:
        # Try UTF-8 first, then fallback to other encodings
        encodings = ['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(path, "r", encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        # If all encodings fail, try with error handling
        with open(path, "r", encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        raise Exception(f"Error reading TXT file: {str(e)}")


def read_xlsx(path):
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        raise Exception(f"Error reading XLSX file: {str(e)}")


# === Определение типа документа ===
def detect_doc_type(text):
    text_lower = text.lower()
    if "curriculum vitae" in text_lower or "resume" in text_lower or "образование" in text_lower:
        return "CV"
    elif "invoice" in text_lower or "счет" in text_lower or "total" in text_lower:
        return "Invoice"
    elif "latitude" in text_lower or "longitude" in text_lower or "city" in text_lower:
        return "Analytics"
    return "Unknown"


# === Выделение сущностей ===
def extract_entities(text):
    doc = nlp(text)
    results = []
    for ent in doc.ents:
        results.append({
            "text": ent.text,
            "label": ent.label_
        })
    return results


# === Обработка файла ===
def process_file(path):
    extension = Path(path).suffix.lower()

    if extension == ".pdf":
        content = read_pdf(path)
    elif extension == ".docx":
        content = read_docx(path)
    elif extension == ".txt":
        content = read_txt(path)
    elif extension == ".xlsx":
        content = read_xlsx(path)
    else:
        raise ValueError("Неподдерживаемый формат файла.")

    return content


# === Обработка аналитики (Excel) ===
def summarize_analytics(df):
    return f"Таблица с {df.shape[0]} строками и {df.shape[1]} столбцами."


# === Преобразование к сериализуемому формату ===
def convert_for_json(obj):
    if isinstance(obj, dict):
        return {k: convert_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_for_json(i) for i in obj]
    elif isinstance(obj, (pd.Timestamp, pd.Series, pd.DataFrame)):
        return str(obj)
    elif hasattr(obj, 'isoformat'):  # datetime
        return obj.isoformat()
    elif isinstance(obj, str):
        # Ensure string is properly encoded
        try:
            return obj.encode('utf-8').decode('utf-8')
        except:
            return obj.encode('ascii', errors='ignore').decode('ascii')
    return obj


# === Сохранение результата ===
def save_to_json(filename: str, file_type: str, full_text, entities: list, summary: str):
    result = {
        "filename": filename,
        "type": file_type,
        "summary": summary,
        "entities": entities,
        "full_text": full_text
    }

    result = convert_for_json(result)

    try:
        with open("results.json", "w", encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
    except Exception as e:
        # Fallback: try with ASCII encoding
        with open("results.json", "w", encoding='ascii', errors='ignore') as f:
            json.dump(result, f, ensure_ascii=True, indent=4)


# === Главная функция ===
def main():
    try:
        # Set up proper encoding for input/output
        import sys
        import locale
        
        # Set environment variable for UTF-8 encoding
        import os
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        path = input("Введите путь к файлу (PDF, DOCX, TXT, XLSX): ").strip()

        if not os.path.exists(path):
            print("❌ Файл не найден.")
            return

        print("\n✅ Содержимое считано. Определение типа...\n")

        content = process_file(path)

        if isinstance(content, pd.DataFrame):
            text = content.to_string(index=False)
            file_type = detect_doc_type(" ".join(content.columns.tolist()))
            summary = summarize_analytics(content)
            entities = []
        else:
            text = content
            file_type = detect_doc_type(text)
            summary = f"Текст из {file_type} файла." if file_type != "Unknown" else "Общий текстовый документ."
            entities = extract_entities(text)

        print(f"📂 Тип файла: {file_type}\n")
        print("📄 Фрагмент содержимого:\n")
        print(text[:1500] + "...\n" if len(text) > 1500 else text + "\n")

        if entities:
            print("🔍 Найденные сущности:")
            for e in entities:
                # Исправлено: убрал подчеркивание
                print(f"{e['label']}: {e['text']}")

        save_to_json(path, file_type, content, entities, summary)
        print("\n💾 Результаты сохранены в results.json")
        
    except Exception as e:
        print(f"❌ Ошибка при обработке файла: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return


if __name__ == "__main__":
    main()