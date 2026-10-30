from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("camera.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "photo" not in request.files:
        return jsonify({"error": "No photo"}), 400

    photo = request.files["photo"]
    os.makedirs("photos", exist_ok=True)
    photo.save(os.path.join("photos", "photo.jpg"))

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
  
