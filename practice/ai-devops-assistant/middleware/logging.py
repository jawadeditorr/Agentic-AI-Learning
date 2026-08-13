#keeps log of every action
from datetime import datetime
import logging
from langchain.agents.middleware import wrap_tool_call, AgentState

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@wrap_tool_call
def logging_middleware(state):
    # tool start
    try:
        # tool success
        logger.info(f"Tool {state['next_step']} started at {datetime.now()}")
        logger.info(f"Tool {state['next_step']} ended at {datetime.now()}")
    except Exception as e:
        # tool error
        logger.error(f"Tool {state['next_step']} failed at {datetime.now()}")
        logger.error(f"Error: {str(e)}")
        