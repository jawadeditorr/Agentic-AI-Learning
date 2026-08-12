#keeps log of every action
from datetime import datetime
import logging
from langchain.agents.middleware import after_model, AgentState

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@after_model
def log_agent_actions(state: AgentState) -> AgentState:
    logger.info(f"Action: {state['next_step']}")
    return state