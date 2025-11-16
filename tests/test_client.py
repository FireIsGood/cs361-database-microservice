# Code adapted from https://github.com/max-osu/ms_top_scores test_client.py
import requests
import json

# Localhost -> 127.0.0.1
# Port Number -> 4820
BASE_URL = "http://127.0.0.1:4820"


def pretty_print(title, response):
    """Print in style."""
    print(f"\n---- {title} ----")
    print(f"Status code: {response.status_code}")
    # Parse body, if there is a body, and print in formatted JSON string.
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    # Return error message.
    except ValueError:
        print(response.text)


# Dynamically generated database entry ID
db_entry_id: str = ""


def main():
    # 1. Test GET /db
    resp = requests.get(f"{BASE_URL}/db")
    pretty_print("1. GET /db (All database entries)", resp)

    # 2. Test POST /db
    resp = requests.post(f"{BASE_URL}/db", json="hi")
    pretty_print("2. POST /db (Add a database entry)", resp)
    global db_entry_id
    res_json = resp.json()
    db_entry_id = res_json.get("id")

    # 3. Test GET /db/{new item ID}
    resp = requests.get(f"{BASE_URL}/db/{db_entry_id}")
    pretty_print("3. GET /db/{new item ID} (New entry)", resp)

    # 4. Test PUT /db{new item ID}
    resp = requests.put(f"{BASE_URL}/db/{db_entry_id}", json="bye")
    pretty_print("4. PUT /db (Modify the submitted entry)", resp)

    # 5. Test GET /db/{new item ID}
    resp = requests.get(f"{BASE_URL}/db/{db_entry_id}")
    pretty_print("5. GET /db/{new item ID} (New entry)", resp)

    # 6. Test DELETE /db/{new item ID}
    resp = requests.delete(f"{BASE_URL}/db/{db_entry_id}")
    pretty_print("6. DELETE /db (Delete new entry)", resp)

    # 7. Test GET /db
    resp = requests.get(f"{BASE_URL}/db")
    pretty_print("7. GET /db (All database entries - should be empty)", resp)


if __name__ == "__main__":
    main()
