from app import create_app
from flask import jsonify

app = create_app()

# Add a basic route to check if server is running
@app.route('/')
def root():
    return jsonify({"message": "Restaurant API is running"})

if __name__ == '__main__':
    app.run(debug=True, host='localhost')