# Project Documentation Assistant

A tool to help manage and interact with project documentation using AI.

## Quick Start

1. Install requirements:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

2. Create input directory and add documents:
```bash
mkdir -p input
```

### Adding Documents

#### PDF Files
- Place any PDF files directly in the `input/` directory
- The system will extract text from all pages
- Example: `input/user_manual.pdf`

#### Markdown Files
- Place .md files directly in the `input/` directory
- The system will process the markdown content
- Example: `input/README.md`

#### URL Files
- Create a .url file containing one URL per line
- The system will fetch and process web content from each URL
- Example `input/websites.url` content:
```
https://example.com/docs
https://anothersite.com/help
https://yoursite.com/faq
```

### Document Processing
- The system automatically processes new documents on startup
- To refresh the knowledge base:
  1. Add/remove files in the `input/` directory
  2. Restart the application

3. Run the application:
```bash
LOGLEVEL=DEBUG FLASK_APP=app.main flask run
```

4. Access the web interface at http://localhost:5123

## Features
- Upload documents (PDF, Markdown, URLs)
- Ask questions about your documentation
- Get AI-powered answers with source references

## Troubleshooting
- Ensure virtual environment is activated
- Check logs for errors
- Verify URLs in .url files are valid
