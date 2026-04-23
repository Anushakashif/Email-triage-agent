from langgraph.graph import StateGraph, END
from agent.state import EmailState
from agent.nodes import (
    fetch_emails_node,
    classify_emails_node,
    draft_replies_node,
    create_digest_node,
)

def create_graph():
    """Create and return the email triage agent graph."""
    
    # Initialize the graph with our state
    graph = StateGraph(EmailState)
    
    # Add 4 nodes (send_approved is triggered manually via API)
    graph.add_node("fetch_emails", fetch_emails_node)
    graph.add_node("classify_emails", classify_emails_node)
    graph.add_node("draft_replies", draft_replies_node)
    graph.add_node("create_digest", create_digest_node)
    
    # Connect nodes in order
    graph.set_entry_point("fetch_emails")
    graph.add_edge("fetch_emails", "classify_emails")
    graph.add_edge("classify_emails", "draft_replies")
    graph.add_edge("draft_replies", "create_digest")
    graph.add_edge("create_digest", END)
    
    return graph.compile()

# Create graph instance
email_graph = create_graph()