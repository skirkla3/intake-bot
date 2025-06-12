from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import openai, os, json

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.api_route("/incoming", methods=["GET", "POST"])
def incoming():
    vr = VoiceResponse()
    vr.say("This call is recorded. I am an automated assistant and cannot give legal advice.")
    g = Gather(input="speech", language="en-US",
               action="/capture", speechTimeout="auto")
    g.say("Please state your full name, phone number, and the reason for your case.")
    vr.append(g)
    vr.say("I did not receive any input. Goodbye.")
    return Response(str(vr), media_type="application/xml")

@app.post("/capture")
def capture(SpeechResult: str = Form(None)):
    prompt = "Return JSON: {full_name, phone, case_reason}"
    chat = openai.ChatCompletion.create(
        model="o3-2025-04-30",
        messages=[
            {"role":"system", "content": prompt},
            {"role":"user",   "content": SpeechResult}
        ],
        temperature=0
    )
    result = json.loads(chat.choices[0].message.content)
    print("NEW INTAKE →", result)   # shows in Render logs
    return "OK"
