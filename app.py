from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    # This endpoint receives chat messages (which may include scanned text)
    data = request.json
    messages = data.get("messages", [])
    
    # In a full production app, this would forward the conversation to an LLM
    # like OpenAI GPT-4 or the real omnidimension text integration.
    # For now, we simulate an intelligent agent response.
    
    last_msg = messages[-1]["content"] if messages else ""
    
    # Simple logic to simulate agent
    is_sanskrit = any('\u0900' <= c <= '\u097F' for c in last_msg)
    
    if is_sanskrit or "scan" in last_msg.lower():
        reply = "यह एक संस्कृत मंत्र है। (This is a Sanskrit mantra.)\n\n**English Meaning**: Let peace be everywhere.\n**Hindi Meaning**: हर जगह शांति हो।"
    else:
        reply = "Thank you for reaching out to the Sanskrit Mantra Converter! How can I help you today? You can type a mantra or scan an image."
        
    return jsonify({
        "success": True,
        "reply": reply
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
