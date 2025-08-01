#!/usr/bin/env python3
"""AI Agent for email task extraction using Arcade tools."""

import asyncio
import datetime
import os
from typing import List, Optional

from agents import Agent, Runner
from agents_arcade import get_arcade_tools
from agents_arcade.errors import AuthorizationError
from arcadepy import AsyncArcade
from dotenv import load_dotenv
from pydantic import BaseModel

from src.database.task_db import TaskDatabase, TaskRecord

# Load environment variables
load_dotenv()


class Task(BaseModel):
    """Task model for extracted email tasks."""

    name: str
    priority: int  # 1 for high, 2 for medium, 3 for low
    due_date: str  # ISO format date string


class ImportantTasks(BaseModel):
    """Container for extracted tasks and summary."""

    tasks: List[Task]
    summary: str


async def extract_email_tasks(
    toolkits: List[str] = ["gmail"],
    model: str = "o3-mini",
    user_email: Optional[str] = None,
) -> ImportantTasks:
    """
    Extract tasks from Gmail emails using AI agent.

    Args:
        toolkits: List of Arcade toolkits to use (default: ["gmail"])
        model: AI model to use (default: "o3-mini")
        user_email: User email for context (optional)

    Returns:
        ImportantTasks object containing extracted tasks and summary
    """
    # Initialize Arcade client
    client = AsyncArcade()

    # Get tools
    tools = await get_arcade_tools(client, toolkits=toolkits)

    # Create agent
    agent = Agent(
        name="Email Task Extractor",
        instructions=(
            "You are a helpful assistant that can analyze Gmail emails. "
            "Your job is to summarize emails and extract actionable tasks. "
            "Ignore promotional emails. Extract tasks with clear priorities and due dates."
        ),
        model=model,
        tools=tools,  # type: ignore
        output_type=ImportantTasks,
    )

    # Run the agent
    context = {"user_id": user_email} if user_email else {}
    result = await Runner.run(
        starting_agent=agent,
        input="What are my latest emails? Extract any actionable tasks.",
        context=context,
    )

    return result.final_output


async def main():
    """Main entry point for the email task extraction agent."""
    print("=" * 50)
    print("EMAIL TASK EXTRACTION AGENT")
    print("Powered by Arcade AI Tools")
    print("=" * 50)

    # Initialize database
    db = TaskDatabase()

    try:
        # Get user email from environment or ask
        user_email = os.getenv("ARCADE_USER_ID")
        if not user_email:
            user_email = input("\nEnter your email address: ")

        print(f"\n📧 Analyzing emails for: {user_email}")
        print("🔄 Processing...")

        # Extract tasks
        result = await extract_email_tasks(user_email=user_email)

        if result and result.tasks:
            print(f"\n✅ Found {len(result.tasks)} tasks")
            print("\n📊 SUMMARY:")
            print(f"   {result.summary}")

            print("\n📋 EXTRACTED TASKS:")
            priority_map = {1: "🔴 HIGH", 2: "🟡 MEDIUM", 3: "🟢 LOW"}

            # Process and store tasks
            new_tasks = []
            duplicate_tasks = []

            for i, task in enumerate(result.tasks, 1):
                print(f"\n{i}. {task.name}")
                print(f"   Priority: {priority_map.get(task.priority, '❓ UNKNOWN')}")
                print(f"   Due: {task.due_date}")

                # Check for duplicates
                is_duplicate = False
                similar_tasks = db.find_similar_tasks(task.name)
                if (
                    similar_tasks
                    and len(similar_tasks) > 0
                    and similar_tasks[0].similarity_distance < 0.1
                ):
                    is_duplicate = True
                    duplicate_tasks.append(task)
                    continue

                # Add new task to database
                db_task = TaskRecord(
                    name=task.name,
                    priority=task.priority,
                    due_date=task.due_date,
                    created_at=datetime.datetime.now().isoformat(),
                )
                db.add_task(db_task)
                new_tasks.append(task)

            # Print summary of database operations
            if new_tasks:
                print(f"\n💾 Saved {len(new_tasks)} new tasks to database")
            if duplicate_tasks:
                print(
                    f"\n🔁 Found {len(duplicate_tasks)} duplicate tasks that were not saved:"
                )
                for task in duplicate_tasks:
                    print(f"   - {task.name}")
        else:
            print("\n❌ No actionable tasks found in recent emails")

    except AuthorizationError as e:
        print("\n❌ Authorization Required")
        print(f"Please login to Google: {e}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

    print("\n" + "=" * 50)
    # Close database connection
    db.close()


if __name__ == "__main__":
    asyncio.run(main())
