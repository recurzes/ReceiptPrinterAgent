#!/usr/bin/env python3
"""Arcade AI tools configuration and examples."""

import asyncio
from typing import List, Dict, Any, Optional
from agents import Agent, Runner
from agents_arcade import get_arcade_tools
from arcadepy import AsyncArcade
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()


# Available Arcade toolkits
AVAILABLE_TOOLKITS = {
    "gmail": "📧 Read, search, send, and manage Gmail messages",
    "math": "🔢 Perform calculations and solve mathematical problems",
    "github": "🐙 Manage repositories, issues, and pull requests",
    "linkedin": "💼 Access professional network data",
    "slack": "💬 Send messages and manage team communication",
    "calendar": "📅 Schedule events and manage appointments",
    "notion": "📝 Access workspace and knowledge management",
    "asana": "✅ Manage projects and tasks",
    "stripe": "💳 Handle payments and transactions",
    "salesforce": "🏢 CRM operations and customer management",
    "discord": "🎮 Community chat and server management",
    "twitter": "🐦 Social media posting and engagement",
    "shopify": "🛒 E-commerce and store management",
}


class ToolkitAgent:
    """Generic agent that can use any combination of Arcade toolkits."""
    
    def __init__(
        self,
        name: str,
        toolkits: List[str],
        instructions: str,
        model: str = "gpt-4o-mini",
        output_type: Optional[type[BaseModel]] = None
    ):
        """
        Initialize a toolkit agent.
        
        Args:
            name: Agent name
            toolkits: List of toolkit names to use
            instructions: Agent instructions
            model: AI model to use
            output_type: Optional Pydantic model for structured output
        """
        self.name = name
        self.toolkits = toolkits
        self.instructions = instructions
        self.model = model
        self.output_type = output_type
        self.client = None
        self.agent = None
    
    async def initialize(self):
        """Initialize the agent with Arcade tools."""
        self.client = AsyncArcade()
        tools = await get_arcade_tools(self.client, toolkits=self.toolkits)
        
        self.agent = Agent(
            name=self.name,
            instructions=self.instructions,
            model=self.model,
            tools=tools,
            output_type=self.output_type,
        )
    
    async def run(self, input_text: str, context: Optional[Dict[str, Any]] = None):
        """Run the agent with the given input."""
        if not self.agent:
            await self.initialize()
        
        result = await Runner.run(
            starting_agent=self.agent,
            input=input_text,
            context=context or {},
        )
        
        return result.final_output if self.output_type else result.messages[-1].content


# Example agent configurations
class AgentExamples:
    """Pre-configured agent examples for common use cases."""
    
    @staticmethod
    async def email_assistant(user_email: Optional[str] = None):
        """Email management assistant."""
        agent = ToolkitAgent(
            name="Email Assistant",
            toolkits=["gmail"],
            instructions=(
                "You are an email assistant. Help manage emails, "
                "extract important information, and identify action items. "
                "Always prioritize urgent messages and provide clear summaries."
            )
        )
        
        await agent.initialize()
        result = await agent.run(
            "Check my recent emails and summarize the important ones",
            context={"user_id": user_email} if user_email else {}
        )
        return result
    
    @staticmethod
    async def math_solver():
        """Mathematical problem solver."""
        agent = ToolkitAgent(
            name="Math Solver",
            toolkits=["math"],
            instructions=(
                "You are a mathematical assistant. Solve equations, "
                "perform calculations, and explain mathematical concepts clearly."
            )
        )
        
        await agent.initialize()
        
        # Interactive math solver
        print("Math Solver Ready! (type 'quit' to exit)")
        while True:
            problem = input("\nEnter math problem: ")
            if problem.lower() in ['quit', 'exit']:
                break
            
            result = await agent.run(problem)
            print(f"Solution: {result}")
    
    @staticmethod
    async def github_manager(repo: str):
        """GitHub repository manager."""
        agent = ToolkitAgent(
            name="GitHub Manager",
            toolkits=["github"],
            instructions=(
                "You are a GitHub repository manager. Help with issues, "
                "pull requests, and code management. Provide clear status updates."
            )
        )
        
        await agent.initialize()
        result = await agent.run(
            f"Show me the open issues and recent activity for {repo}"
        )
        return result
    
    @staticmethod
    async def multi_tool_assistant():
        """Multi-tool assistant combining email, calendar, and tasks."""
        agent = ToolkitAgent(
            name="Productivity Assistant",
            toolkits=["gmail", "calendar", "asana"],
            instructions=(
                "You are a productivity assistant with access to email, calendar, "
                "and task management. Help organize work, schedule meetings, "
                "and track tasks efficiently."
            )
        )
        
        await agent.initialize()
        result = await agent.run(
            "Check my emails for meeting requests and help me schedule them"
        )
        return result


async def list_available_tools():
    """List all available Arcade toolkits."""
    print("=" * 60)
    print("AVAILABLE ARCADE TOOLKITS")
    print("=" * 60)
    
    for toolkit, description in AVAILABLE_TOOLKITS.items():
        print(f"{description}")
        print(f"   Toolkit name: '{toolkit}'")
        print()


async def create_custom_agent():
    """Interactive custom agent creator."""
    print("=" * 60)
    print("CREATE CUSTOM AGENT")
    print("=" * 60)
    
    # Get agent name
    name = input("\nAgent name: ")
    
    # Select toolkits
    print("\nAvailable toolkits:")
    for i, (toolkit, desc) in enumerate(AVAILABLE_TOOLKITS.items(), 1):
        print(f"{i}. {toolkit}: {desc}")
    
    toolkit_nums = input("\nSelect toolkits (comma-separated numbers): ")
    selected_toolkits = []
    toolkit_list = list(AVAILABLE_TOOLKITS.keys())
    
    for num in toolkit_nums.split(','):
        try:
            idx = int(num.strip()) - 1
            if 0 <= idx < len(toolkit_list):
                selected_toolkits.append(toolkit_list[idx])
        except ValueError:
            pass
    
    if not selected_toolkits:
        print("No valid toolkits selected!")
        return
    
    print(f"\nSelected toolkits: {', '.join(selected_toolkits)}")
    
    # Get instructions
    print("\nEnter agent instructions (end with empty line):")
    instructions_lines = []
    while True:
        line = input()
        if not line:
            break
        instructions_lines.append(line)
    
    instructions = ' '.join(instructions_lines)
    
    # Create and run agent
    agent = ToolkitAgent(
        name=name,
        toolkits=selected_toolkits,
        instructions=instructions
    )
    
    await agent.initialize()
    print(f"\n✅ Agent '{name}' created successfully!")
    
    # Interactive mode
    print("\nEnter commands for your agent (type 'quit' to exit):")
    while True:
        command = input("\n>> ")
        if command.lower() in ['quit', 'exit']:
            break
        
        print("\n🔄 Processing...")
        result = await agent.run(command)
        print(f"\n{result}")


async def main():
    """Main entry point for tools demonstration."""
    print("=" * 60)
    print("ARCADE AI TOOLS")
    print("=" * 60)
    
    options = {
        "1": ("List available toolkits", list_available_tools),
        "2": ("Email assistant demo", lambda: AgentExamples.email_assistant()),
        "3": ("Math solver demo", AgentExamples.math_solver),
        "4": ("Create custom agent", create_custom_agent),
    }
    
    print("\nOptions:")
    for key, (desc, _) in options.items():
        print(f"{key}. {desc}")
    
    choice = input("\nSelect option: ")
    
    if choice in options:
        _, func = options[choice]
        await func()
    else:
        print("Invalid option!")


if __name__ == "__main__":
    asyncio.run(main())