"""
Planner Agent — breaks complex user queries into a structured task graph.
"""
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import TypedDict, List


class TaskGraph(TypedDict):
    tasks: List[str]
    agents: List[str]
    reasoning: str


SYSTEM_PROMPT = """You are a planning agent inside a multi-agent enterprise intelligence system.

Your job: decompose the user's business question into ordered sub-tasks.
Each task maps to a specialized agent: retriever, sql, analytics, visualization, explanation.

Return a JSON object with:
- tasks: list of specific sub-tasks
- agents: which agent handles each task (same order)
- reasoning: one sentence explaining the plan

Be concise and precise. Max 6 tasks."""

USER_PROMPT = "Business question: {question}"


def run_planner(question: str, llm: ChatOpenAI = None) -> TaskGraph:
    """Decompose a business question into an ordered task graph."""
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human",  USER_PROMPT),
    ])
    chain = prompt | llm
    response = chain.invoke({"question": question})

    import json, re
    raw = response.content
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {"tasks": [raw], "agents": ["explanation"], "reasoning": "Fallback single-step plan."}
