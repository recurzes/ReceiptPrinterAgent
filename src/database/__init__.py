"""Database module for task storage with embeddings."""

# Primary database interface
from .task_db import TaskDatabase, TaskRecord

__all__ = ['TaskDatabase', 'TaskRecord']
