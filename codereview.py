import os
from fastapi import FastAPI
from openai import OpenAI

# -----------------------------
# 🔑 API KEY
# -----------------------------
os.environ["OPENAI_API_KEY"] = "k-proj-sLvZnFkHJw1yM6nP7q8_YNodyQD3UTR5cIpYJ1B8CP4O-QpTyAdhshuqtNfrco-LC3MO4Mw-Z-T3BlbkFJnSdzSGsGhwALCsTrzU4RO1GBpGWpeccUAqHNheuo9iZQAYPm99zV-yAR107YoNJyLnC1YnacEA"

client = OpenAI(api_key="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")

app = FastAPI()

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

Return JSON:
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
@app.post("/review")
def review(input: dict):
    architecture = input.get("architecture", "")
    language = input.get("language", "")
    guidelines = input.get("guidelines", "")
    code = input.get("code", "")

    if not code:
        return {"error": "Code is required"}

    result = review_code(architecture, language, guidelines, code)

    return {
        "review": result
    }