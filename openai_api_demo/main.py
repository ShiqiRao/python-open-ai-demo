import requests
import json
import logging
from config import API_KEY, BOT_NAME, SLACK_BOT_TOKEN 
from fastapi import FastAPI, Request
from pydantic import BaseModel
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info("Start Verbal Victoria Backend Service")
client = WebClient(token=SLACK_BOT_TOKEN)

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

@app.post("/event")
async def handle_event(request: Request):
    event = await request.json()
    logger.info(event)
    if event["type"] == "url_verification":
        return {"challenge": event["challenge"]}
    return {"message": "ok"}

@app.get("/history/{channel_id}")
async def dm_history(channel_id):
    # Store conversation history
    conversation_history = []
    # ID of the channel you want to send the message to

    try:
        # Call the conversations.history method using the WebClient
        # conversations.history returns the first 100 messages by default
        # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
        result = client.conversations_history(channel=channel_id)

        conversation_history = result["messages"]

        # Print results
        logger.info("{} messages found in {}".format(len(conversation_history), channel_id))

    except SlackApiError as e:  
        logger.error("Error creating conversation: {}".format(e))
    return {"message": conversation_history}

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