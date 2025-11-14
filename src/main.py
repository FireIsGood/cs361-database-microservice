from typing import Any
from flask import Flask, request
from dataclasses import asdict, dataclass
import uuid


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


# The simplest in-memory database...
db = {}

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


def main():
    # Load DB from memory
    pass

    # Start process to save DB to memory? (I dunno)
    pass

    app.run(host="localhost", port=4820, debug=True)


if __name__ == "__main__":
    main()
