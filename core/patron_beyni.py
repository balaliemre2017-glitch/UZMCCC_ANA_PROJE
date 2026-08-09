
import pathlib, json
from config.settings import BASE_DIR
from auth.manager import is_logged_in
from database.models import log_hafiza
def load_manifests():
    mans={}
    wdir=BASE_DIR/'workers'
    for p in wdir.iterdir():
        if p.is_dir():
            mf=p/'manifest.json'
            if mf.exists():
                try: mans[p.name]=json.loads(mf.read_text(encoding='utf-8'))
                except: pass
    return mans
def analiz_et(emir_text):
    emir=emir_text.lower()
    mans=load_manifests()
    hedefler=[]
    is_foto = any(x in emir for x in ['foto','resim','gonderi','image'])
    if is_foto:
        for pl in ['youtube','whatsapp','instagram','facebook']:
            if pl in mans: hedefler.append(pl)
    for plat in mans.keys():
        if plat in emir and plat not in hedefler:
            hedefler.append(plat)
    if not hedefler:
        for plat in mans.keys():
            if is_logged_in(plat):
                hedefler.append(plat)
    if not hedefler:
        hedefler=['youtube']
    filtreli=[p for p in hedefler if p in ['canva','capcut'] or is_logged_in(p)]
    return {'hedefler': filtreli, 'tip': 'foto' if is_foto else 'video', 'orijinal': emir_text}
def gorev_dagit(video_path, emir_text):
    analiz=analiz_et(emir_text)
    print(f"PATRON: {analiz}")
    log_hafiza(emir_text, str(analiz))
    sonuclar=[]
    for plat in analiz['hedefler']:
        try:
            import importlib.util
            wp=BASE_DIR/f'workers/{plat}/worker.py'
            if not wp.exists(): continue
            spec=importlib.util.spec_from_file_location(f"{plat}_worker", str(wp))
            mod=importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            worker=mod.Worker()
            if analiz['tip']=='foto' and not worker.can_do('foto_paylas'):
                continue
            worker.paylas(video_path, emir_text)
            sonuclar.append(plat)
        except Exception as e:
            print(f"[{plat}] HATA: {e}")
    return sonuclar
