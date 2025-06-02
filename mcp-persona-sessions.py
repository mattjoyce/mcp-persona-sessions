#!/usr/bin/env python3
import os
import yaml
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from fastmcp.prompts.prompt import Message
from pathlib import Path
from timer import TimerManager

# Load environment variables
load_dotenv()

# Logging Setup
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, "mcp-persona-sessions.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("session_mcp")

# Load Config
config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
try:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    logger.info(f"Config loaded: {config}")
except Exception as e:
    logger.error(f"Error loading config.yaml: {e}")
    config = {}

# Initialize Server
mcp = FastMCP("Session MCP Server")

# Server Statistics
class ServerStats:
    def __init__(self):
        self.api_calls = 0
        self.resource_requests = 0
        self.tool_calls = 0
        self.errors = 0
        self.start_time = datetime.now()

    def log_status(self):
        uptime = datetime.now() - self.start_time
        logger.info(f"Uptime: {uptime}, API Calls: {self.api_calls}, Resources: {self.resource_requests}, Tools: {self.tool_calls}, Errors: {self.errors}")

stats = ServerStats()

# Initialize Timer Manager
timer_manager = TimerManager()

def validate_file_path(file_path: str) -> bool:
    """Validate file path to prevent directory traversal attacks."""
    try:
        # Resolve path and check if it's within allowed directories
        resolved = Path(file_path).resolve()
        base_dir = Path(__file__).parent.resolve()
        return str(resolved).startswith(str(base_dir))
    except Exception:
        return False

def get_persona_file(persona_file: str) -> str:
    """Returns the content of the specified persona file."""
    persona_path = config.get("persona_path", "roles")
    try:
        # Validate file path for security
        if not validate_file_path(f"{persona_path}/{persona_file}"):
            raise ValueError("Invalid file path")
            
        filepath = Path(__file__).parent / persona_path / persona_file
        return filepath.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"Error loading persona file '{persona_file}' from '{filepath}': {e}")
        return f"# Error\n\n{str(e)}"




# 🛠 Tools
@mcp.tool(name="list_session_frameworks",
          description="Browse available session frameworks and templates. Use this first to understand what types of structured sessions are available, their requirements, and expected outcomes before setting up a session.")
async def get_all_session_types() -> dict:
    session_types_file = config.get("session_types_file", "interview_types.yaml")
    path = Path(__file__).parent / session_types_file
    try:
        stats.tool_calls += 1
        types = yaml.safe_load(path.read_text(encoding="utf-8"))
        return {"session_types": types}
    except Exception as e:
        stats.errors += 1
        logger.error(f"Error loading session types: {e}")
        return {"error": str(e)}



@mcp.tool(
    name="initialize_session",
    description="Initialize a structured session with a specific persona and context. This sets up the formal session environment and should be used after gathering prerequisites and persona details. The session begins after this setup."
)
async def conduct_session(prerequisites :str, persona_content :str) -> str:
    """Loads and returns the content of the specified persona file."""
    # concatenate persona, then prerequisites, then final instructions
    try:
        stats.tool_calls += 1
        # Combine persona content with prerequisites
        combined_content = (
            f"<SESSION_LEADER>\n{persona_content}\n</SESSION_LEADER>\n\n"
            f"---\n\n"
            f"<PREREQUISITES>\n{prerequisites}\n</PREREQUISITES>\n\n"
            f"""<FINAL_INSTRUCTIONS>
            MUST Check the timer status before answering, every time.
            This is role play for you as a session leader, so set the scene and stay in character.
            Always let the participant answer the current question.
            Finally, provide the transcript of the session in markdown format, and offer to provide feedback.
            </FINAL_INSTRUCTIONS>\n\n"""
        )
        return combined_content
    except Exception as e:
        stats.errors += 1
        logger.error(f"Error conducting session: {e}")
        return f"# Error\n\n{str(e)}"


@mcp.tool(
    name="get_persona_details",
    description="Retrieve detailed information about a specific session leader persona. Use this when you need the full background, communication style, and characteristics of a persona before conducting a session."
)
async def load_persona_file(persona_file: str) -> str:
    """Loads and returns the contents of the specified persona file.  Or uses default."""
    try:
        stats.tool_calls += 1
        return get_persona_file(persona_file)
    except Exception as e:
        stats.errors += 1
        logger.error(f"Error loading persona file: {e}")
        default_file = config.get("default_persona_file", "Role-Interviewer-mcp.md")
        return get_persona_file(default_file)


@mcp.tool(
    name="assess_session_readiness",
    description="Assess what information is needed to conduct an effective session. This tool analyzes your context and either confirms you're ready to proceed or tells you what additional information to gather."
)
async def check_prerequisites() -> str:
    """Check if the prerequisites for the session are met."""
    stats.tool_calls += 1
    return """Check session types.
              Review the conversation so far.
              If you think you have enough information to conduct the session, use it to structure the prerequisites.
              Otherwise ask user for more information."""


@mcp.tool(name="start_timer", description="Start a session timer with optional target duration.")
async def start_timer(duration_minutes: int = 0, name: str = "default") -> str:
    """Start a timer with optional target duration."""
    try:
        stats.tool_calls += 1
        result = timer_manager.start(name=name, minutes=duration_minutes)
        logger.info(f"Timer '{name}' started with duration {duration_minutes} minutes")
        return f"🕒 {result} MUST check timer status often."
    except Exception as e:
        stats.errors += 1
        logger.error(f"Error starting timer: {e}")
        return f"❌ Error starting timer: {str(e)}"

@mcp.tool(name="stop_timer", description="Stop the session timer.")
async def stop_timer(name: str = "default") -> str:
    """Stop a timer and return final status."""
    try:
        stats.tool_calls += 1
        result = timer_manager.stop(name=name)
        logger.info(f"Timer '{name}' stopped")
        return f"🛑 {result} Now offer feedback and evaluation."
    except Exception as e:
        stats.errors += 1
        logger.error(f"Error stopping timer: {e}")
        return f"❌ Error stopping timer: {str(e)}"

@mcp.tool(name="check_timer_status", description="Check the current status of a running timer.")
async def check_timer_status(name: str = "default") -> str:
    """Check the status of a timer including elapsed time and progress."""
    try:
        stats.tool_calls += 1
        result = timer_manager.check(name=name)
        logger.info(f"Timer status checked for '{name}'")
        return f"⏱️ {result}"
    except Exception as e:
        stats.errors += 1
        logger.error(f"Error checking timer status: {e}")
        return f"❌ Error checking timer status: {str(e)}"

@mcp.tool(name="list_session_personas", description="Browse all available session leader personas for structured sessions. Each persona has unique expertise, communication styles, and focus areas. Use this to select the most appropriate session leader for your session.")
async def list_personas() -> Dict[str, str]:
    """List all available personas."""
    persona_path = config.get("persona_path", "roles")
    persona_dir = Path(__file__).parent / persona_path
    try:
        stats.tool_calls += 1
        personas = {f.stem: f.read_text(encoding="utf-8") for f in persona_dir.glob("*.md")}
        return personas
    except Exception as e:
        stats.errors += 1
        logger.error(f"Error listing personas: {e}")
        return {"error": str(e)}

@mcp.tool(
    name="get_session_feedback",
    description="Analyze a session transcript and receive detailed feedback on performance. The evaluator persona will assess response quality, communication effectiveness, and provide actionable improvement suggestions."
)
async def evaluate_session(transcript: str) -> str:
    """Combines the evaluator persona with the provided transcript and returns the content."""
    evaluator_file = config.get("evaluator_persona_file", "Role-Interview-Evaluator.md")
    persona_path = config.get("persona_path", "roles")
    persona_file_path = Path(__file__).parent / persona_path / evaluator_file
    try:
        stats.tool_calls += 1
        persona_content = persona_file_path.read_text(encoding="utf-8")
        
        combined_content = (
            f"{persona_content}\n\n"
            f"---\n\n"
            f"**Session Transcript:**\n\n{transcript}"
        )
        return combined_content
    except Exception as e:
        stats.errors += 1
        logger.error(f"Error loading evaluator persona file '{persona_file_path}': {e}")
        return f"# Error\n\n{str(e)}"

# Start Server
if __name__ == "__main__":
    logger.info("Starting Session MCP Server...")
    mcp.run()
