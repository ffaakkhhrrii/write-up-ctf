# `Dark side of asteroid`
Category : Web
## 🗒️ Description
> something seems wrong??????
---
## 🪄 Solution Steps
Pada soal kali ini kita diberikan sebuah website yang memberikan catalog dari asteroid, dimana kita juga harus login dan register. Untuk step pertama kita melakukan register dan login terlebih dahulu untuk mengecek kira kira apakah ada halaman yang dapat dijadikan sebuah hint. Dan setelah login terdapat halaman Profile yang bisa melakukan input url sebuah image. Lalu setelah mengecek seluruh halaman langsung saja kita analisis source code yang diberikan.

Dan ditemukan beberapa kesimpulan yaitu : 
- Flag disimpan di dalam tabel admin_secrets dengan access_level = 3
- Terdapat endpoint /internal/admin/search yang tampaknya dapat mengakses tabel admin_secrets.
- Endpoint /profile dapat digunakan untuk mengunggah foto profil dari sebuah URL. Code ini menggunakan requests.get(photo_url) untuk mengambil konten dari URL yang diberikan. Ini adalah kandidat kuat untuk SSRF. Terdapat filter is_private_url yang mencoba mencegah akses ke alamat IP internal.

Maka dari itu, untuk saat ini next step kita adalah membuat query sqli pada endpoint internal. Karena eksekusi query pada endpoint itu menggunakan f-string. Dan payload yang dapat kita gunakan adalah %'/**/AND/**/access_level/**/LIKE/**/'3'/**/–. Jika di inject akan menjadi seperti ini.

```
SELECT ... FROM admin_secrets WHERE secret_name LIKE '%'/**/AND/**/access_level/**/LIKE/**/'3'/**/--' AND access_level <= 2
```

Lalu selanjutnya kita akan membuat payload url yang akan diinput ke endpoint profile. Namun ada beberapa hal lagi yang harus kita lakukan yaitu : 

- Membuat url internal yang include dengan query injection yang kita buat.
- Membuat URL publik yang sah ke server.
- Meloloskan filter is_private_url yang di implemen pada endpoint profile.
- Server publik tersebut kemudian merespons dengan HTTP Redirect 302 yang mengarahkan server target ke URL internal yang kita inginkan.
- Library requests secara default akan mengikuti redirect ini, sehingga server target akhirnya mengakses 127.0.0.1.

Pertama kita buat terlebih dahulu url internal yang sudah include dengan query injection, dan akan menjadi seperti ini http%3A%2F%2F127.0.0.1%3A5000%2Finternal%2Fadmin%2Fsearch%3Fq%3D%25%27%2F%2A%2A%2FAND%2F%2A%2A%2Faccess_level%2F%2A%2A%2FLIKE%2F%2A%2A%2F%273%27%2F%2A%2A%2F--


Disini sudah saya URL-encode agar bisa dipakai di parameter httpbin.org. Lalu selanjutnya akan kita gabungkan dengan url httpbin, dan akan menjadi seperti ini.

https://httpbin.org/redirect-to?url=http%3A%2F%2F127.0.0.1%3A5000%2Finternal%2Fadmin%2Fsearch%3Fq%3D%25%27%2F%2A%2A%2FAND%2F%2A%2A%2Faccess_level%2F%2A%2A%2FLIKE%2F%2A%2A%2F%273%27%2F%2A%2A%2F--

Lalu langsung saja kita kembali ke web, dan masuk ke halaman profile dan akan mendapatkan flagnya
