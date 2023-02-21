from uwconnect_core.main import create_app
from flask_cors import CORS

app = create_app()
CORS(app)

@app.route("/")
def foo():
    return "Hello World"

if __name__ == "__main__":
    app.run()