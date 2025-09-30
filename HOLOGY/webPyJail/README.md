# `webPyJail`
Category : Web
## 🗒️ Description
> I hope I patched all the unintended ways...
---
## 🪄 Solution Steps
Pada soal kali ini kita disajikan sebuah web. Web ini memiliki satu halaman utama dengan sebuah kolom input yang meminta kita untuk memasukkan ekspresi Python. Tujuannya terlihat jelas: melakukan jailbreak dari lingkungan Python yang terbatas untuk membaca flag di server. Namun disini kita tidak diperbolehkan untuk memasukkan beberapa text antara lain : 
- Tanda kurung (())
- Garis bawah (_)
- Tanda kutip (' dan ")

Dan juga di runner.py terdapat code membuat kita tidak bisa  mengakses ke semua fungsi dan modul bawaan Python : 
```python
def main():
    expr = sys.stdin.read(30000)
    expr = expr.strip()

    safe_globals = {"__builtins__": None} # 
    safe_locals = {}

    try:
        out = eval(expr, safe_globals, safe_locals)
        print(repr(out))
    except Exception as e:
        print(f"[error] {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
```

Setelah mencoba beberapa payload dan gagal, akhirnya saya menemukan sesuatu yang menarik dan itu berada di Dockerfile, yaitu: 
```
COPY . /var/www/html/
```

Dimana arti dari code ini adalah menginstruksikan Docker untuk menyalin semua file dan folder (.) dari direktori build ke dalam direktori root server web (/var/www/html/). Sehingga otomatis kita bisa langsung mengambil flag.txt lewat path. Dan yap kita dapatkan flagnya : 

<img width="504" height="121" alt="image" src="https://github.com/user-attachments/assets/d41d898c-03cb-48a4-a8c0-b997a1493cdd" />
