from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "hello gamers\n"


def main():
    app.run(host="localhost", port=4820)


if __name__ == "__main__":
    main()
