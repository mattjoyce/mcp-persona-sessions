# mcp-persona-sessions

A Model Context Protocol (MCP) server that enables AI assistants to conduct structured, persona-driven sessions including interview preparation, personal reflection, and coaching conversations.

## Overview

Transform your AI interactions with realistic persona-driven sessions. Originally designed for mock interview preparation (practice with your "new boss" before that important meeting), this MCP server has evolved into a flexible framework for guided conversations of all kinds.

Whether you're preparing for a crucial presentation, seeking structured self-reflection, or wanting to practice difficult conversations in a safe environment, this server provides the framework for meaningful, guided dialogue.

## Key Features

- 🎭 **Persona-Driven Sessions**: Load detailed persona profiles that completely transform AI behavior and expertise
- ⏱️ **Built-in Timer Management**: Track session duration with start, stop, and status checking
- 📋 **Structured Frameworks**: Pre-defined session templates with clear goals and outcomes  
- 🔄 **Adaptive Flow**: Sessions that respond to what emerges naturally in conversation
- 📊 **Session Evaluation**: Get detailed feedback on performance and communication effectiveness
- 🔒 **Secure Operation**: Safe file handling with path validation and error handling

## Session Types

### Meeting Preparation
Practice conversations with realistic personas:
- **Healthcare CIO**: Technical discussions with mission-driven leadership perspective
- **Board Members**: High-level strategic conversations
- **Team Leaders**: Collaborative planning and decision-making sessions

### Personal Reflection
Adaptive journaling sessions that flow between:
- Daily experience processing
- Creative exploration and inspiration
- Gratitude practice and appreciation
- Life pattern recognition and growth planning

### Custom Sessions
Create your own personas and session frameworks for specific needs.

## Quick Start

### Prerequisites
- Python 3.8+
- MCP-compatible AI assistant (Claude Desktop, etc.)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mattjoyce/mcp-persona-sessions.git
cd mcp-persona-sessions
```

2. Install dependencies:
```bash
pip install fastmcp
```

3. Set up configuration:
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your preferences
```

### MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "persona-sessions": {
      "command": "/path/to/venv/python",
      "args": ["/path/to/mcp-persona-sessions/mcp-persona-sessions.py"],
      "cwd": "/path/to/mcp-persona-sessions"
    }
  }
}
```

## Usage

### Basic Session Flow

I use Claude as the mcp client, you might use something else.
Simple ask claude to initiate a session.

"Claude, use your tools to run a mock meeting, this meeting is with XXX and is about YYY, duration 10 mins."
If you have useful documents, include them with the request.



## Configuration

### config.yaml

```yaml
persona_path: "roles"                           # Directory containing persona files
session_types_file: "session_types.yaml"       # Session framework definitions
default_persona_file: "Role-Interviewer-mcp.md" # Fallback persona
evaluator_persona_file: "Role-Interview-Evaluator.md" # Feedback persona
```

### Adding Custom Personas

Create a new `.md` file in the `roles/` directory with:

```markdown
# Your Persona Name

## Identity and Purpose
[Define who this persona is and their role]

## Communication Style
[How they speak and interact]

## Expertise Areas
[What they know and focus on]

## Goals
[What they aim to achieve in sessions]

[Additional sections as needed...]
```

### Adding Custom Session Types

Edit `session_types.yaml` to add new session frameworks:

```yaml
session_types:
  - name: "Your Custom Session"
    persona: "Your Persona"
    persona_file: "Role-Your-Persona.md"
    description: "What this session accomplishes"
    prerequisites: ["What's needed to start"]
    duration: 20
    topics: ["Key areas to explore"]
    goals: ["Session outcomes"]
```

## Project Structure

```
mcp-persona-sessions/
├── mcp-persona-sessions.py    # Main MCP server
├── timer.py                   # Timer management utilities
├── config.yaml               # Server configuration
├── session_types.yaml        # Available session frameworks
├── roles/                     # Persona definition files
│   ├── Role-CIO.md
│   ├── Role-Reflective-Companion.md
│   ├── Role-Interview-Evaluator.md
│   └── ...
├── requirements.txt
└── README.md
```

## Available Tools

| Tool | Purpose |
|------|---------|
| `list_session_frameworks` | Browse available session types and templates |
| `list_session_personas` | View all available personas |
| `get_persona_details` | Get full details of a specific persona |
| `assess_session_readiness` | Check if ready to start a session |
| `initialize_session` | Begin a structured session |
| `start_timer` | Start session timer with optional duration |
| `check_timer_status` | Monitor running timer progress |
| `stop_timer` | End timer and conclude session |
| `get_session_feedback` | Analyze session transcript for feedback |

## Use Cases

- **Job Interview Prep**: Practice with realistic interviewer personas
- **Presentation Rehearsal**: Get feedback on messaging and delivery
- **Difficult Conversations**: Role-play challenging workplace discussions
- **Personal Development**: Structured self-reflection and goal clarification
- **Creative Exploration**: Guided sessions for artistic and innovative thinking
- **Decision Making**: Work through complex choices with focused dialogue
- **Daily Reflection**: Consistent journaling practice with adaptive guidance

## Contributing

Contributions welcome! Areas of interest:
- New persona definitions for different roles/industries
- Additional session frameworks for specific use cases
- Enhanced timer and session management features
- Integration improvements for different MCP clients

## License

GPL-3.0 License - see LICENSE file for details.

## Acknowledgments

Built using the [Model Context Protocol](https://modelcontextprotocol.io/) framework for AI assistant extensibility.
