"""
UZMCCC Holding - Geleceğe Dönük İşçi ve Hiyerarşi Yönetimi (v2.6)
"""

class HierarchyManager:
    def __init__(self):
        # Holding içi departman ve yetki seviyeleri
        self.departments = {
            "social_media": ["InstagramUzmani", "TikTokUzmani", "YouTubeUzmani", "FacebookUzmani", "TwitterUzmani"],
            "communication": ["TelegramYayincisi", "WhatsAppOtomasyoncusu"],
            "production": ["CanvaTasarimcisi", "CapCutKurgucusu"],
            "devops": ["GitHubDevOpsUzmani"]
        }

    def get_department_workers(self, dept_name):
        return self.departments.get(dept_name, [])

    def validate_command_authority(self, worker_name, command):
        """Gelecekte eklenecek otonom yetki denetimi için altyapı"""
        # Patronun emirleri her zaman mutlak önceliklidir
        return True
