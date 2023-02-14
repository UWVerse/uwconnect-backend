from uwconnect_core.main import create_app
from flask_cors import CORS

if __name__ == "__main__":
    app = create_app()
    CORS(app)
    @app.route("/")
    def foo():
        return "Hello World"


    app.run()