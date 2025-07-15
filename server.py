from flask import Flask, request, jsonify, send_from_directory
from docx import Document
import os, uuid

app = Flask(__name__)

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def save_docx(filename: str, content: str) -> str:
    doc = Document()
    for line in content.splitlines():
        doc.add_paragraph(line)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    path = os.path.join(DOWNLOAD_DIR, unique_name)
    doc.save(path)
    return unique_name  # chỉ trả về tên file

@app.route("/generate_docx", methods=["POST"])
def generate_docx():
    data = request.get_json(force=True)
    unique = save_docx(data["filename"], data["content"])
    # Tự động lấy domain + /downloads
    base = request.url_root.rstrip('/')         # e.g. "https://docx-generator-3wju.onrender.com"
    download_url = f"{base}/downloads/{unique}"
    return jsonify({"url": download_url}), 200

@app.route("/downloads/<path:fname>", methods=["GET"])
def fetch(fname):
    return send_from_directory(DOWNLOAD_DIR, fname, as_attachment=True)
