from flask import Flask

app = Flask(__name__)


@app.route("/", defaults={"_path": ""})
@app.route("/<path:_path>")
def hello(_path):
    return "Hello from App 2!\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
