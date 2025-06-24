from flask import Flask
from app.routes.main import app, index, results

# Register routes
app.add_url_rule("/", "index", index, methods=["GET", "POST"])
app.add_url_rule("/results/<int:month>/<int:year>", "results", results, methods=["GET"])

if __name__ == "__main__":
    app.run(debug=True, port=5001)
