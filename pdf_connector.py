# ============================================================
# PDF CONNECTOR — Session 6
# Watches inbox_pdfs folder for supported inbox files
# Reads them, extracts key information for the briefing
# Moves processed files to processed_pdfs folder
# ============================================================

import os
import shutil
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from docx import Document
except ImportError:
    Document = None

# PDF reading library
try:
    from PyPDF2 import PdfReader
except ImportError:
    try:
        import pypdf as PdfReader
    except ImportError:
        PdfReader = None

# ── Folder paths ─────────────────────────────────────────────

INBOX_FOLDER    = "inbox_pdfs"
PROCESSED_FOLDER= "processed_pdfs"
SUPPORTED_EXTENSIONS = {".pdf", ".csv", ".xlsx", ".txt", ".docx"}

def ensure_folders():
    """Make sure both folders exist"""
    os.makedirs(INBOX_FOLDER,     exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)


def _truncate_text(text, limit=4000):
    return text[:limit]

def extract_text_from_pdf(filepath):
    """
    Extract all text from a PDF file.
    Returns the text as a string, or an error message.
    """
    if PdfReader is None:
        return "PDF library not available. Run: pip install pypdf2"

    try:
        reader   = PdfReader(filepath)
        pages    = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())

        full_text = "\n\n".join(pages)

        if not full_text.strip():
            return "Could not extract text — PDF may be scanned or image-based"

        # Truncate very long documents — AI doesn't need everything
        return full_text[:4000]

    except Exception as e:
        return f"Error reading PDF: {e}"


def extract_text_from_csv(filepath):
    """
    Extract a concise text snapshot from a CSV file.
    """
    if pd is None:
        return "CSV support requires pandas. Run: pip install -r requirements.txt"

    try:
        dataframe = pd.read_csv(filepath)

        if dataframe.empty:
            return "CSV file is empty"

        return _truncate_text(dataframe.head(20).to_string(index=False))

    except Exception as e:
        return f"Error reading CSV: {e}"


def extract_text_from_excel(filepath):
    """
    Extract a concise text snapshot from an Excel workbook.
    """
    if pd is None:
        return "Excel support requires pandas. Run: pip install -r requirements.txt"

    try:
        workbook = pd.read_excel(filepath, sheet_name=None)

        if not workbook:
            return "Excel workbook is empty"

        sections = []
        for sheet_name, dataframe in workbook.items():
            sections.append(f"SHEET: {sheet_name}")

            if dataframe.empty:
                sections.append("(empty)")
            else:
                sections.append(dataframe.head(20).to_string(index=False))

            sections.append("")

        return _truncate_text("\n".join(sections))

    except Exception as e:
        return f"Error reading Excel file: {e}"


def extract_text_from_txt(filepath):
    """
    Extract text from a plain text file.
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as file:
            text = file.read()

        if not text.strip():
            return "Text file is empty"

        return _truncate_text(text)

    except Exception as e:
        return f"Error reading text file: {e}"


def extract_text_from_docx(filepath):
    """
    Extract text from a Word document.
    """
    if Document is None:
        return "DOCX support requires python-docx. Run: pip install -r requirements.txt"

    try:
        document = Document(filepath)
        paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]

        if not paragraphs:
            return "Word document is empty"

        return _truncate_text("\n".join(paragraphs))

    except Exception as e:
        return f"Error reading DOCX file: {e}"


def extract_text_from_file(filepath):
    """
    Read a supported inbox file and return a text summary.
    """
    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(filepath)
    if extension == ".csv":
        return extract_text_from_csv(filepath)
    if extension == ".xlsx":
        return extract_text_from_excel(filepath)
    if extension == ".txt":
        return extract_text_from_txt(filepath)
    if extension == ".docx":
        return extract_text_from_docx(filepath)

    return f"Unsupported file type: {extension}"


def get_pending_pdfs():
    """
    Scan inbox_pdfs folder for unprocessed PDF files.
    Returns list of file paths.
    """
    ensure_folders()

    pdfs = []
    for filename in os.listdir(INBOX_FOLDER):
        if filename.lower().endswith(".pdf"):
            pdfs.append(os.path.join(INBOX_FOLDER, filename))

    return pdfs


def get_pending_files():
    """
    Scan inbox_pdfs folder for supported file types.
    Returns list of file paths.
    """
    ensure_folders()

    files = []
    for filename in os.listdir(INBOX_FOLDER):
        if filename.startswith("~$"):
            continue

        extension = os.path.splitext(filename)[1].lower()
        if extension in SUPPORTED_EXTENSIONS:
            files.append(os.path.join(INBOX_FOLDER, filename))

    return files


def move_to_processed(filepath):
    """
    Move a processed PDF to the processed_pdfs folder.
    Adds timestamp to filename to avoid conflicts.
    """
    filename  = os.path.basename(filepath)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name  = f"{timestamp}_{filename}"
    dest      = os.path.join(PROCESSED_FOLDER, new_name)

    try:
        shutil.move(filepath, dest)
        return dest
    except Exception as e:
        return None


def process_all_pdfs():
    """
    Main function — processes all supported files in inbox_pdfs folder.
    Returns a list of document summaries for the AI briefing.
    """
    ensure_folders()
    pdfs = get_pending_files()

    if not pdfs:
        return []

    documents = []
    for filepath in pdfs:
        filename = os.path.basename(filepath)
        extension = os.path.splitext(filename)[1].lower().lstrip(".").upper() or "FILE"
        print(f"   📄 Reading: {filename}")

        text = extract_text_from_file(filepath)

        documents.append({
            "filename": filename,
            "type":    extension,
            "text":     text,
            "pages":    len(text) // 500 + 1  # rough page estimate
        })

        # Move to processed folder
        dest = move_to_processed(filepath)
        if dest:
            print(f"      ✅ Moved to processed_pdfs/")
        else:
            print(f"      ⚠️  Could not move file — still in inbox")

    return documents


def format_pdfs_for_ai(documents):
    """
    Format processed inbox contents into structured text
    for AI analysis in the morning briefing.
    """
    if not documents:
        return "No new documents in inbox."

    lines = []
    for i, doc in enumerate(documents, 1):
        file_type = doc.get("type", "FILE")
        lines.append(f"DOCUMENT {i}: {doc['filename']} ({file_type})")
        lines.append(f"Content:")
        lines.append(doc['text'][:2000])
        lines.append("")

    return "\n".join(lines)


# ── Standalone test ───────────────────────────────────────────

if __name__ == "__main__":
    print("📄 Inbox Connector Test")
    print(f"   Watching folder: {INBOX_FOLDER}/")
    print()

    ensure_folders()
    pdfs = get_pending_files()

    if not pdfs:
        print(f"   No supported files found in {INBOX_FOLDER}/")
        print(f"   Drop a PDF, CSV, Excel, or text file into that folder and run this again.")
    else:
        print(f"   Found {len(pdfs)} supported file(s) — processing...\n")
        documents = process_all_pdfs()

        for doc in documents:
            print(f"   📄 {doc['filename']} ({doc.get('type', 'FILE')})")
            print(f"   First 300 chars of extracted text:")
            print(f"   {doc['text'][:300]}")
            print()
