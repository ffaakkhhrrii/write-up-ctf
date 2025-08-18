# `Magic_library`
Category : Web
## 🗒️ Description
> Raya Lucaria is a majestic academy that stands in the midst of a mist-shrouded lake.
---
## 🪄 Solution Steps
Di soal kali ini kita diberikan sebuah web statis untuk akademi sihir. Dan tidak ada source code yang mencurigakan, maka dari itu kita langsung check ke resource soal yang diberikan. Ada beberapa file yang bisa dijadikan sebuah hint yaitu

- Dockerfile: Memberikan informasi penting tentang lingkungan server. Flag berada di RUN echo "HIDC2025{find_me}" > /flag.txt. Kemudian izin file flag diatur ke 644, yang berarti pengguna web server (www-data) dapat membacanya.
- File PHP: Beberapa file PHP mendefinisikan class-class berikut: Library, Member, Loan, dan Book.

Petunjuk penting berada di Member.php dan index.php

index.php <br>
<img width="652" height="241" alt="Screenshot 2025-08-17 193718" src="https://github.com/user-attachments/assets/7fd2a780-e5e2-4342-bf91-359c8e9faa09" />

Membuktikan bahwa cookie library data akan di unserialize.

Member.php <br>
<img width="915" height="271" alt="Screenshot 2025-08-17 193922" src="https://github.com/user-attachments/assets/961f8bf8-da24-4435-86dd-576f8596ce67" />

Di class member php menggunakan function system dan akan di echo, sehingga kita bisa menjalankan command shell. Yang kita butuhkan sekarang adalah base64 payload yang berisi command cat /flag.txt dan sudah di serialize. Maka dari itu kita bisa membuat sebuah script:

<img width="705" height="967" alt="Screenshot 2025-08-17 194221" src="https://github.com/user-attachments/assets/07808fe3-7cbd-4754-9d07-969ba4f44aee" />

Setelah itu jalankan dan kemudian base64 yang kita dapatkan, kita letakkan di cookie yang ada pada web F12 -> Application -> Cookies. Dan nanti dibagian atas halaman web akan muncul flagnya.

> HIDC2025{r4ya_luc4r1a_15_p34k}
