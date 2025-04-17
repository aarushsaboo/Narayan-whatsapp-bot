from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "✅ Flask + ngrok is working!", 200

@app.route('/test', methods=['POST'])
def test_post():
    data = request.get_json(force=True)
    return jsonify({
        "message": "✅ POST received",
        "data": data
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
