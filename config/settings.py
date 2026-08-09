import pathlib
BASE_DIR = pathlib.Path(__file__).parent.parent
YEDEKLER_DIR = BASE_DIR / "yedekler"
DB_PATH = YEDEKLER_DIR / "uzmccc.db"
AUTH_PATH = YEDEKLER_DIR / "auth.json"
ENV_PATH = BASE_DIR / "API_ANAHTARLAR.env"
HAFIZA_PATH = YEDEKLER_DIR / "hafiza.json"
