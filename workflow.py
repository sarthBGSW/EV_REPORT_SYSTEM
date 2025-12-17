import sys
import os
from dotenv import load_dotenv

# Load environment variables BEFORE importing modules that need them
load_dotenv()
print(f"[WORKFLOW] Environment loaded. AZURE_OPENAI_KEY present: {bool(os.getenv('AZURE_OPENAI_KEY'))}", file=sys.stderr)

from langgraph.graph import StateGraph, END
from modules.state import AgentState
from modules.agents import planner_agent, researcher_agent, writer_agent, reviewer_agent

print("[WORKFLOW] Initializing workflow graph...", file=sys.stderr)

__all__ = ['app_graph', 'workflow', 'should_continue']

def should_continue(state):
    current = state["current_chapter_index"]
    total = len(state["outline"])
    print(f"[WORKFLOW] Chapter progress: {current}/{total}", file=sys.stderr)
    
    if current >= total:
        print(f"[WORKFLOW] All chapters complete! Stopping workflow.", file=sys.stderr)
        return END
    
    print(f"[WORKFLOW] Continuing to next chapter: {state['outline'][current]}", file=sys.stderr)
    return "research"

try:
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("planner", planner_agent)
    workflow.add_node("research", researcher_agent)
    workflow.add_node("write", writer_agent)
    workflow.add_node("review", reviewer_agent)

    # Add Edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "research")
    workflow.add_edge("research", "write")
    workflow.add_edge("write", "review")

    # Conditional Edge: If chapters remain, go back to research, else End
    workflow.add_conditional_edges("review", should_continue, {
        "research": "research",
        END: END
    })

    app_graph = workflow.compile()
    print("[WORKFLOW] ✓ Workflow graph compiled successfully", file=sys.stderr)
    
except Exception as e:
    print(f"[WORKFLOW ERROR] Failed to compile graph: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    raise