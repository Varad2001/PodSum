from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route("/test", methods=['POST'])
def test():
    if request.method == 'POST':
        return jsonify({'status' : 200, 'msg' : 'success'})


if __name__ == '__main__':
    app.run()
