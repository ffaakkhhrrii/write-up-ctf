# `ezzz jail`
Category : Miscellanous
## 🗒️ Description
> just your normal ez jail.
---
## 🪄 Solution Steps
Dalam tantangan ini, kita diberikan sebuah program Python di dalam environment sandbox. Tujuannya adalah untuk mencegah kita mengakses sistem. Misi kita adalah mencari celah keamanan dalam batasan-batasan tersebut agar bisa membaca isi file flag.txt.

Setelah dilakukan analisis didapatkan beberapa hal berikut : 
- Menggunakan RestrictedPython untuk mengeksekusi kode.
- Sebuah daftar panjang built-in exceptions standar (EXCEPTIONS_TO_REMOVE) dihapus dari __builtins__.
- Fungsi print() tidak tersedia secara efektif, karena RestrictedPython mengubahnya menjadi _print_() yang tidak terdefinisi, hal ini juga terjadi ke getattr dan type.
- Hint #1: Fungsi open() yang asli dan tidak dibatasi secara sengaja ditambahkan kembali ke __builtins__. Ini adalah indikasi kuat bahwa kita harus membaca file.
- Hint #2: Terdapat blok try...except Exception as e: print(f"Error: {e}"). Ini memberitahu kita bahwa satu-satunya cara untuk mendapatkan output adalah dengan memicu (raise) sebuah exception dan membiarkan server mencetaknya untuk kita.
- Menggunakan image python:3.11-slim. Ini krusial, karena perilaku dan fitur built-in Python bisa berbeda antar versi.
- Menyalin flag.txt ke direktori kerja /app. Ini mengkonfirmasi lokasi file flag adalah 'flag.txt'.

Setelah mencoba beberapa payload ditemukan lah payload akhir yang dapat digunakan yaitu : 
```python
raise ExceptionGroup(open('flag.txt').read(), [error])
```

Payload ini dapat digunakan karena pada python versi 3.11, memperkenalkan dua built-in exception baru sebagai bagian dari fitur Exception Groups (PEP 654):
- ExceptionGroup
- BaseExceptionGroup

Maka dari itu langsung saja kita encode payload ini menjadi base64 dan masukkan kedalam input, dan yap

<img width="777" height="114" alt="image" src="https://github.com/user-attachments/assets/2f888d06-6e41-4659-a31a-d23cbc200a85" />
