import os
from project import app
from flask import send_from_directory


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    """Catchall to serve our React app by default"""
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")
