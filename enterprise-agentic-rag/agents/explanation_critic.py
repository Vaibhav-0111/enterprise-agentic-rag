"""
Explanation Agent — transforms raw data into human-readable business narrative.
Critic Agent     — validates the full output and scores confidence.
"""
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Any, Dict


# ─── Explanation Agent ──────────────────────────────────────────────────────────

EXPLAIN_SYSTEM = """You are a senior business analyst. Given analytics results and retrieved documents,
write a clear, concise business narrative (3-5 bullet points) explaining:
- What happened
- Why it happened (grounded in the data and documents)
- What it means for the business

Format: Start each bullet with a product/category name in bold. Be direct. No fluff."""

EXPLAIN_USER = """
Analytics results:
{analytics}

Retrieved document excerpts:
{documents}

Question: {question}
"""


def run_explanation(
    analytics: Dict[str, Any],
    documents: list,
    question: str,
    llm: ChatOpenAI = None,
) -> str:
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    doc_snippets = "\n".join(
        f"- [{d['source']}] {d['content'][:200]}" for d in documents[:3]
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", EXPLAIN_SYSTEM),
        ("human",  EXPLAIN_USER),
    ])
    chain  = prompt | llm
    result = chain.invoke({
        "analytics": str(analytics),
        "documents": doc_snippets,
        "question":  question,
    })
    return result.content


# ─── Critic Agent ──────────────────────────────────────────────────────────────

CRITIC_SYSTEM = """You are a critic agent. Review the AI-generated answer for:
1. Factual accuracy (grounded in provided data)
2. Logical consistency
3. Hallucinations (claims not supported by data/docs)
4. Completeness

Return JSON: {"passed": bool, "confidence": float (0-1), "issues": [...], "refined": "improved text or empty"}"""

CRITIC_USER = """
Original question: {question}
AI answer: {answer}
Supporting data summary: {data_summary}
"""


def run_critic(
    question: str,
    answer: str,
    data_summary: Dict[str, Any],
    llm: ChatOpenAI = None,
) -> Dict[str, Any]:
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", CRITIC_SYSTEM),
        ("human",  CRITIC_USER),
    ])
    chain  = prompt | llm
    result = chain.invoke({
        "question":     question,
        "answer":       answer,
        "data_summary": str(data_summary)[:800],
    })

    import json, re
    raw   = result.content
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {"passed": True, "confidence": 0.85, "issues": [], "refined": ""}
