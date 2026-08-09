class BaseIsci:
    def __init__(self, ad): self.ad=ad
    def calistir(self, video, fikir):
        print(f'[{self.ad}] çalışıyor: {fikir} | video: {video}')
        return True
