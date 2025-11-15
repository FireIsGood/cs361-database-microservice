from typing import Any
from flask import Flask, request
from dataclasses import asdict, dataclass
from pathlib import Path
import json
import threading
import time
import uuid
import logging
import atexit


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
)


@dataclass
class DbEntry:
    """Represents an entry in the database"""

    id: str
    data: Any

    def __init__(self, id: uuid.UUID | None = None, data: Any | None = None) -> None:
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = str(id)
        self.data = data


# ***In-memory database and on-disk locations***
db: dict[str, Any] = {}
# database/ folder lives at project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_ROOT / "database"
DB_FILE = DB_DIR / "db.json"


def load_db_from_disk() -> None:
    """
    Loads the database from database/db.json if it exists.
    If not, then starts with an empty in-memory db.
    """
    global db
    DB_DIR.mkdir(exist_ok=True)

    # Guard clause: if file doesn't exist, then starts empty and returns
    if not DB_FILE.exists():
        db = {}
        logging.info("No existing db.json found; starting with empty database.")
        return

    try:
        with DB_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        # On any error, starts fresh rather than crashing
        db = {}
        logging.warning(
            "Failed to load db.json (%s); starting with empty database.", e
        )
        return

    # Expects {id: value, ...}
    if isinstance(data, dict):
        db = data
        logging.info("Loaded database from disk with %d entries.", len(db))
    else:
        db = {}
        logging.warning(
            "db.json did not contain a JSON object; starting with empty database."
        )


def save_db_to_disk() -> None:
    """
    Saves the current in-memory db to database/db.json.

    If db.json already exists,
    rename it to database/db_backup_<UNIX_TIMESTAMP>.json first,
    then write the new db.json.
    """
    DB_DIR.mkdir(exist_ok=True)

    if DB_FILE.exists():
        backup_name = DB_DIR / f"db_backup_{int(time.time())}.json"
        DB_FILE.replace(backup_name)

    # Takes a shallow copy so that writes during the save won't break things
    snapshot = dict(db)
    with DB_FILE.open("w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    logging.info("Saved database to db.json with %d entries.", len(snapshot))


def autosave_loop(interval_seconds: int = 60) -> None:
    """Background loop that periodically saves the db to disk."""
    while True:
        time.sleep(interval_seconds)
        try:
            save_db_to_disk()
            logging.info(
                "Autosave complete; current database size: %d entries.", len(db)
            )
        except Exception as e:
            logging.error("Error during autosave: %s", e)


def graceful_shutdown():
    """Run any last tasks before shutting down"""
    logging.info("Exiting gracefully")

    # Save database to disk
    save_db_to_disk()


# ***Flask app and routes***
app = Flask(__name__)


@app.route("/db")
def read_database_full():
    return db


@app.route("/db/<uuid:id>")
def read_database(id: uuid.UUID):
    entry = DbEntry(id, db.get(str(id)))
    if entry.data is None:
        return "Database entry does not exist\n", 404
    return asdict(entry)


@app.route("/db", methods=["POST"])
def write_database():
    data = request.get_json(silent=True)
    if data is None:
        return "Invalid type of data\n", 400

    entry = DbEntry(data=data)
    db[entry.id] = entry.data

    return asdict(entry)


@app.route("/db/<uuid:id>", methods=["PUT"])
def update_database(id: uuid.UUID):
    entry = DbEntry(id, db.get(str(id)))
    if entry.data is None:
        return "Database entry does not exist\n", 404

    data = request.get_json(silent=True)
    if data is None:
        return "Invalid type of data\n", 400

    entry.data = data
    db[entry.id] = entry.data

    return asdict(entry)


@app.route("/db/<uuid:id>", methods=["DELETE"])
def delete_database(id: uuid.UUID):
    """
    Deletes an entry by id.
    If the entry exists, then removes it and returns 204 + empty body.
    If not, returns 404.
    """
    removed = db.pop(str(id), None)
    if removed is None:
        return "Database entry does not exist\n", 404

    return "", 204


def main():
    # Loads DB from disk (if it exists)
    load_db_from_disk()

    # Starts background autosave every 60 seconds
    autosave_thread = threading.Thread(target=autosave_loop, args=(60,), daemon=True)
    autosave_thread.start()

    # Register graceful shutdown function
    atexit.register(graceful_shutdown)

    # Runs Flask app
    app.run(host="localhost", port=4820)


if __name__ == "__main__":
    main()
