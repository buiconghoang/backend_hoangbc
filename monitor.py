from filemonitor import app
from filemonitor.config import config
if __name__ == "__main__":
    app.run(host=config.host, debug=config.debug, port=config.port)