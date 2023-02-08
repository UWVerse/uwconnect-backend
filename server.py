from uwconnect_core import create_app
from flask_cors import CORS

if __name__ == "__main__":
    app = create_app()
    CORS(app)
    @app.route("/")
    def foo():
        return "Check /dummy/ and /dummy/ping_db for examples"


    app.run()