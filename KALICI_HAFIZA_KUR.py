
import pathlib, json, os, shutil
BASE=pathlib.Path(__file__).parent
print("=== V21 KALICI HAFIZA RESTORE ===")
print("Eski yaptiklarin geri yukleniyor, SILINMEYECEK!")

# 1. Dump'tan gelen eski dosyalar
DUMP = {
    "API_ANAHTARLAR.env": "GEMINI_API_KEY=AQ.Ab8RN6LqiNF_RnZykzNYoAiH8YWfP9JJKrVsNzOFn82jS0I0zw\nELEVENLABS_API_KEY=\nOPENAI_API_KEY=\nYOUTUBE_API_KEY=AIzaSyBQgQQTzGh_pG9_4hSdJ7xCwTB-HcE1qQM\nTIKTOK_TOKEN=\nINSTAGRAM_TOKEN=\n",
    "yedekler/hafiza.json": "{\"gecmis\": [{\"emir\": \"cizgileri kirmizi yap\"}, {\"emir\": \"çizgileri mavi yap\"}], \"faz\": \"FAZ 1 KURUCU TAMAMLANDI\", \"youtube\": \"ON\", \"tarih\": \"09-08-2026\", \"master\": \"balaliemre2017@gmail.com\"}",
    "yedekler/auth.json": "{\"master\": {\"email\": \"balaliemre2017@gmail.com\", \"phone\": \"\"}, \"youtube\": {\"username\": \"balaliemre2017@gmail.com\", \"token\": \"AIzaSyBQgQQTzGh_pG9_4hSdJ7xCwTB-HcE1qQM\"}, \"instagram\": {\"username\": \"balaliemre2017@gmail.com\"}, \"tiktok\": {\"username\": \"balaliemre2017@gmail.com\"}, \"facebook\": {\"username\": \"balaliemre2017@gmail.com\"}}"
}

for rel, content in DUMP.items():
    p=BASE/rel
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        print(f"OLUŞTURULDU (yoktu): {rel}")
    else:
        # VARSA BIRLEŞTIR, SILME!
        try:
            if rel.endswith('.json'):
                old=json.loads(p.read_text(encoding='utf-8'))
                new=json.loads(content)
                # Merge: eski korunur, yeni eklenir
                merged={**new, **old}
                # ic ice dict merge icin master
                if 'master' in old and 'master' in new:
                    merged['master']={**new['master'], **old['master']}
                p.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding='utf-8')
                print(f"BIRLEŞTIRILDI (korundu): {rel}")
            elif rel.endswith('.env'):
                # ENV merge
                old_keys={}
                for l in p.read_text(encoding='utf-8', errors='ignore').splitlines():
                    if '=' in l and not l.strip().startswith('#'):
                        k,v=l.split('=',1)
                        old_keys[k.strip()]=v.strip()
                new_keys={}
                for l in content.splitlines():
                    if '=' in l:
                        k,v=l.split('=',1)
                        new_keys[k.strip()]=v.strip()
                merged={**new_keys, **old_keys}  # eski ustun
                p.write_text('\n'.join([f"{k}={v}" for k,v in merged.items()])+'\n', encoding='utf-8')
                print(f"ENV BIRLEŞTIRILDI: {list(merged.keys())}")
        except Exception as e:
            print(f"Birleştirme hatası {rel}: {e} - korunuyor")

# 2. Eski panel/app.py yedeğini al
panel_path=BASE/'panel'/'app.py'
if panel_path.exists():
    backup=BASE/'panel'/f'app.py.backup_{os.getpid()}'
    shutil.copy(panel_path, backup)
    print(f"Panel yedek: {backup}")

print("=== RESTORE BITTI - HERSEY KORUNDU ===")
