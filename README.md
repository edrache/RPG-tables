# RPG Random Table Generator

This is a simple web application built with Flask that allows users to create, manage, and roll on random tables for tabletop RPGs. Users can also create custom pages that display a random roll from a selection of multiple tables, which can be shared via a unique URL.

## Features

- **Create Tables**: Define new random tables with a unique name and descriptive tags.
- **Bulk Add Items**: Populate tables with multiple items at once using a simple format: `item1; item2:weight2; item3`.
- **Roll on Tables**: Get a random, weighted result from any table with a single click.
- **Markup-Based Custom Pages**: Create custom, shareable pages using a simple markup language. Use the tag `<t:table_name>` to embed a random roll from any of your tables directly into your text.

## How to Use

1.  **Create a Table**: From the home page, click "Create New Table". Give your table a unique name (e.g., `monsters`) and some tags, then click "Create Table".

2.  **Add Items**: You will be taken to the table detail page. In the "Add New Items" text box, you can add multiple items at once.
    -   Separate items with a semicolon (`;`).
    -   To assign a weight other than the default of 1, add a colon (`:`) followed by a number.
    -   Example: `Goblin; Orc; Hobgoblin:2; Dragon:5`

3.  **Create a Custom Page**: Go back to the home page and click "Create New Custom Page".
    -   Give your page a title (e.g., "Dungeon Entrance").
    -   In the "Content" box, write any text you like and embed your table rolls using the `<t:table_name>` tag.
    -   Example: `A <t:monsters> and a <t:monsters> guard the entrance. On the ground, you see a <t:minor_treasures>.`

4.  **View and Share**: After creating the page, you will be redirected to it. The page will display your text with the tags replaced by random rolls. You can copy the unique URL from your browser's address bar to share this page with others.

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
