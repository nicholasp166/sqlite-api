# SQLite Database Manager

A FastAPI-based web application for managing SQLite databases through an intuitive HTML interface.

## Description

This project provides a simple web interface to create and manage SQLite databases. Users can view existing databases, create new tables, and explore database contents through a browser-based UI.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLite** - Lightweight database engine
- **Jinja2** - Template rendering
- **Pydantic** - Data validation

## Features

- List all SQLite databases
- Create new tables in databases
- View database structure and contents
- RESTful API endpoints
- Health check endpoint

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Or on Linux/Mac
source .venv/bin/activate
```

## Usage

```bash
# Navigate to src directory
cd src

# Run the application
uvicorn main:app --reload
```

The application will be available at http://localhost:8000

## API Endpoints

| Method | Endpoint                          | Description                  |
| ------ | --------------------------------- | ---------------------------- |
| GET    | `/`                               | Main page with database list |
| GET    | `/databases/{dbName}`             | View database tables         |
| POST   | `/databases/createTable/{dbName}` | Create a new table           |
| GET    | `/health`                         | Health check endpoint        |

## Project Structure

```
dbproj/
├── src/
│   ├── main.py              # FastAPI application
│   ├── services/
│   │   ├── __init__.py
│   │   └── dbservice.py     # Database service class
│   ├── templates/           # HTML templates
│   │   ├── index.html
│   │   └── database.html
│   └── database/            # SQLite database files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Example Usage

1. Visit the main page to see all databases
2. Click on a database to view its tables
3. Use the form to create new tables with custom columns

## License

MIT
