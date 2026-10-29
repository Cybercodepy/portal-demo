# Entry-point untuk hosting (Render/Railway/dll).
# Pilih web mana yang dijalankan lewat environment variable APP:
#   APP=web1 -> demo_login_sqli  (si cerewet)
#   APP=web2 -> demo_blind_sqli  (si pelit)
# Default: web1
import os

which = os.environ.get("APP", "web1").lower()
if which == "web2":
    import demo_blind_sqli as m
else:
    import demo_login_sqli as m

m.setup_database()     # siapkan database fiktif saat start
app = m.app            # gunicorn mencari variabel bernama 'app'
