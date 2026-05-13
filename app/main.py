from flask import Flask, request, jsonify

app = Flask(__name__)


@app.get("/")
def get_ip():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    print(client_ip)
    if "," in client_ip:
        client_ip = client_ip.split(",")[0].strip()
    return jsonify(your_ip=client_ip)


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/ready")
def ready():
    return jsonify(status="ready")
