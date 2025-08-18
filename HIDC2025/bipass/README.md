# `bipass`
Category : Web
## 🗒️ Description
> watdehel, many type of bipass.
---
## 🪄 Solution Steps
Di soal kali ini kita diberikan sebuah halaman login dan untuk step pertama kita lihat terlebih dahulu source code halaman ini karena biasanya akan selalu ada petunjuk dari situ. 
Setelah view page source kita akan menemukan : 

```html
<button id="showSourceBtn" style="display:none" onclick="showSource()">Show Backend Source</button>
```
Dan kita juga bisa melihat isi dari function showSource()
```javascript
function showSource() {
    window.open('depan/source.html', '_blank');
}
```

Dari sini kita bisa tahu bahwa kita dapat melihat sebuah source code digunakan untuk halaman ini. Maka dari itu langsung saja kita halaman /depan/source.html dan kita akan mendapatkan :

<img width="829" height="499" alt="Screenshot 2025-08-17 154605" src="https://github.com/user-attachments/assets/96e57cfe-8e75-40bd-a3f7-f320b96787cb" />

Kita diberikan source code untuk auth, dan dari code itu kita bisa hit endpoint auth seperti ini :

<img width="779" height="153" alt="image" src="https://github.com/user-attachments/assets/c8a089fe-d54f-405a-bd97-5792cddf50bd" />

Command diatas adalah curl yg dimana request body nya sudah kita encode. Disini terdapat dua celah pada pengecekan username dan password. Celah pertama ada di username, Ketika PHP membandingkan dua data dengan tipe data yang berbeda menggunakan ==, ia akan mencoba "memaksa" agar tipe datanya sama. Saat membandingkan string dengan angka (integer), PHP akan mengubah string itu menjadi angka. Jika stringnya diawali angka (misal "123apel"), ia akan diubah menjadi 123.
Jika stringnya tidak diawali angka (seperti "hidc_admin"), ia akan diubah menjadi 0. Disini karena kita mengirim sebuah data integer 0, maka server akan membandingkan 0 dengan $USER, jika kemungkinan $USER sebuah string adalah benar maka $USER akan diubah menjadi 0. Lalu celah berikutnya ada di pengecekan password, sebelumnya saya sudah sempat melakukan command seperti ini :

<img width="771" height="144" alt="image" src="https://github.com/user-attachments/assets/bb761c69-ecc8-4776-be4d-ae8a643fd5e5" />

Dan muncul response 
```
<b>Fatal error</b>:  Uncaught TypeError: strcmp(): Argument #1 ($string1) must be of type string, array given in /var/www/html/belakang/auth.php:19
Stack trace:
#0 /var/www/html/belakang/auth.php(19): strcmp(Array, '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8')
#1 {main}
  thrown in <b>/var/www/html/belakang/auth.php</b> on line <b>19</b><br />
```

Dan sangat jelas kita diberikan value dari $PASSWORD_SHA256.
Lalu kita akan dapat flagnya
 > HIDC2025{b1p4ss1ng_is_easy}

