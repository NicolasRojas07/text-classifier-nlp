#!/usr/bin/env python3
"""Test simple del servidor Flask"""

from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route("/test", methods=["GET"])
def test():
    print(f"[{time.time():.2f}] GET /test")
    return jsonify({
        "status": "ok",
        "time": time.time()
    })

if __name__ == "__main__":
    print("🚀 Servidor test en http://127.0.0.1:5555")
    app.run(host="127.0.0.1", port=5555, debug=False)
