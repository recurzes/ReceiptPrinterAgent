"""Database setup script."""

import os
import sys
from dotenv import load_dotenv
import libsql_experimental as libsql

load_dotenv()


def test_database():
    """Test database connection and functionality."""
    try:
        from src.database import TaskDatabase
        
        print("\n🔧 Testing database connection...")
        db = TaskDatabase()
        print("✅ Database connection successful")
        
        # Test adding a sample task
        from datetime import datetime
        
        class SampleTask:
            name = "Database Test Task"
            priority = 2
            due_date = datetime.now().isoformat()
        
        print("\n🧪 Testing task creation...")
        task_record = db.add_task(SampleTask(), email_context="Database setup test")
        print(f"✅ Created test task with ID: {task_record.id}")
        
        # Test similarity search
        print("\n🔍 Testing similarity search...")
        similar_tasks = db.find_similar_tasks("database test", limit=1)
        if similar_tasks:
            print(f"✅ Found {len(similar_tasks)} similar task(s)")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False


def create_database_tables():
    """Create the required tables in Turso database."""
    
    # Get credentials from environment
    db_url = os.getenv("TURSO_DATABASE_URL")
    auth_token = os.getenv("TURSO_AUTH_TOKEN")
    
    if not db_url or not auth_token:
        print("❌ Missing database credentials!")
        print("Please set TURSO_DATABASE_URL and TURSO_AUTH_TOKEN in your .env file")
        return False
    
    print(f"📍 Connecting to: {db_url}")
    
    try:
        # Connect to database
        conn = libsql.connect(db_url, auth_token=auth_token)
        cursor = conn.cursor()
        
        # Check if tasks table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='tasks'
        """)
        
        if cursor.fetchone():
            print("⚠️  Tasks table already exists")
            recreate = input("Drop and recreate table? (y/n): ").lower()
            if recreate == 'y':
                cursor.execute("DROP TABLE IF EXISTS tasks")
                cursor.execute("DROP INDEX IF EXISTS tasks_embedding_idx")
                print("🗑️  Dropped existing table and index")
        
        # Create tasks table
        print("📝 Creating tasks table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                priority INTEGER NOT NULL,
                due_date TEXT NOT NULL,
                created_at TEXT NOT NULL,
                email_context TEXT,
                embedding F32_BLOB(1536)
            )
        """)
        
        # Create vector index
        print("🔍 Creating vector index...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS tasks_embedding_idx 
            ON tasks(libsql_vector_idx(embedding))
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return False


def main():
    """Main setup function."""
    print("🗄️  Database Setup")
    print("=" * 30)
    
    # Check environment variables
    db_url = os.getenv("TURSO_DATABASE_URL")
    auth_token = os.getenv("TURSO_AUTH_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not db_url or not auth_token or not openai_key:
        print("❌ Missing required environment variables:")
        if not db_url:
            print("   - TURSO_DATABASE_URL")
        if not auth_token:
            print("   - TURSO_AUTH_TOKEN") 
        if not openai_key:
            print("   - OPENAI_API_KEY")
        print("\nPlease set these in your .env file")
        return
    
    print("✅ Environment variables found")
    
    # Ask about table creation
    print("\n" + "=" * 30)
    create_tables = input("Create/recreate database tables? (y/n): ").lower()
    
    if create_tables == 'y':
        if not create_database_tables():
            return
    
    # Test database
    print("\n" + "=" * 30)
    test_conn = input("Test database connection? (y/n): ").lower()
    
    if test_conn == 'y':
        if not test_database():
            return
    
    # Done
    print("\n" + "=" * 30)
    print("✅ Database setup complete!")
    print("\nYour database is ready for:")
    print("  - python agent.py")
    print("  - python main.py")


if __name__ == "__main__":
    main()
