from omnidimension import Client
import os

def create_agent():
    api_key = os.environ.get("OMNIDIMENSION_API_KEY", "YOUR_API_KEY_HERE")
    client = Client(api_key)

    response = client.agent.create(
        name="Sanskrit Mantra Converter",
        welcome_message="""Hello, welcome to the Sanskrit Mantra Converter......""",
        context_breakdown=[
                    {"title": "Introduction", "body": """ Welcome the caller warmly and inquire about their specific translation needs. 'Hello, welcome to the Sanskrit Mantra Converter. How can I assist you with your translation needs today?' """ , 
                    "is_enabled" : True},
                    {"title": "Understanding Request", "body": """ Listen carefully to the caller to understand which Sanskrit mantra or line they need to be translated and into which languages (English or Hindi). Follow up with clarifying questions if needed. """ , 
                    "is_enabled" : True},
                    {"title": "Translation Process", "body": """ Identify the Sanskrit words or phrases that need translation and provide direct translations in both Hindi and English without asking the user for confirmation or additional context. """ , 
                    "is_enabled" : True},
                    {"title": "Confirmation", "body": """ Read back the translations to the caller to confirm accuracy. Ask the caller if they need further assistance or more translations. """ , 
                    "is_enabled" : True},
                    {"title": "Closing", "body": """ Thank the caller for using the Sanskrit Mantra Converter and invite them to reach out again if they need further help. 'Thank you for choosing Sanskrit Mantra Converter. If you have more translations or questions, feel free to reach out anytime.' """ , 
                    "is_enabled" : True}
        ],
        call_type="Incoming",
        transcriber={
            "provider": "Azure",
            "silence_timeout_ms": 400
        },
        model={
            "model": "gpt-4.1-mini",
            "temperature": 0.7
        },
        voice={
            "provider": "eleven_labs",
            "voice_id": "qZCqzgsdxAHYGdLgJhis"
        },
    )
    return response

if __name__ == "__main__":
    print(create_agent())
