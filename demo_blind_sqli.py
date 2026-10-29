# ============================================================
# DEMO WEB #2 - "SI PELIT" (BLIND SQL INJECTION)
# Web ini DIAM: apa pun input salah, notifnya sama. Tidak ada error.
# Celahnya tetap ada, tapi cuma ketahuan lewat JEDA WAKTU (web jadi lemot).
#
# Tampilan sengaja dibedakan dari Web #1 (tema & warna beda).
# Ganti mode lewat alamat:  /mode/aman   atau   /mode/rentan
#
# Install : py -m pip install flask
# Jalankan: py demo_blind_sqli.py
# Buka    : http://127.0.0.1:5055
# ============================================================

from flask import Flask, request, render_template_string, session, redirect
import sqlite3
import os
import time

app = Flask(__name__)
app.secret_key = "kunci-demo-pelit"
DB_FILE = "demo_pelit.db"


def jeda(detik):
    """Fungsi SQL buatan untuk meniru SLEEP()/WAITFOR, dibatasi maks 6 detik."""
    time.sleep(min(float(detik), 6))
    return 1


def setup_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE peserta (
        nis INTEGER, username TEXT, password TEXT,
        nama TEXT, jurusan TEXT, status TEXT
    )""")
    cur.executemany("INSERT INTO peserta VALUES (?,?,?,?,?,?)", [
        (1,  "admin",  "P4nitiaSeleksi!", "Panitia Seleksi",  "-",               "-"),
        (2,  "rizky",  "rizky2026",       "Rizky Maulana",    "Teknik Komputer", "DITERIMA"),
        (3,  "sari",   "sari2026",        "Sari Wulandari",   "Multimedia",      "CADANGAN"),
        (4,  "fajar",  "fajar2026",       "Fajar Nugroho",    "Teknik Komputer", "DITOLAK"),
        (5,  "dinda",  "dinda2026",       "Dinda Lestari",    "Akuntansi",       "DITERIMA"),
        (6,  "bayu",   "bayu2026",        "Bayu Ananda",      "Multimedia",      "DITERIMA"),
        (7,  "nadia",  "nadia2026",       "Nadia Salsabila",  "Akuntansi",       "CADANGAN"),
        (8,  "reza",   "reza2026",        "Reza Pratama",     "Teknik Komputer", "DITERIMA"),
        (9,  "vina",   "vina2026",        "Vina Oktaviani",   "Multimedia",      "DITOLAK"),
        (10, "galih",  "galih2026",       "Galih Permadi",    "Akuntansi",       "DITERIMA"),
    ])
    conn.commit()
    conn.close()


def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.create_function("JEDA", 1, jeda)
    return conn


# ---------------------------------------------------------------
#  TAMPILAN  (tema teal, layout beda dari Web #1)
# ---------------------------------------------------------------
STYLE = """
<style>
  :root{
    --bg:#eef3f4; --card:#ffffff; --ink:#0e1f24; --muted:#5b6c72;
    --line:#dce5e7; --brand:#0d9488; --brand-d:#0b7268; --accent:#f0fdfa;
    --ok:#15803d; --danger:#be123c; --ring:rgba(13,148,136,.16);
  }
  *{box-sizing:border-box;}
  body{
    font-family:'Segoe UI',-apple-system,Roboto,Helvetica,sans-serif;
    color:var(--ink); margin:0; min-height:100vh; padding:48px 16px;
    background:
      linear-gradient(180deg,#e7f1f0,transparent 240px), var(--bg);
    display:flex; align-items:flex-start; justify-content:center;
  }
  .wrap{width:100%; max-width:430px;}
  .wrap.wide{max-width:880px;}

  .card{background:var(--card); border:1px solid var(--line); border-radius:12px;
    overflow:hidden; box-shadow:0 12px 30px rgba(14,31,36,.10);}
  .cardhead{background:linear-gradient(100deg,var(--brand),var(--brand-d));
    color:#fff; padding:24px 28px; display:flex; align-items:center; gap:14px;}
  .mark{width:42px; height:42px; border-radius:9px; background:rgba(255,255,255,.18);
    border:1px solid rgba(255,255,255,.35); display:flex; align-items:center;
    justify-content:center; font-weight:800; letter-spacing:1px; font-size:16px;}
  .cardhead h1{font-size:17px; margin:0;}
  .cardhead p{font-size:12.5px; margin:2px 0 0; opacity:.9;}
  .cardbody{padding:28px;}

  label{font-size:12px; color:var(--muted); font-weight:600; text-transform:uppercase;
    letter-spacing:.5px; display:block; margin:16px 0 6px;}
  label:first-child{margin-top:0;}
  input{width:100%; padding:11px 13px; border:1px solid var(--line); border-radius:8px;
    font-size:14px; color:var(--ink); background:#fbfefe; outline:none; transition:.15s;}
  input:focus{border-color:var(--brand); box-shadow:0 0 0 3px var(--ring);}
  button{width:100%; margin-top:22px; padding:12px; border:none; cursor:pointer;
    border-radius:8px; font-size:14px; font-weight:700; color:#fff; background:var(--brand);
    transition:.15s;}
  button:hover{background:var(--brand-d);}

  .msg{margin-top:16px; padding:11px 13px; border-radius:8px; font-size:13px;
    background:var(--accent); border:1px solid #bdeae3; color:#0b5f57;}

  .alt{margin-top:18px; text-align:center; font-size:13px;}
  a.link{color:var(--brand); text-decoration:none; font-weight:600;}
  a.link:hover{text-decoration:underline;}

  h2{font-size:18px; margin:0 0 2px;}
  p.sub{color:var(--muted); font-size:13px; margin:0;}
  .scroll{overflow-x:auto; border:1px solid var(--line); border-radius:10px; margin-top:16px;}
  table{width:100%; border-collapse:collapse; font-size:13px;}
  thead th{background:#f1f7f6; color:var(--muted); font-weight:600; text-align:left;
    padding:10px 12px; white-space:nowrap;}
  tbody td{padding:10px 12px; border-top:1px solid var(--line); white-space:nowrap;}
  tbody tr:hover{background:#fafefd;}
  .kv{display:flex; justify-content:space-between; padding:11px 2px;
    border-bottom:1px solid var(--line); font-size:14px;}
  .kv span:first-child{color:var(--muted);}
  .badge{font-size:12px; padding:3px 10px; border-radius:20px; font-weight:600;}
  .b-ok{background:#dcfce7; color:#166534;} .b-cad{background:#fef9c3; color:#854d0e;}
  .b-no{background:#ffe4e6; color:#9f1239;}
</style>
"""

LOGIN_TEMPLATE = STYLE + """
<div class="wrap">
  <div class="card">
    <div class="cardhead">
      <div class="mark">SA</div>
      <div><h1>Portal Akademik</h1><p>Sistem Informasi Seleksi</p></div>
    </div>
    <div class="cardbody">
      <form method="POST">
        <label>Username</label>
        <input type="text" name="username" autofocus autocomplete="off" placeholder="Nama pengguna">
        <label>Password</label>
        <input type="password" name="password" autocomplete="off" placeholder="Kata sandi">
        <button type="submit">Masuk</button>
      </form>
      {% if pesan %}<div class="msg">{{ pesan }}</div>{% endif %}
      <p class="alt"><a class="link" href="/cek">Cek status pendaftaran</a></p>
    </div>
  </div>
</div>
"""

CEK_TEMPLATE = STYLE + """
<div class="wrap">
  <div class="card">
    <div class="cardhead">
      <div class="mark">SA</div>
      <div><h1>Cek Status Pendaftaran</h1><p>Masukkan nomor induk peserta</p></div>
    </div>
    <div class="cardbody">
      <form method="GET">
        <label>Nomor Induk (NIS)</label>
        <input name="nis" value="{{ nis }}" autofocus autocomplete="off" placeholder="contoh: 2">
        <button type="submit">Cek</button>
      </form>
      {% if pesan %}<div class="msg">{{ pesan }}</div>{% endif %}
      {% if hasil %}
      <div class="scroll">
        <table>
          <thead><tr><th>Nama</th><th>Jurusan</th><th>Status</th></tr></thead>
          <tbody>
          {% for r in hasil %}<tr><td>{{ r[3] }}</td><td>{{ r[4] }}</td><td>{{ r[5] }}</td></tr>{% endfor %}
          </tbody>
        </table>
      </div>
      {% endif %}
      <p class="alt"><a class="link" href="/">Kembali ke halaman masuk</a></p>
    </div>
  </div>
</div>
"""

ADMIN_TEMPLATE = STYLE + """
<div class="wrap wide">
  <div class="card">
    <div class="cardhead">
      <div class="mark">PN</div>
      <div><h2>Panel Panitia</h2><p class="sub" style="color:#e6fffb">Data seluruh peserta (Total {{ semua|length }})</p></div>
    </div>
    <div class="cardbody">
      <div class="scroll">
        <table>
          <thead><tr>
            <th>Nama</th><th>NIS</th><th>Jurusan</th><th>Status</th><th>Username</th><th>Password</th>
          </tr></thead>
          <tbody>
          {% for s in semua %}
            <tr>
              <td>{{ s[3] }}</td><td>{{ s[0] }}</td><td>{{ s[4] }}</td><td>{{ s[5] }}</td>
              <td>{{ s[1] }}</td><td style="font-family:monospace">{{ s[2] }}</td>
            </tr>
          {% endfor %}
          </tbody>
        </table>
      </div>
      <p class="alt" style="text-align:left"><a class="link" href="/logout">Keluar</a></p>
    </div>
  </div>
</div>
"""

DASH_TEMPLATE = STYLE + """
<div class="wrap">
  <div class="card">
    <div class="cardhead">
      <div class="mark">SA</div>
      <div><h2>{{ u[3] }}</h2><p class="sub" style="color:#e6fffb">{{ u[4] }}</p></div>
    </div>
    <div class="cardbody">
      <div class="kv"><span>NIS</span><span>{{ u[0] }}</span></div>
      <div class="kv"><span>Jurusan</span><span>{{ u[4] }}</span></div>
      <div class="kv"><span>Status</span><span>{{ u[5] }}</span></div>
      <p class="alt" style="text-align:left"><a class="link" href="/logout">Keluar</a></p>
    </div>
  </div>
</div>
"""

# Pesan SAMA untuk semua kondisi -> inilah yang bikin web ini "pelit".
PESAN_SERAGAM = "Permintaan diterima. Jika data valid, sistem akan menindaklanjuti."


@app.route("/mode/<pilih>")
def ganti_mode(pilih):
    session["mode"] = "aman" if pilih == "aman" else "rentan"
    return redirect(request.referrer or "/")


@app.route("/", methods=["GET", "POST"])
def login():
    mode = session.get("mode", "rentan")
    pesan = None

    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        conn = get_conn()
        cur = conn.cursor()
        user = None
        try:
            if mode == "rentan":
                query = f"SELECT * FROM peserta WHERE username = '{u}' AND password = '{p}'"
                cur.execute(query)
            else:
                cur.execute("SELECT * FROM peserta WHERE username = ? AND password = ?", (u, p))
            user = cur.fetchone()
        except sqlite3.Error:
            user = None            # error DITELAN, tak pernah tampil ke layar
        conn.close()

        if user:
            session["user"] = user
            return redirect("/dashboard")
        pesan = PESAN_SERAGAM      # gagal apa pun sebabnya -> pesan sama

    return render_template_string(LOGIN_TEMPLATE, pesan=pesan)


@app.route("/cek")
def cek():
    mode = session.get("mode", "rentan")
    nis = request.args.get("nis", "")
    pesan, hasil = None, []

    if nis != "":
        conn = get_conn()
        cur = conn.cursor()
        try:
            if mode == "rentan":
                query = f"SELECT * FROM peserta WHERE nis = {nis}"
                cur.execute(query)
            else:
                cur.execute("SELECT * FROM peserta WHERE nis = ?", (nis,))
            hasil = cur.fetchall()
        except sqlite3.Error:
            hasil = []
        conn.close()
        if not hasil:
            pesan = PESAN_SERAGAM

    return render_template_string(CEK_TEMPLATE, pesan=pesan, hasil=hasil, nis=nis)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    user = session["user"]
    if user[1] == "admin":
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM peserta WHERE username != 'admin'")
        semua = cur.fetchall()
        conn.close()
        return render_template_string(ADMIN_TEMPLATE, semua=semua)
    return render_template_string(DASH_TEMPLATE, u=user)


@app.route("/logout")
def logout():
    mode = session.get("mode", "rentan")
    session.clear()
    session["mode"] = mode
    return redirect("/")


if __name__ == "__main__":
    setup_database()
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5055"))
    print(f"Web #2 'si pelit' jalan di http://{host}:{port}  (Ctrl+C untuk berhenti)")
    app.run(host=host, port=port, debug=False)
