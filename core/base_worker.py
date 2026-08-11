# core/base_worker.py
from abc import ABC, abstractmethod
import logging

class BaseWorker(ABC):
    def __init__(self, platform_name):
        self.platform_name = platform_name
        self.is_authenticated = False
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @abstractmethod
    def authenticate(self):
        """Platforma giriş yapma ve API'ye bağlanma işlemi."""
        pass

    @abstractmethod
    def execute_task(self, task_data):
        """Platforma özel görevi (post atma, video yükleme vb.) yerine getirme."""
        pass

    def log_status(self, message):
        """İşlemleri terminale veya log dosyasına yazdırma."""
        logging.info(f"[{self.platform_name.upper()} WORKER] : {message}")
