from flask import Flask, request, jsonify, render_template_string, send_file
import time
import io

# File handling
import PyPDF2
import docx
import pandas as pd

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>SummarAI</title>

<style>
body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
}

/* Background image layer */
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e');
    background-size: cover;
    background-position: center;
    opacity: 0.25;   /* clean fade */
    z-index: -1;
}

.container {
    max-width: 700px;
    margin: 60px auto;
    background: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

textarea {
    width: 95%;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #ccc;
}

button {
    margin-top: 10px;
    padding: 10px 20px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
}

/* ✨ Spinner Loader */
.loader {
    display: none;
    margin-top: 20px;
}

.spinner {
    border: 5px solid #f3f3f3;
    border-top: 5px solid #667eea;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: auto;
}

@keyframes spin {
    100% { transform: rotate(360deg); }
}

.summary-box {
    margin-top: 20px;
    padding: 15px;
    background: #f0f0f0;
    border-radius: 10px;
}
</style>

<script>
function showLoader() {
    document.getElementById("loader").style.display = "block";
}
</script>

</head>

<body>

<div class="container">
<h2>🤖 SummarAI</h2>

<form method="post" enctype="multipart/form-data" onsubmit="showLoader()">

<textarea name="text" rows="5" placeholder="Enter text or upload file..."></textarea><br><br>

<input type="file" name="file"><br><br>

<button type="submit">✨ Generate Summary</button>

</form>

<!-- 🔄 LOADER -->
<div id="loader" class="loader">
    <div class="spinner"></div>
    <p>Processing your content...</p>
</div>

{% if result %}
<div class="summary-box">
<h3>✨ Smart Summary</h3>
<p>{{ result }}</p>

<a href="/download">⬇ Download Summary</a>
</div>
{% endif %}

</div>

</body>
</html>
"""

summary_store = ""

# 🧠 Smart summary logic
def summarize_text(text):
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) > 15:
        summary = ". ".join(sentences[:7])
    elif len(sentences) > 5:
        summary = ". ".join(sentences[:5])
    else:
        summary = ". ".join(sentences)

    return summary + "."


# 📄 Extract text from files
def extract_text(file):
    filename = file.filename

    if filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

    elif filename.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join([p.text for p in doc.paragraphs])

    elif filename.endswith(".csv"):
        df = pd.read_csv(file)
        return df.to_string()

    elif filename.endswith(".txt"):
        return file.read().decode("utf-8")

    return ""


@app.route("/", methods=["GET", "POST"])
def home():
    global summary_store

    if request.method == "POST":
        text = request.form.get("text")
        file = request.files.get("file")

        if file and file.filename != "":
            text = extract_text(file)

        time.sleep(2)  # ⏳ loading effect

        result = summarize_text(text)
        summary_store = result

        return render_template_string(HTML_PAGE, result=result)

    return render_template_string(HTML_PAGE)


# 🔌 API endpoint
@app.route("/api", methods=["POST"])
def api():
    data = request.get_json()
    text = data.get("text")

    summary = summarize_text(text)
    return jsonify({"summary": summary})


# ⬇ Download summary
@app.route("/download")
def download():
    global summary_store
    return send_file(
        io.BytesIO(summary_store.encode()),
        as_attachment=True,
        download_name="summary.txt"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)