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
    # 1) summarise
    summary_text = "Could not understand."  # default fallback
    if SpeechResult:
        prompt = "Return JSON: {full_name, phone, case_reason}"
        try:
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"system","content":prompt},
                          {"role":"user","content":SpeechResult}],
                temperature=0
            )
            summary = json.loads(chat.choices[0].message.content)
            summary_text = (
                f"Name {summary['full_name']}, phone {summary['phone']}. "
                f"Reason: {summary['case_reason']}"
            )
            print("NEW INTAKE →", summary)
        except Exception as e:
            print("OpenAI error:", e)

    # 2) tell the caller we’re done
    vr = VoiceResponse()
    vr.say("Thank you. Your information has been recorded. Goodbye.")
    return Response(str(vr), media_type="application/xml")
