# Cara bikin web ini ONLINE (gratis, tanpa laptop sendiri jadi server)

Dua web:
  Web 1 "cerewet" = APP web1   |   Web 2 "pelit" = APP web2

Catatan jujur: kamu tetap harus login ke akun hostingmu sendiri dan klik
"deploy" di browser. Tidak ada cara aman meng-online-kan tanpa langkah itu.

====================================================================
CARA TERMUDAH: RENDER + upload lewat web GitHub (tanpa install git)
====================================================================
1. Buat akun gratis di github.com (kalau belum punya).
2. Klik "New repository" -> kasih nama (misal: demo-sqli-les) -> Create.
3. Di halaman repo kosong, klik "uploading an existing file".
   Drag SEMUA file di folder ini ke situ, lalu "Commit changes".
4. Buat akun gratis di render.com, pilih "Sign in with GitHub".
5. Render -> New -> "Blueprint" -> pilih repo tadi -> Apply.
   (render.yaml otomatis bikin DUA web sekaligus.)
6. Tunggu ~2 menit. Render kasih 2 link https:
     nando.onrender.com
     bima.onrender.com
   Bagikan link itu ke murid. Jalan di server Render, bukan laptopmu.

Catatan: free tier Render "tidur" kalau nganggur; akses pertama agak
lambat ~30 detik, itu normal.

====================================================================
ALTERNATIF SUPER CEPAT buat sesi les langsung: ngrok (tanpa hosting)
====================================================================
1. py demo_login_sqli.py        (biarkan jalan)
2. ngrok http 5050              (dapat link https publik sementara)
Link pakai domain ngrok, bukan IP-mu. Tutup terminal = link mati.

## Keamanan (sekaligus bahan ajar)
- Semua data FIKTIF. Jangan pakai data asli.
- Web ini sengaja bocor -> matikan/hapus service-nya kalau sudah selesai.
