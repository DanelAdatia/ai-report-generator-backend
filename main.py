from fastapi import FastAPI
from groq import Groq
import json
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.get("/")
def home():
    return {"message": "Backend running 🚀"}


@app.post("/generate-report")
def generate_report(data: dict):
    try:
        text = data.get("text")
        report_type = data.get("type", "business")

        # Input validation
        if not text or len(text.strip()) < 30:
            return {
                "success": False,
                "error": "Please enter a meaningful problem description"
            }

        # Smart modes
        if report_type == "business":
            role = "business analyst"
            focus = "revenue, operations, customer impact"
        elif report_type == "technical":
            role = "software architect"
            focus = "system performance, scalability, technical risks"
        else:
            role = "general analyst"
            focus = "overall situation and practical insights"

        # Prompt
        prompt = f"""
            You are a senior {role}.

            Provide deep, realistic insights. Avoid generic or vague responses.

            Analyze with focus on: {focus}

            Return ONLY valid JSON.

            Format:
            {{
            "summary": "string",
            "insights": ["string"],
            "risks": [
                {{ "issue": "string", "level": "High | Medium | Low" }}
            ],
            "recommendations": ["string"]
            }}

            Rules:
            - Only analyze real-world, professional, or meaningful problems
            - If input is inappropriate, offensive, nonsensical, or irrelevant:
            return EXACTLY this JSON:

            {{
            "summary": "Input not suitable for analysis",
            "insights": [],
            "risks": [],
            "recommendations": ["Provide a clear and professional problem description"]
            }}

            - Do not include any explanations outside JSON
            - Avoid generic statements

            Input:
            {text}
            """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()

        if not content.endswith("}"):
            content += "}"

        try:
            parsed = json.loads(content)
            return {
                "success": True,
                "data": parsed
            }
        except:
            return {
                "success": False,
                "error": "AI returned invalid format",
                "raw": content
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }