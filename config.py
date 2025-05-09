import os
from dotenv import load_dotenv
from load import load_form_sample

load_dotenv(override=True)

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")
DISPLAY_WIDTH = int(os.getenv("DISPLAY_WIDTH", 1024))
DISPLAY_HEIGHT = int(os.getenv("DISPLAY_HEIGHT", 768))
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-03-01-preview")   
ITERATIONS = int(os.getenv("ITERATIONS", 5))
WEB_URL = os.getenv("WEB_URL", "https://www.bing.com/")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# Key mapping for special keys in Playwright
KEY_MAPPING = {
    "/": "Slash", "\\": "Backslash", "alt": "Alt", "arrowdown": "ArrowDown",
    "arrowleft": "ArrowLeft", "arrowright": "ArrowRight", "arrowup": "ArrowUp",
    "backspace": "Backspace", "ctrl": "Control", "delete": "Delete", 
    "enter": "Enter", "esc": "Escape", "shift": "Shift", "space": " ",
    "tab": "Tab", "win": "Meta", "cmd": "Meta", "super": "Meta", "option": "Alt"
}

# modify this instructions if needed
INSTRUCTIONS = f"""
You are an AI agent with the ability to control a browser. 
You can control the keyboard and mouse. 
Your responsibility is to enter the all information below.
As the form has several textareas, you must input them.
Finally press a send button at the bottom of the form.

The information you need to enter is as follows:
{load_form_sample()}
"""
