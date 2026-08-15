#keeps log of every action
from datetime import datetime
import time
import logging
from pathlib import Path
from langchain.agents.middleware import wrap_tool_call

# setting up log directory dynamically relative to this file
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "agent_logs.log"

# setting up logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    filename=str(LOG_FILE),
    filemode='a',
    force=True
)

logger = logging.getLogger(__name__)

@wrap_tool_call
def logging_middleware(request, handler):
    # tool start
    tool_name = request.tool_call["name"]
    tool_args = request.tool_call["args"]

    logger.info(f"TOOLS | {tool_name} started")
    logger.info(f"ARGS | {tool_args} for tool {tool_name}")
    
    start_time = time.perf_counter()

    try:
        result = handler(request)
        # tool success
        logger.info(f"TOOL_RESULT | SUCCESS {tool_name} completed")
        execution_time = time.perf_counter() - start_time
        logger.info(f"EXECUTION TIME | {execution_time} seconds")
        return result
    except Exception as e:
        # tool error
        logger.error(f"TOOL_RESULT | {tool_name} ERROR")
        logger.error(f"ERROR | {e}")
        execution_time = time.perf_counter() - start_time
        logger.info(f"EXECUTION TIME | {execution_time} seconds")
        raise

