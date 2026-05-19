# AI Report Generator — Backend

FastAPI backend for the AI Report Generator. Accepts a problem description and returns structured insights using LLaMA 3.1 (via Groq).

**Live:** https://ai-report-generator-backend-rlc0.onrender.com  
**Docs:** https://ai-report-generator-backend-rlc0.onrender.com/docs  

---

## Endpoint

### POST /generate-report

#### Request

```json
{
  "text": "Our checkout flow has 70% cart abandonment...",
  "type": "business"
}
```

- `type`: `business`, `technical`, or `general`  
- `text`: minimum 30 characters  

---

#### Response

```json
{
  "success": true,
  "data": {
    "summary": "...",
    "insights": ["..."],
    "risks": [
      { "issue": "...", "level": "High" }
    ],
    "recommendations": ["..."]
  }
}
```

---

## Stack

FastAPI · Python · Groq (LLaMA 3.1 8B) · Render  

---

## Run locally

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_key
```

Run the server:

```bash
uvicorn main:app --reload
```

---

## Frontend

Frontend Repo → https://github.com/DanelAdatia/ai-report-generator-frontend  
Live App → https://ai-report-generator-frontend-kappa.vercel.app
