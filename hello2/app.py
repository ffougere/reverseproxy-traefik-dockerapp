import os

from flask import Flask, jsonify
import psycopg

app = Flask(__name__)


APP_NAME = "hello2"
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "appdb"),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", ""),
    "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "3")),
}


@app.route("/health")
def health():
    return jsonify({"status": "ok", "app": APP_NAME, "check": "liveness"})


@app.route("/db-check")
def db_check():
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS connectivity_checks (
                        id SERIAL PRIMARY KEY,
                        app_name TEXT NOT NULL,
                        checked_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                    """
                )
                cur.execute(
                    "INSERT INTO connectivity_checks (app_name) VALUES (%s)",
                    (APP_NAME,),
                )
                cur.execute(
                    "SELECT COUNT(*) FROM connectivity_checks WHERE app_name = %s",
                    (APP_NAME,),
                )
                total_checks = cur.fetchone()[0]

        return jsonify(
            {
                "status": "ok",
                "app": APP_NAME,
                "db_host": DB_CONFIG["host"],
                "checks_for_app": total_checks,
            }
        )
    except Exception as exc:
        return jsonify({"status": "error", "app": APP_NAME, "error": str(exc)}), 500


@app.route("/", defaults={"_path": ""})
@app.route("/<path:_path>")
def hello(_path):
    return "Hello from App 2!\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
