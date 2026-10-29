# ============================================================
# DEMO KELAS: LOGIN RENTAN SQL INJECTION  (Web #1 - "si cerewet")
# Untuk pelajaran Keamanan & Integritas Data.
#
# - Semua data FIKTIF, database lokal, direset tiap program dijalankan.
# - Server hanya bisa diakses dari komputer ini (127.0.0.1).
# - Tampilan: halaman login biasa. Kontrol guru disembunyikan di "Mode Guru".
# - Masuk sebagai admin -> kebuka panel berisi SELURUH data siswa.
#
# Install : py -m pip install flask
# Jalankan: py demo_login_sqli.py
# Buka    : http://127.0.0.1:5050
# ============================================================

from flask import Flask, request, render_template_string, session, redirect
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "kunci-demo-kelas"
DB_FILE = "demo_sekolah.db"


def setup_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE siswa (
        username TEXT, password TEXT, nama TEXT, nis TEXT,
        kelas TEXT, nilai_rata TEXT, alamat TEXT, no_hp TEXT
    )""")
    cur.executemany("INSERT INTO siswa VALUES (?,?,?,?,?,?,?,?)", [
        ("admin",  "Adm1nSekolah!", "Administrator TU", "-", "-", "-", "Ruang Tata Usaha", "-"),
        ("andi",     "andi2026",     "Andi Pratama",       "2026001", "XI RPL 1", "84", "Jl. Mawar No. 1",      "0812-3345-1101"),
        ("bunga",    "bunga2026",    "Bunga Lestari",      "2026002", "XI RPL 1", "91", "Jl. Melati No. 7",     "0813-7788-2202"),
        ("citra",    "citra2026",    "Citra Dewi",         "2026003", "XI RPL 2", "78", "Jl. Kenanga No. 3",    "0857-1122-3303"),
        ("dimas",    "dimas2026",    "Dimas Saputra",      "2026004", "XI RPL 2", "88", "Jl. Anggrek No. 9",    "0821-4455-4404"),
        ("eka",      "eka2026",      "Eka Fitriani",       "2026005", "XI TKJ 1", "90", "Jl. Cempaka No. 12",   "0812-9090-5505"),
        ("farhan",   "farhan2026",   "Farhan Hidayat",     "2026006", "XI TKJ 1", "82", "Jl. Flamboyan No. 5",  "0838-3344-6606"),
        ("gita",     "gita2026",     "Gita Permata",       "2026007", "XI TKJ 2", "86", "Jl. Dahlia No. 21",    "0877-5566-7707"),
        ("hadi",     "hadi2026",     "Hadi Kurniawan",     "2026008", "XI MM 1",  "75", "Jl. Teratai No. 4",    "0813-2211-8808"),
        ("indah",    "indah2026",    "Indah Purnama",      "2026009", "XI MM 1",  "93", "Jl. Seroja No. 8",     "0852-7788-9909"),
        ("joko",     "joko2026",     "Joko Santoso",       "2026010", "XI MM 2",  "80", "Jl. Bougenville No.2", "0812-6677-1010"),
        ("kirana",   "kirana2026",   "Kirana Maharani",    "2026011", "XII RPL 1","95", "Jl. Mawar No. 15",     "0819-3344-1111"),
        ("lukman",   "lukman2026",   "Lukman Hakim",       "2026012", "XII RPL 1","79", "Jl. Melati No. 22",    "0812-8899-1212"),
        ("mira",     "mira2026",     "Mira Anggraini",     "2026013", "XII TKJ 1","87", "Jl. Kenanga No. 30",   "0856-1234-1313"),
        ("nanda",    "nanda2026",    "Nanda Prakoso",      "2026014", "XII TKJ 1","83", "Jl. Anggrek No. 18",   "0813-4321-1414"),
        ("okta",     "okta2026",     "Okta Ramadhan",      "2026015", "XII MM 1", "89", "Jl. Cempaka No. 27",   "0821-5678-1515"),
        ("putri",    "putri2026",    "Putri Ayu Wulan",    "2026016", "XII MM 1", "92", "Jl. Flamboyan No.11",  "0877-8765-1616"),
        ("rendi",    "rendi2026",    "Rendi Firmansyah",   "2026017", "X RPL 1",  "77", "Jl. Dahlia No. 6",     "0852-2468-1717"),
        ("sinta",    "sinta2026",    "Sinta Rahmawati",    "2026018", "X RPL 1",  "85", "Jl. Teratai No. 19",   "0812-1357-1818"),
    ])
    conn.commit()
    conn.close()


STYLE = """
<style>
  :root{
    --bg1:#eef2ff; --bg2:#f8fafc; --card:#ffffff; --ink:#0f172a;
    --muted:#64748b; --line:#e5e9f2; --brand:#3b55e6; --brand2:#6d28d9;
    --ok:#15803d; --danger:#dc2626; --ring:rgba(59,85,230,.18);
  }
  *{box-sizing:border-box;}
  body{
    font-family:'Segoe UI',-apple-system,Roboto,Helvetica,sans-serif;
    color:var(--ink); margin:0; min-height:100vh; padding:40px 16px;
    background:
      radial-gradient(900px 500px at 15% -10%, #dbe4ff 0%, transparent 55%),
      radial-gradient(900px 500px at 110% 10%, #ede9fe 0%, transparent 50%),
      linear-gradient(180deg, var(--bg1), var(--bg2));
    display:flex; align-items:flex-start; justify-content:center;
  }
  .wrap{width:100%; max-width:420px;}
  .wrap.wide{max-width:900px;}

  /* kartu login */
  .login-card{
    background:var(--card); border:1px solid var(--line); border-radius:18px;
    padding:36px 32px; box-shadow:0 20px 45px rgba(30,41,99,.12);
  }
  .brand{display:flex; flex-direction:column; align-items:center; text-align:center; margin-bottom:26px;}
  .logo{
    width:56px; height:56px; border-radius:16px; margin-bottom:14px;
    background:linear-gradient(135deg,var(--brand),var(--brand2));
    display:flex; align-items:center; justify-content:center;
    color:#fff; font-size:26px; box-shadow:0 8px 18px var(--ring);
  }
  .brand h1{font-size:19px; margin:0 0 3px; letter-spacing:.2px;}
  .brand p{font-size:13px; color:var(--muted); margin:0;}

  label{font-size:12.5px; color:var(--muted); font-weight:600; display:block; margin:16px 0 6px;}
  input{
    width:100%; padding:12px 14px; border:1.5px solid var(--line); border-radius:11px;
    font-size:14px; color:var(--ink); background:#fbfcff; outline:none; transition:.15s;
  }
  input:focus{border-color:var(--brand); background:#fff; box-shadow:0 0 0 4px var(--ring);}
  button{
    width:100%; margin-top:22px; padding:13px; border:none; cursor:pointer;
    border-radius:11px; font-size:14.5px; font-weight:700; color:#fff;
    background:linear-gradient(135deg,var(--brand),var(--brand2));
    box-shadow:0 10px 20px var(--ring); transition:.15s;
  }
  button:hover{filter:brightness(1.05); transform:translateY(-1px);}

  .msg{margin-top:16px; padding:11px 13px; border-radius:10px; font-size:13px;}
  .msg.gagal{background:#fef2f2; color:var(--danger); border:1px solid #fecaca;}
  .msg.error{background:#fffbeb; color:#b45309; border:1px solid #fde68a;}

  .foot{text-align:center; color:var(--muted); font-size:11.5px; margin-top:18px;}

  /* panel setelah login */
  .panel{background:var(--card); border:1px solid var(--line); border-radius:18px;
    padding:30px; box-shadow:0 18px 40px rgba(30,41,99,.10);}
  .phead{display:flex; align-items:center; gap:14px; margin-bottom:6px;}
  .phead .logo{width:46px; height:46px; border-radius:13px; font-size:22px; margin:0;}
  h2{font-size:20px; margin:0;}
  p.sub{color:var(--muted); font-size:13px; margin:2px 0 0;}
  .banner{background:#fef2f2; color:var(--danger); border:1px solid #fecaca;
    padding:11px 14px; border-radius:11px; font-size:13px; margin:18px 0;}
  .scroll{overflow-x:auto; border:1px solid var(--line); border-radius:12px;}
  table{width:100%; border-collapse:collapse; font-size:13px;}
  thead th{background:#f3f6fd; color:var(--muted); font-weight:600; text-align:left;
    padding:11px 12px; white-space:nowrap; position:sticky; top:0;}
  tbody td{padding:10px 12px; border-top:1px solid var(--line); white-space:nowrap;}
  tbody tr:hover{background:#fafbff;}
  td.bocor{color:var(--ink); font-family:'Consolas',monospace;}
  .logo{font-weight:800; letter-spacing:1px; font-size:20px;}
  .kv{display:flex; justify-content:space-between; padding:12px 2px; border-bottom:1px solid var(--line); font-size:14px;}
  .kv span:first-child{color:var(--muted);}
  a.link{color:var(--brand); font-size:13px; text-decoration:none; font-weight:600;}
  a.link:hover{text-decoration:underline;}

  .guru{margin-top:22px; border-top:1px dashed var(--line); padding-top:14px;}
  .guru summary{cursor:pointer; font-size:12px; color:var(--muted); list-style:none;}
  .guru summary:hover{color:var(--ink);}
  pre{background:#0f172a; color:#e2e8f0; padding:13px; border-radius:10px;
    font-size:12px; white-space:pre-wrap; word-break:break-all; margin:10px 0 0;}
</style>
"""

LOGIN_TEMPLATE = STYLE + """
<div class="wrap">
  <div class="login-card">
    <div class="brand">
      <div class="logo">PS</div>
      <h1>Portal Siswa</h1>
    </div>
    <form method="POST">
      <label>Username</label>
      <input type="text" name="username" autofocus autocomplete="off" placeholder="Masukkan username">
      <label>Password</label>
      <input type="password" name="password" autocomplete="off" placeholder="Masukkan password">
      <button type="submit">Masuk</button>
    </form>
    {% if pesan %}<div class="msg {{ jenis }}">{{ pesan }}</div>{% endif %}
  </div>
</div>
"""

ADMIN_TEMPLATE = STYLE + """
<div class="wrap wide">
  <div class="panel">
    <div class="phead">
      <div class="logo">TU</div>
      <div>
        <h2>Panel Administrasi</h2>
        <p class="sub">Data Siswa (Total {{ semua|length }} siswa)</p>
      </div>
    </div>
    <div class="scroll">
      <table>
        <thead><tr>
          <th>Nama</th><th>NIS</th><th>Kelas</th><th>Nilai</th>
          <th>No. HP</th><th>Alamat</th><th>Username</th><th>Password</th>
        </tr></thead>
        <tbody>
        {% for s in semua %}
          <tr>
            <td>{{ s[2] }}</td><td>{{ s[3] }}</td><td>{{ s[4] }}</td><td>{{ s[5] }}</td>
            <td>{{ s[7] }}</td><td>{{ s[6] }}</td>
            <td>{{ s[0] }}</td><td class="bocor">{{ s[1] }}</td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
    </div>
    <p style="margin-top:18px"><a class="link" href="/logout">Keluar</a></p>
  </div>
</div>
"""

DASHBOARD_TEMPLATE = STYLE + """
<div class="wrap">
  <div class="panel">
    <div class="phead">
      <div class="logo">PS</div>
      <div>
        <h2>{{ user[2] }}</h2>
        <p class="sub">{{ user[4] }}</p>
      </div>
    </div>
    <div style="margin-top:14px">
      <div class="kv"><span>NIS</span><span>{{ user[3] }}</span></div>
      <div class="kv"><span>Kelas</span><span>{{ user[4] }}</span></div>
      <div class="kv"><span>Nilai rata-rata</span><span>{{ user[5] }}</span></div>
      <div class="kv"><span>No. HP</span><span>{{ user[7] }}</span></div>
      <div class="kv"><span>Alamat</span><span>{{ user[6] }}</span></div>
    </div>
    <p style="margin-top:18px"><a class="link" href="/logout">Keluar</a></p>
  </div>
</div>
"""


@app.route("/mode/<pilih>")
def ganti_mode(pilih):
    session["mode"] = "aman" if pilih == "aman" else "rentan"
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def login():
    mode = session.get("mode", "rentan")
    pesan, jenis, query, params = None, "gagal", None, None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        user = None
        try:
            if mode == "rentan":
                # SALAH: input pengguna langsung ditempel ke dalam teks SQL.
                query = f"SELECT * FROM siswa WHERE username = '{username}' AND password = '{password}'"
                cur.execute(query)
            else:
                # BENAR: input dikirim sebagai parameter, bukan bagian dari SQL.
                query = "SELECT * FROM siswa WHERE username = ? AND password = ?"
                params = (username, password)
                cur.execute(query, params)
            user = cur.fetchone()
        except sqlite3.Error as e:
            pesan = f"Error database: {e}"
            jenis = "error"
        conn.close()

        if user:
            session["user"] = user
            session["query"] = query
            return redirect("/dashboard")
        if pesan is None:
            pesan = "Username atau password salah."

    return render_template_string(LOGIN_TEMPLATE, mode=mode, pesan=pesan,
                                  jenis=jenis, query=query, params=params)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    user = session["user"]
    query = session.get("query")
    mode = session.get("mode", "rentan")

    # Kalau yang masuk akun admin -> tampilkan panel berisi SELURUH data siswa.
    if user[0] == "admin":
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM siswa WHERE username != 'admin'")
        semua = cur.fetchall()
        conn.close()
        return render_template_string(ADMIN_TEMPLATE, semua=semua, query=query)

    return render_template_string(DASHBOARD_TEMPLATE, user=user, query=query, mode=mode)


@app.route("/logout")
def logout():
    mode = session.get("mode", "rentan")
    session.clear()
    session["mode"] = mode
    return redirect("/")


if __name__ == "__main__":
    setup_database()
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5050"))
    print(f"Demo jalan di http://{host}:{port}  (Ctrl+C untuk berhenti)")
    app.run(host=host, port=port, debug=False)
