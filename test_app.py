from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Flask is working!"})

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Test endpoint"})

if __name__ == "__main__":
    app.run(debug=True, port=5000) 