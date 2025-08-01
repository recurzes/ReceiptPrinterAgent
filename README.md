# Arcade AI Agent Toolkit

A Python toolkit for building AI agents powered by [Arcade AI](https://arcade.ai) tools. Extract tasks from emails, solve math problems, manage GitHub repos, and more - all through natural language.

## Features

- 🤖 **AI-Powered Agents**: Build custom agents using OpenAI models
- 🛠️ **Arcade Tools Integration**: Access 13+ external services (Gmail, GitHub, Slack, etc.)
- 📧 **Email Task Extraction**: Automatically extract actionable tasks from emails
- 🖨️ **Task Card Generation**: Create printable task cards with priorities and due dates
- 🔧 **Extensible Framework**: Easy to add new agents and capabilities

## Quick Start

### Prerequisites

- Python 3.8+
- Arcade API key ([get one here](https://arcade.ai))
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/lewis-leong/arcade-agent-toolkit.git
cd arcade-agent-toolkit

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Basic Usage

#### 1. Email Task Extraction

Extract actionable tasks from your Gmail inbox:

```bash
python agent.py
```

#### 2. AI Task Generator

Convert natural language into structured tasks:

```bash
python main.py
```

Example:
```
>> Call John about the quarterly report by Friday
✅ Generated Task: Call John - Quarterly Report Discussion
📌 Priority: HIGH
📅 Due: Friday
```

#### 3. Custom Agents with Tools

Explore available tools and create custom agents:

```bash
python tools.py
```

## Available Arcade Tools

| Tool | Description |
|------|-------------|
| 📧 **gmail** | Read, search, send, and manage Gmail messages |
| 🔢 **math** | Perform calculations and solve mathematical problems |
| 🐙 **github** | Manage repositories, issues, and pull requests |
| 💼 **linkedin** | Access professional network data |
| 💬 **slack** | Send messages and manage team communication |
| 📅 **calendar** | Schedule events and manage appointments |
| 📝 **notion** | Access workspace and knowledge management |
| ✅ **asana** | Manage projects and tasks |
| 💳 **stripe** | Handle payments and transactions |
| 🏢 **salesforce** | CRM operations and customer management |
| 🎮 **discord** | Community chat and server management |
| 🐦 **twitter** | Social media posting and engagement |
| 🛒 **shopify** | E-commerce and store management |

## Creating Custom Agents

```python
from tools import ToolkitAgent
import asyncio

async def create_productivity_agent():
    agent = ToolkitAgent(
        name="Productivity Assistant",
        toolkits=["gmail", "calendar", "asana"],
        instructions=(
            "You are a productivity assistant. Help organize work, "
            "schedule meetings, and track tasks efficiently."
        )
    )
    
    await agent.initialize()
    result = await agent.run("Check my emails for meeting requests")
    print(result)

asyncio.run(create_productivity_agent())
```

## Project Structure

```
arcade-agent-toolkit/
├── agent.py              # Email task extraction agent
├── main.py               # Simple task generator CLI
├── tools.py              # Arcade tools framework and examples
├── agent_config.py       # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── src/
    └── task_card_generator/
        ├── ai_client.py      # OpenAI integration
        ├── html_generator.py # Task card HTML generation
        ├── image_generator.py # Task card image generation
        ├── pdf_generator.py  # PDF export functionality
        └── printer.py        # Thermal printer support
```

## Configuration

Create a `.env` file with your API credentials:

```env
# Required
ARCADE_API_KEY=your_arcade_api_key
OPENAI_API_KEY=your_openai_api_key

# Optional
ARCADE_USER_ID=your_email@example.com
```

## Examples

### Email Assistant

```python
from tools import AgentExamples
import asyncio

# Check emails and extract tasks
result = asyncio.run(AgentExamples.email_assistant("user@example.com"))
```

### Math Solver

```python
# Interactive math problem solver
asyncio.run(AgentExamples.math_solver())
```

### Multi-Tool Agent

```python
# Combine multiple tools for complex workflows
agent = ToolkitAgent(
    name="Research Assistant",
    toolkits=["github", "notion", "slack"],
    instructions="Help with code research and documentation"
)
```

## Advanced Features

### Task Card Generation

The toolkit includes utilities for generating printable task cards:

- HTML-based card generation with emoji support
- PDF export for digital archiving
- Thermal printer integration (optional)

### Structured Output

Use Pydantic models for structured agent responses:

```python
from pydantic import BaseModel
from typing import List

class TaskList(BaseModel):
    tasks: List[str]
    priority: str
    estimated_hours: float

agent = ToolkitAgent(
    name="Project Planner",
    toolkits=["asana", "github"],
    instructions="Extract project tasks and estimate effort",
    output_type=TaskList
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Arcade AI](https://arcade.ai) - AI-powered tool integration platform
- Powered by [OpenAI](https://openai.com) language models
- Special thanks to the agents-arcade community

## Support

- 📖 [Arcade Documentation](https://docs.arcade.ai)
- 💬 [Discord Community](https://discord.gg/arcade-ai)
- 🐛 [Report Issues](https://github.com/lewis-leong/arcade-agent-toolkit/issues)