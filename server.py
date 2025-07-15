from flask import Flask, request, jsonify, send_from_directory
from docx import Document
import os, uuid

app = Flask(__name__)

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
BASE_URL     = os.getenv("BASE_URL",   "https://docx-generator.onrender.com/downloads")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def save_docx(filename: str, content: str) -> str:
    doc = Document()
    for line in content.splitlines():
        doc.add_paragraph(line)
    unique = f"{uuid.uuid4().hex}_{filename}"
    path   = os.path.join(DOWNLOAD_DIR, unique)
    doc.save(path)
    return f"{BASE_URL}/{unique}"

@app.post("/generate_docx")
def generate():
    data = request.get_json(force=True)
    url  = save_docx(data["filename"], data["content"])
    return jsonify({"url": url})

@app.get("/downloads/<path:fname>")
def fetch(fname):
    return send_from_directory(DOWNLOAD_DIR, fname, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
