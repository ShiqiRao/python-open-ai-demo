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
  url = "https://api.openai.com/v1/chat/completions"

  data = {
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }

  response = requests.post(url, json=data, headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
  return response.json().get("choices")[0].get("message").get("content")