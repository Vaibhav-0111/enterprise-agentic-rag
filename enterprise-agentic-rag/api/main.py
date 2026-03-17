"""
FastAPI Backend — REST API for the multi-agent system.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any
import uvicorn
import time

from orchestrator.workflow import run_workflow

app = FastAPI(
    title="Enterprise AI API",
    description="Multi-Agent RAG platform — autonomous business intelligence",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Models ───────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    question:      str
    final_answer:  str
    sql:           Optional[str]
    analytics:     Optional[Any]
    confidence:    Optional[float]
    latency_ms:    int
    errors:        list


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "enterprise-ai"}


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    start = time.time()
    try:
        state = run_workflow(req.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    latency = int((time.time() - start) * 1000)
    confidence = None
    if state.get("critic_result"):
        confidence = state["critic_result"].get("confidence")

    return QueryResponse(
        question     = req.question,
        final_answer = state.get("final_answer", ""),
        sql          = state.get("sql_result", {}).get("sql"),
        analytics    = state.get("analytics"),
        confidence   = confidence,
        latency_ms   = latency,
        errors       = state.get("errors", []),
    )


@app.get("/agents")
def list_agents():
    return {
        "agents": [
            {"name": "Planner",       "status": "active", "file": "planner_agent.py"},
            {"name": "Retriever",     "status": "active", "file": "retriever_agent.py"},
            {"name": "SQL",           "status": "active", "file": "sql_agent.py"},
            {"name": "Analytics",     "status": "active", "file": "analytics_agent.py"},
            {"name": "Visualization", "status": "active", "file": "visualization_agent.py"},
            {"name": "Explanation",   "status": "active", "file": "explanation_critic.py"},
            {"name": "Critic",        "status": "active", "file": "explanation_critic.py"},
        ]
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
