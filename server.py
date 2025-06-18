from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from openai import OpenAI
from relevanceai.auth import Auth
import requests
import os
import json
import logging
from urllib.parse import quote

openai_client = None
if os.getenv("OPENAI_API_KEY"):
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

rai_auth = None
if all(os.getenv(k) for k in ["RELEVANCEAI_API_KEY", "RELEVANCEAI_PROJECT", "RELEVANCEAI_REGION"]):
    try:
        rai_auth = Auth(
            api_key=os.getenv("RELEVANCEAI_API_KEY"),
            project=os.getenv("RELEVANCEAI_PROJECT"),
            region=os.getenv("RELEVANCEAI_REGION"),
        )
    except Exception as e:
        logging.error("Relevance AI auth failed", exc_info=e)

def rai_chat(prompt: str, message: str) -> str | None:
    if not rai_auth:
        return None
    try:
        resp = requests.post(
            f"{rai_auth.url}/v1/chat/completions",
            headers=rai_auth.headers,
            json={
                "project": rai_auth.project,
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message},
                ],
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error("Relevance AI error", exc_info=e)
        return None

app = FastAPI()

def _speech_url(request: Request, text: str) -> str:
    return str(request.url_for("speech")) + f"?text={quote(text)}"

@app.get("/speech")
def speech(text: str):
    if not openai_client:
        raise HTTPException(503, "OpenAI not configured")
    try:
        resp = openai_client.audio.speech.create(model="tts-1", voice="onyx", input=text)
        return Response(resp.content, media_type="audio/mpeg")
    except Exception as e:
        logging.error("TTS error", exc_info=e)
        raise HTTPException(500, "speech failed")

@app.api_route("/incoming", methods=["GET", "POST"])
def incoming(request: Request):
    vr = VoiceResponse()
    if openai_client:
        vr.play(_speech_url(request, "This call is recorded. I am an automated assistant and cannot give legal advice."))
    else:
        vr.say("This call is recorded. I am an automated assistant and cannot give legal advice.", voice="Polly.Joanna")
    g = Gather(input="speech", language="en-US", action="/capture", speechTimeout="auto", timeout=5, action_on_empty_result=True)
    if openai_client:
        g.play(_speech_url(request, "Please state your full name, phone number, and the reason for your case."))
    else:
        g.say("Please state your full name, phone number, and the reason for your case.", voice="Polly.Joanna")
    vr.append(g)
    return Response(str(vr), media_type="application/xml")

