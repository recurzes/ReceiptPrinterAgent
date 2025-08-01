# Receipt Printer Task Manager

A Python-based task management system that prints tasks to a thermal receipt printer and integrates with various services.

## Features

- Print tasks to thermal receipt printers
- Extract tasks from Gmail automatically
- AI-powered task parsing and prioritization
- Duplicate detection using vector embeddings
- Integration with multiple services (Gmail, Slack, Calendar, Notion) via Arcade.dev

## Installation

```bash
# Clone the repository
git clone https://github.com/CodingWithLewis/ReceiptPrinterAgent
cd receipt-printer-tasks

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Required environment variables:
- `ARCADE_API_KEY` - Get from [arcade.dev](https://arcade.dev)
- `OPENAI_API_KEY` - OpenAI API key
- `TURSO_DATABASE_URL` - Database URL (optional, uses local SQLite by default)
- `TURSO_AUTH_TOKEN` - Database auth token (if using Turso)

## Usage

### Extract tasks from Gmail
```bash
python agent.py
```

### Create a task from text
```bash
python main.py
```

### Use Arcade tools
```bash
python tools.py
```

### Setup database
```bash
python setup_database.py
```

## Requirements

- Python 3.8+
- Thermal receipt printer (USB)
- API keys for OpenAI and Arcade.dev

## License

MIT License - see LICENSE file for details.