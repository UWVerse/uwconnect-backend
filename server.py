from uwconnect_core.main import create_app
from flask_cors import CORS

app = create_app()
CORS(app, supports_credentials=True)

if __name__ == "__main__":
    # app.run(host='dev.localhost')
    app.run()