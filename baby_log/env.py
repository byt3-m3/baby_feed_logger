import os

DEBUG = os.getenv("DEBUG", False)
APP_PORT = os.getenv("APP_PORT", 80)
APP_HOST_BIND = os.getenv("APP_HOST_BIND", "0.0.0.0")
MONGO_DB_HOST = os.getenv("MONGO_DB_HOST", "192.168.1.182")
MONGO_DB_PORT = os.getenv("MONG_DB_PORT", 27017)
