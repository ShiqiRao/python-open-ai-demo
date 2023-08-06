import requests
import json
from config import API_KEY, BOT_NAME 
from fastapi import FastAPI
from pydantic import BaseModel

class Message(BaseModel):
    content: str

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/chat")
async def chat(message: Message):
    prompt = message.content
    result = chat(prompt)
    return {"message": result}

def chat(message_content):
  url = "https://chat.openai-sb.com/api/chat"

  data = {
	"model": {
		"id": "gpt-3.5-turbo",
		"name": "GPT-3.5",
		"maxLength": 12000,
		"tokenLimit": 4000
	},
	"messages": [{
		"role": "user",
		"content": f"{message_content}"
	}],
	"key": f"{API_KEY}",
	"prompt": f'''
I'm an English learning assistant named {BOT_NAME}. My goal is to provide simple, easy to understand explanations of English vocabulary to help beginner learners improve their English skills. 
I will explain the meanings of English words using simple language that a beginner learner can understand. I use analogies, examples and clear descriptions to make my explanations intuitive. I am patient and supportive. I provide feedback to guide users to better understand the words.
''',
	"temperature": 0.5
}

  response = requests.post(url, json=data)

  return response.text