# Project Documentation Assistant

A tool to help manage and interact with project documentation using vector storage and natural language processing.

## Project Structure

- `app/` - Core application code
- `tests/` - Unit and integration tests
- `input/` - Input documents and files
- `output/` - Processed output files

## Setup and Installation

### Prerequisites
- Python 3.9 or higher
- curl (for uv installation)

### Step 1: Install uv (Python package manager)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Create and activate virtual environment
```bash
# Create virtual environment
uv venv

# Activate environment
source .venv/bin/activate  # Linux/MacOS
# .\.venv\Scripts\activate  # Windows (PowerShell)
```

### Step 3: Install dependencies
```bash
uv pip install -r requirements.txt
```

### Step 4: Initialize the project
1. Create the input directory:
```bash
mkdir -p input
```

2. Place your documents (PDF, Markdown, or .url files) in the input directory

### Step 5: Run the application
```bash
# Set debug logging and start Flask
LOGLEVEL=DEBUG FLASK_APP=app.main flask run

# The application will be available at http://localhost:5000
```

## Usage
1. Access the web interface at http://localhost:5000
2. Upload documents to the input directory
3. Ask questions about your documentation using the chat interface

## Troubleshooting
- If you get "flask command not found", ensure your virtual environment is activated
- Check logs for any errors during document processing
- Ensure your .url files contain valid URLs, one per line
