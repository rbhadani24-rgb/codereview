import os
from fastapi import FastAPI
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
# -----------------------------
# 🔑 API KEY
# -----------------------------
#os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"

client = OpenAI()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------
# 🧠 PROMPT BUILDER (UPDATED)
# -----------------------------
def build_prompt(architecture, language, guidelines, code):
    return f"""
You are a senior software architect.

Review the code based on the following architecture requirements.
Architecture:
{architecture}

Programming Language:
{language}

Guidelines:
{guidelines}

Tasks:
1. Check if code follows architecture
2. Identify bugs
3. Identify performance issues
4. Identify security risks
5. Suggest improvements

Return ONLY valid JSON. 
Do not add explanation, text, or markdown.
{{
  "architecture_issues": [],
  "bugs": [],
  "performance": [],
  "security": [],
  "suggestions": []
}}

Code:
{code}
"""

# -----------------------------
# 🤖 AI CALL
# -----------------------------
def review_code(architecture, language, guidelines, code):
    prompt = build_prompt(architecture, language, guidelines, code)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# -----------------------------
# 🌐 API
# -----------------------------
import json
import re

@app.post("/review")
def review(input: dict):
    result = review_code(
        input.get("architecture", ""),
        input.get("language", ""),
        input.get("guidelines", ""),
        input.get("code", "")
    )

    print("AI RAW OUTPUT:", result)

    try:
        # Remove markdown if present
        cleaned = re.sub(r"```json|```", "", result).strip()

        return json.loads(cleaned)

    except Exception as e:
        return {
            "error": "Invalid AI response",
            "raw_output": result
        }
    
from fastapi.staticfiles import StaticFiles
# Serve frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
