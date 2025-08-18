# `Wat-Now`
Category : Web
## 🗒️ Description
> You got login page, but do you know wat to do?
---
## 🪄 Solution Steps
Disini kita diberikan halaman login lagi, dan setelah kita cek source code nya adalah, fitur login ini di secure menggunakan wasm. Tapi karena secure menggunakan wasm itu dijalankan dari sisi client, jadi kita bisa coba langsung saja menggunakan curl

<img width="1465" height="703" alt="Screenshot 2025-08-17 195413" src="https://github.com/user-attachments/assets/13a61471-e7b5-4160-8b20-da57fadceff6" />

Dan yap, ternyata benar, jika kita langsung login menggunakan curl tidak ada sama sekali validasi yg harus kita bobol, jadi langsung saja kita jalankan curl get ke halaman dashboard.

<img width="1464" height="58" alt="Screenshot 2025-08-17 195537" src="https://github.com/user-attachments/assets/b41402da-7b09-4368-af03-68e4bf1e2cb6" />

Dan nanti flag akan muncul

> HIDC{N0w_Y0u_KnoOW_WAT_tO_Do}
