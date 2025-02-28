from fastapi import FastAPI
from history_ai import history_gemini
import google.generativeai as genai
from dotenv import dotenv_values
import datetime

app = FastAPI()

getenv = dotenv_values(".env")
history = history_gemini.memory

GEMINI_API_KEY=getenv.get('GEMINI_API_KEY')
current_time = datetime.datetime.now().strftime("%H:%M")
current_date = datetime.datetime.now().strftime("%d %B %Y, %A")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables!")

@app.get("/query")
def deva_chat(request):
    user_input = request    
    if not user_input:
        return {"error": "Message cannot be empty"}
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="You are assistant of quantumdev. Your name is Deva, call me Sir."
        )
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input)
        model_response = response.text

        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [model_response]})
        
        return {"time":current_time,
                "date": current_date, 
                "question": user_input,
                "response": model_response}

    except Exception as e:
        return {"error": str(e)}
