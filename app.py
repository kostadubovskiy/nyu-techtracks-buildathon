from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return jsonify({\"message\": \"Backend is running!\"})

if __name__ == '__main__':
    app.run(debug=True)