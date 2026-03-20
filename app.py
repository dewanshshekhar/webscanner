from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def translate_with_ai(text):
    """Use GPT to translate Sanskrit text with detailed explanations"""
    
    if not client:
        return "Error: OPENAI_API_KEY not configured. Please add your API key in the environment variables."
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are an expert Sanskrit translator and spiritual scholar. 
                    
Please analyze and translate the following Sanskrit text:

"{text}"

Provide:
1. Word-by-word Sanskrit breakdown
2. English translation
3. Hindi translation
4. Detailed explanation of the meaning and spiritual significance
5. Context about where this mantra/text comes from if applicable

Format your response clearly with sections for each part. Be thorough and accurate."""
                }
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Translation Error: {str(e)}. Please check your API key configuration."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    # This endpoint receives chat messages (which may include scanned text)
    data = request.json
    messages = data.get("messages", [])
    
    last_msg = messages[-1]["content"] if messages else ""
    
    if not last_msg:
        return jsonify({
            "success": False,
            "reply": "Please provide Sanskrit text to translate."
        })
    
    # Check if text contains Sanskrit characters
    is_sanskrit = any('\u0900' <= c <= '\u097F' for c in last_msg)
    
    if not is_sanskrit:
        return jsonify({
            "success": False,
            "reply": "Please provide Sanskrit text. I can translate Sanskrit mantras, shlokas, and other texts with detailed explanations in English and Hindi."
        })
    
    # Use AI to translate
    reply = translate_with_ai(last_msg)
        
    return jsonify({
        "success": True,
        "reply": reply
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
