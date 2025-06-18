import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from server import app

client = TestClient(app)

def test_incoming_route():
    resp = client.post('/incoming')
    assert resp.status_code == 200
    assert '<Gather' in resp.text


def test_capture_no_speech():
    resp = client.post('/capture', data={'SpeechResult': ''})
    assert resp.status_code == 200
    assert 'Thank you' in resp.text
