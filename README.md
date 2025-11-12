# CS 361 Database Microservice

A Flask microservice to allow basic HTTP access to a simple in-memory database.

## Database

The database has all the basic CRUD functionality. It is intended for internal use so there is no system of
authorization.

## API

Routes:

- Read database entry
- Write database entry
- Update database entry
- Delete database entry

The API opens at the address <http://localhost:4820/> by default.

### Read database entry

> GET `/db/<id>`

Given an ID, returns the database entry.

EXAMPLE CALL:

```py
requests.get("http://localhost:4820/db/1def569a-a49a-4d0e-9448-733ef0b60828")
```

EXAMPLE OUTPUTS:

Object data

```json
{
  "id": "4ded3320-59bf-44df-b619-17e3bd9c9397",
  "data": {
    "word": "fish",
    "number": 4
  }
}
```

String data

```json
{
  "id": "1def569a-a49a-4d0e-9448-733ef0b60828",
  "data": "fish"
}
```

Number data

```json
{
  "id": "e754e750-85f3-40cf-a345-8cf30750ccbd",
  "data": 4
}
```

### Write database entry

> POST `/db`

Given data, stores the data in a database entry. The resulting new entry is returned.

EXAMPLE CALLS:

```py
requests.post("http://localhost:4820/db", json={"word": "fish", "number": 4})
requests.post("http://localhost:4820/db", json="fish")
requests.post("http://localhost:4820/db", json=4)
```

EXAMPLE OUTPUTS:

(same as from the 'Read database entry' endpoint)

```json
{
  "id": "79388c82-87e6-4528-accf-0bda421d71d9",
  "data": {
    "word": "fish",
    "number": 4
  }
}
```

### Update database entry

> PUT `/db/<id>`

Given data, changes the data of the given database entry matching the ID. The resulting updated entry is returned.

EXAMPLE CALLS:

```py
requests.post("http://localhost:4820/db/79388c82-87e6-4528-accf-0bda421d71d9", json={"word": "bird", "number": 6})
...
```

EXAMPLE OUTPUTS:

```json
{
  "id": "79388c82-87e6-4528-accf-0bda421d71d9",
  "data": {
    "word": "bird",
    "number": 6
  }
}
```

### Delete database entry

TODO

## Installation

This program requires additional libraries to function. This installation shows the steps to install the requirements
via pip inside a virtual environment.

> [!WARNING]  
> _The command to enter the Python Virtual environment differs by operating system. You can [check the full
> list](https://docs.python.org/3/library/venv.html#how-venvs-work) for your specific command. The POSIX version is listed
> in this example._

### Prerequisites

To run this program you must have Python 3 and pip installed. You can verify that the programs are installed with the
following command:

```bash
python3 --version
pip --version
```

### Initial setup

Create a virtual environment:

```bash
python3 -m venv env
```

Enter the virtual environment and install the dependencies:

```bash
source env/bin/activate
pip install -r requirements.txt
```

The requirements should now be installed into the virtual environment and the program can be run whenever you are within
this virtual environment.

### Running the program

Enter the virtual environment if not already inside:

```bash
source env/bin/activate
```

Run the program:

```bash
python3 src/main.py

```
