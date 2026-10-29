# ============================================================
# JALANKAN DUA WEB SEKALIGUS (satu perintah)
#
#   py jalankan_semua.py
#
# Web 1 (cerewet) -> http://127.0.0.1:5050
# Web 2 (pelit)   -> http://127.0.0.1:5055
#
# Tekan Ctrl+C untuk menghentikan keduanya.
# ============================================================

import threading
import demo_login_sqli as web1
import demo_blind_sqli as web2

if __name__ == "__main__":
    web1.setup_database()
    web2.setup_database()

    # Web 1 jalan di thread terpisah, Web 2 di thread utama.
    t = threading.Thread(
        target=lambda: web1.app.run(host="127.0.0.1", port=5050, use_reloader=False),
        daemon=True,
    )
    t.start()

    print("Web 1 (cerewet) -> http://127.0.0.1:5050")
    print("Web 2 (pelit)   -> http://127.0.0.1:5055")
    print("Tekan Ctrl+C untuk berhenti.")
    web2.app.run(host="127.0.0.1", port=5055, use_reloader=False)
