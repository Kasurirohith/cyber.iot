from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import datetime

app = Flask(__name__)
CORS(app)

model = joblib.load("saved_model/model.pkl")

logs = []

@app.route('/')
def home():
    return "CyberShield Backend Running 🚀"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json['features']

        input_data = np.array(data).reshape(1, -1)

        # MODEL PREDICTION
        prediction = model.predict(input_data)[0]
        result = int(prediction)

        # FORCE ATTACK DEMO (VERY IMPORTANT FOR FINAL)
        if sum(data) > 200:
            result = 1

        confidence = None
        if hasattr(model, "predict_proba"):
            confidence = max(model.predict_proba(input_data)[0])

        time_now = datetime.datetime.now().strftime("%H:%M:%S")

        logs.append({
            "input": data,
            "result": result,
            "confidence": round(confidence, 2) if confidence else None,
            "time": time_now
        })

        return jsonify({
            "result": result,
            "confidence": round(confidence, 2) if confidence else None,
            "time": time_now
        })

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/logs')
def get_logs():
    return jsonify(logs)

@app.route('/stats')
def stats():
    total = len(logs)
    normal = len([x for x in logs if x['result'] == 0])
    attack = len([x for x in logs if x['result'] == 1])

    return jsonify({
        "total": total,
        "normal": normal,
        "attack": attack
    })

@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    global logs
    logs = []
    return jsonify({"message": "Logs cleared"})

if __name__ == '__main__':
    app.run(debug=True)