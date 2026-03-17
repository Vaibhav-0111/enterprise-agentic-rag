"""
LangGraph Orchestrator — manages the full multi-agent workflow.
"""
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Any, Optional
from agents.planner_agent     import run_planner
from agents.retriever_agent   import run_retriever
from agents.sql_agent         import run_sql_agent
from agents.analytics_agent   import run_analytics
from agents.visualization_agent import run_visualization
from agents.explanation_critic  import run_explanation, run_critic


# ─── Shared State ─────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    question:      str
    task_graph:    Optional[dict]
    documents:     List[dict]
    sql_result:    Optional[dict]
    analytics:     Optional[dict]
    figure:        Any
    explanation:   str
    critic_result: Optional[dict]
    final_answer:  str
    errors:        List[str]


# ─── Node functions ────────────────────────────────────────────────────────────

def planner_node(state: AgentState) -> AgentState:
    try:
        state["task_graph"] = run_planner(state["question"])
    except Exception as e:
        state["errors"].append(f"Planner: {e}")
    return state


def retriever_node(state: AgentState) -> AgentState:
    try:
        state["documents"] = run_retriever(state["question"])
    except Exception as e:
        state["errors"].append(f"Retriever: {e}")
        state["documents"] = []
    return state


def sql_node(state: AgentState) -> AgentState:
    try:
        state["sql_result"] = run_sql_agent(state["question"])
    except Exception as e:
        state["errors"].append(f"SQL: {e}")
        state["sql_result"] = {"rows": [], "columns": [], "sql": "", "count": 0}
    return state


def analytics_node(state: AgentState) -> AgentState:
    sr = state.get("sql_result") or {}
    try:
        state["analytics"] = run_analytics(
            sr.get("rows", []),
            sr.get("columns", []),
            state["question"],
        )
    except Exception as e:
        state["errors"].append(f"Analytics: {e}")
        state["analytics"] = {}
    return state


def visualization_node(state: AgentState) -> AgentState:
    sr = state.get("sql_result") or {}
    try:
        state["figure"] = run_visualization(sr.get("rows", []), sr.get("columns", []))
    except Exception as e:
        state["errors"].append(f"Visualization: {e}")
        state["figure"] = None
    return state


def explanation_node(state: AgentState) -> AgentState:
    try:
        state["explanation"] = run_explanation(
            state.get("analytics", {}),
            state.get("documents", []),
            state["question"],
        )
    except Exception as e:
        state["errors"].append(f"Explanation: {e}")
        state["explanation"] = "Unable to generate explanation."
    return state


def critic_node(state: AgentState) -> AgentState:
    try:
        result = run_critic(
            state["question"],
            state.get("explanation", ""),
            state.get("analytics", {}),
        )
        state["critic_result"] = result
        # Use refined answer if critic improved it
        if result.get("refined"):
            state["final_answer"] = result["refined"]
        else:
            state["final_answer"] = state.get("explanation", "")
    except Exception as e:
        state["errors"].append(f"Critic: {e}")
        state["final_answer"] = state.get("explanation", "")
    return state


# ─── Build the Graph ───────────────────────────────────────────────────────────

def build_workflow() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("planner",       planner_node)
    graph.add_node("retriever",     retriever_node)
    graph.add_node("sql",           sql_node)
    graph.add_node("analytics",     analytics_node)
    graph.add_node("visualization", visualization_node)
    graph.add_node("explanation",   explanation_node)
    graph.add_node("critic",        critic_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner",       "retriever")
    graph.add_edge("planner",       "sql")
    graph.add_edge("retriever",     "explanation")
    graph.add_edge("sql",           "analytics")
    graph.add_edge("analytics",     "visualization")
    graph.add_edge("analytics",     "explanation")
    graph.add_edge("visualization", "explanation")
    graph.add_edge("explanation",   "critic")
    graph.add_edge("critic",        END)

    return graph.compile()


def run_workflow(question: str) -> AgentState:
    """Run the full multi-agent pipeline for a business question."""
    workflow = build_workflow()
    initial_state: AgentState = {
        "question":      question,
        "task_graph":    None,
        "documents":     [],
        "sql_result":    None,
        "analytics":     None,
        "figure":        None,
        "explanation":   "",
        "critic_result": None,
        "final_answer":  "",
        "errors":        [],
    }
    return workflow.invoke(initial_state)
