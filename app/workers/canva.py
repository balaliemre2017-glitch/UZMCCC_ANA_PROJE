from .base import BaseIsci
class CanvaIsci(BaseIsci):
    def __init__(self): super().__init__('CANVA')

# MERGE - SSO destekli
import pathlib, json
def load_auth():
    p=pathlib.Path(__file__).parent.parent.parent / 'yedekler' / 'auth.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
