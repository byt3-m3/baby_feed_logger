from baby_log.core import app, connect_mongoengine
from baby_log.env import APP_PORT, MONGO_DB_HOST, MONGO_DB_PORT, DEBUG, APP_HOST_BIND
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Baby Log Server')
    parser.add_argument('--run',
                        action='store_true',
                        help="Runs the WSGI Server"
                        )

    args = parser.parse_args()

    if args.run:
        connect_mongoengine(MONGO_DB_HOST, MONGO_DB_PORT)
        app.run(host=APP_HOST_BIND, port=APP_PORT, debug=DEBUG)
