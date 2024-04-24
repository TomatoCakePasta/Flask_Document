import sqlite3

import click
from flask import current_app, g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

# These are functions that will run SQL commandas
def init_db():
    # get_db() returns a database connection
    db = get_db()

    # open a file relative to the flaskr package
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
    
# defines a command line command called "init-db"
@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""

    # calls the init_db()
    init_db()

    # shows a success message
    click.echo("Initialized the database.")

def init_app(app):
    # tells Flask to call that function
    app.teardown_appcontext(close_db)

    # adds a new command that can be called with the flask command
    app.cli.add_command(init_db_command)

