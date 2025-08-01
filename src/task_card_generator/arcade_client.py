"""Arcade API client for automated task generation and printing."""

import os
from dotenv import load_dotenv
from arcadepy import Arcade
from .ai_client import parse_ai_response

# Load environment variables from .env file
load_dotenv()


class ArcadeTaskGenerator:
    """Handles Arcade API integration for task generation."""
    
    def __init__(self, api_key=None, user_id=None):
        """Initialize Arcade client."""
        self.api_key = api_key or os.getenv("ARCADE_API_KEY")
        self.user_id = user_id or os.getenv("ARCADE_USER_ID", "user@example.com")
        self.client = Arcade(api_key=self.api_key) if self.api_key else None
    
    def get_task_from_arcade(self, tool_name, input_data):
        """Get task response from Arcade tool and format for printing."""
        if not self.client:
            return None, "Error: ARCADE_API_KEY not configured"
        
        try:
            # Execute the Arcade tool
            response = self.client.tools.execute(
                tool_name=tool_name,
                input=input_data,
                user_id=self.user_id,
            )
            
            # Format the response for task card generation
            task_data = self._format_arcade_response(response, tool_name)
            return task_data, None
            
        except Exception as e:
            return None, f"Error executing Arcade tool: {str(e)}"
    
    def authorize_tool(self, tool_name):
        """Authorize a tool that requires authentication."""
        if not self.client:
            return None, "Error: ARCADE_API_KEY not configured"
        
        try:
            auth_response = self.client.tools.authorize(
                tool_name=tool_name,
                user_id=self.user_id,
            )
            return auth_response, None
        except Exception as e:
            return None, f"Error authorizing tool: {str(e)}"
    
    def _format_arcade_response(self, response, tool_name):
        """Format Arcade response into task card data."""
        # Extract the actual value from the response
        output_value = response.output.value if hasattr(response.output, 'value') else str(response.output)
        
        # Create task data structure
        task_data = {
            "title": f"{tool_name} Result",
            "priority": "MEDIUM",
            "content": output_value,
            "tool_name": tool_name
        }
        
        # Try to determine priority based on tool name or content
        if "urgent" in tool_name.lower() or "critical" in tool_name.lower():
            task_data["priority"] = "HIGH"
        elif "info" in tool_name.lower() or "search" in tool_name.lower():
            task_data["priority"] = "LOW"
        
        return task_data


def get_task_from_arcade_tool(tool_name, input_data, api_key=None, user_id=None):
    """Convenience function to get task from Arcade tool."""
    generator = ArcadeTaskGenerator(api_key=api_key, user_id=user_id)
    return generator.get_task_from_arcade(tool_name, input_data)


def authorize_arcade_tool(tool_name, api_key=None, user_id=None):
    """Convenience function to authorize an Arcade tool."""
    generator = ArcadeTaskGenerator(api_key=api_key, user_id=user_id)
    return generator.authorize_tool(tool_name)