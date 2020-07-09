from baby_log.core import app, connect_mongoengine
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Baby Log Server')
    parser.add_argument('--run',
                        action='store_true',
                        help="Runs the WSGI Server"
                        )

    args = parser.parse_args()

    if args.run:
        connect_mongoengine()
        app.run(host="0.0.0.0", port=80, debug=True)
