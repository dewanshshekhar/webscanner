from flask import Flask, render_template, request, jsonify
import os
import re

app = Flask(__name__)

# Sanskrit-English-Hindi Dictionary
SANSKRIT_DICTIONARY = {
    "ॐ": {"english": "Om", "hindi": "ओम", "meaning": "The sacred sound of the universe, representing the divine energy"},
    "शांति": {"english": "Peace/Shanti", "hindi": "शांति", "meaning": "Peace, tranquility, and harmony"},
    "शक्ति": {"english": "Strength/Shakti", "hindi": "शक्ति", "meaning": "Divine feminine energy, power, and strength"},
    "प्रेम": {"english": "Love/Prem", "hindi": "प्रेम", "meaning": "Divine love and compassion"},
    "सत्य": {"english": "Truth/Satya", "hindi": "सत्य", "meaning": "Truth, authenticity, and reality"},
    "आत्मा": {"english": "Soul/Atma", "hindi": "आत्मा", "meaning": "The eternal self or soul within all beings"},
    "मन": {"english": "Mind/Man", "hindi": "मन", "meaning": "Mind, consciousness, and intellect"},
    "हृदय": {"english": "Heart/Hridaya", "hindi": "हृदय", "meaning": "Heart, the seat of emotions and compassion"},
    "ब्रह्म": {"english": "Brahman/Brahm", "hindi": "ब्रह्म", "meaning": "The ultimate reality, universal consciousness"},
    "देव": {"english": "Divine/Dev", "hindi": "देव", "meaning": "God, divinity, celestial being"},
    "मंत्र": {"english": "Mantra/Mantr", "hindi": "मंत्र", "meaning": "Sacred sound or phrase with spiritual power"},
    "योग": {"english": "Union/Yoga", "hindi": "योग", "meaning": "Union of individual soul with universal consciousness, yoga practice"},
    "ध्यान": {"english": "Meditation/Dhyan", "hindi": "ध्यान", "meaning": "Meditation, deep concentration and contemplation"},
    "तप": {"english": "Austerity/Tap", "hindi": "तप", "meaning": "Spiritual discipline and austerity for self-purification"},
    "कर्म": {"english": "Action/Karma", "hindi": "कर्म", "meaning": "Action and its consequences, the law of cause and effect"},
    "धर्म": {"english": "Duty/Dharma", "hindi": "धर्म", "meaning": "Righteousness, duty, and cosmic order"},
    "मोक्ष": {"english": "Liberation/Moksh", "hindi": "मोक्ष", "meaning": "Liberation from the cycle of birth and death"},
    "आनंद": {"english": "Bliss/Anand", "hindi": "आनंद", "meaning": "Supreme bliss and eternal joy"},
    "गुरु": {"english": "Guru/Teacher", "hindi": "गुरु", "meaning": "Spiritual teacher and guide"},
    "नमस्ते": {"english": "Namaste", "hindi": "नमस्ते", "meaning": "Respectful greeting meaning 'I bow to you'"},
}

def extract_sanskrit_words(text):
    """Extract Sanskrit words from text"""
    sanskrit_pattern = r'[\u0900-\u097F]+'
    matches = re.findall(sanskrit_pattern, text)
    return matches

def translate_sanskrit(text):
    """Translate Sanskrit text to English and Hindi with explanations"""
    
    # Check if text contains Sanskrit characters
    is_sanskrit = any('\u0900' <= c <= '\u097F' for c in text)
    
    if not is_sanskrit:
        return None
    
    # Extract Sanskrit words
    words = extract_sanskrit_words(text)
    
    if not words:
        return None
    
    translations = []
    
    for word in words:
        if word in SANSKRIT_DICTIONARY:
            entry = SANSKRIT_DICTIONARY[word]
            translations.append({
                "sanskrit": word,
                "english": entry["english"],
                "hindi": entry["hindi"],
                "meaning": entry["meaning"]
            })
    
    return translations if translations else None

def create_translation_response(text):
    """Create a formatted response with translations"""
    
    translations = translate_sanskrit(text)
    
    if not translations:
        return "I could not detect Sanskrit text in your input. Please provide a Sanskrit mantra or text for translation."
    
    response = "## Sanskrit Translation & Analysis\n\n"
    
    for i, translation in enumerate(translations, 1):
        response += f"### Word {i}: **{translation['sanskrit']}**\n"
        response += f"**English:** {translation['english']}\n"
        response += f"**Hindi:** {translation['hindi']}\n"
        response += f"**Meaning:** {translation['meaning']}\n\n"
    
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    # This endpoint receives chat messages (which may include scanned text)
    data = request.json
    messages = data.get("messages", [])
    
    last_msg = messages[-1]["content"] if messages else ""
    
    # Process the message for translation
    reply = create_translation_response(last_msg)
    
    # If no Sanskrit was found, provide helpful guidance
    if "could not detect" in reply:
        reply += "\n\n**How to use:**\n"
        reply += "- **Scan an image:** Click the camera icon to scan Sanskrit text from an image\n"
        reply += "- **Type text:** Enter Sanskrit text directly\n"
        reply += "- **Upload image:** Click the upload icon to upload an image file\n\n"
        reply += "I can help you translate Sanskrit mantras and texts with detailed explanations in English and Hindi."
        
    return jsonify({
        "success": True,
        "reply": reply
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
