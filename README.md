# RPG Random Table Generator

This is a simple web application built with Flask that allows users to create, manage, and roll on random tables for tabletop RPGs. Users can also create custom pages that display a random roll from a selection of multiple tables, which can be shared via a unique URL.

## Features

- **Create Tables**: Define new random tables with a unique name and descriptive tags.
- **Add Weighted Items**: Populate tables with items, each having a specific weight to influence its chance of being rolled.
- **Roll on Tables**: Get a random, weighted result from any table with a single click.
- **Custom Shareable Pages**: Create custom pages that combine multiple tables. When visiting the page's unique URL, a random result from each included table is displayed.

## Project Structure

```
.
├── app.py              # Main Flask application file
├── models.py           # SQLAlchemy database models
├── requirements.txt    # Python dependencies
├── static/             # CSS and other static files
│   └── style.css
├── templates/          # HTML templates
│   ├── create_custom_page.html
│   ├── create_table.html
│   ├── custom_page.html
│   ├── index.html
│   └── table_detail.html
└── tests/              # Pytest tests
    ├── conftest.py
    └── test_app.py
```

## Setup and Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install all the required Python packages using pip.

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

Create the SQLite database and all the necessary tables by running the following command:

```bash
flask init-db
```
This will create a `rpg_tables.db` file in the `instance/` directory.

## Running the Application

Once the setup is complete, you can run the development server:

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000`.

## Running the Tests

The project includes a suite of tests written with `pytest`. To run the tests, execute the following command from the root directory of the project:

```bash
PYTHONPATH=. pytest
```

The `PYTHONPATH=.` part is important as it ensures that the test runner can correctly locate the application module.
