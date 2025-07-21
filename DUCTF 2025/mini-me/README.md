# `mini-me`
Category : Web
## 🗒️ Description
> The app looks scrambled and full of brainrot! But ther's more than meets the eye. Dive into the code, connect the dots, and see if you can uncover what's really going on behind the scenes, or right at the front!
---
## 🪄 Solution Steps
- We are given a website, where we can login, without any username/email and password that we have to look up. Where after login there will be a brainrot display.
- First, I checked the provided zip file. It contains an `app.py` file that functions as a route from the website.<br/>

### ``app.py``

```py
from flask import Flask, render_template, send_from_directory, request, redirect, make_response
from dotenv import load_dotenv

import os
load_dotenv()
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
FLAG = os.getenv("FLAG")

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    return redirect("/confidential.html")

@app.route("/confidential.html")
def confidential():
    return render_template("confidential.html")


@app.route("/admin/flag", methods=["POST"])
def flag():
    key = request.headers.get("X-API-Key")
    if key == API_SECRET_KEY:
        return FLAG
    return "Unauthorized", 403

```
### ``index.html``
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>EmailCTF Login</title>
  <link rel="stylesheet" href="/static/css/style.css" />
</head>
<body>
  <div class="login-container">
    <h1>EmailCTF Webmail</h1>
    <form method="POST" action="/login">
      <input type="text" placeholder="Email" required />
      <input type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
  <script src="/static/js/main.min.js"></script>
</body>
</html>

```
### ``confidential.html``
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Confidential</title>
  <link rel="stylesheet" href="/static/css/style.css" />
</head>
<body>
  <div id="audio-warning">
    ⚠️ This experience contains sound. Please ensure your volume is adjusted appropriately.
  </div>

  <button id="start-btn">Begin Experience</button>

  <div id="dancer"></div>
  
  <img id="dancer-img" src="/static/ballerina-cappucina/ballerina-cappucina.png" alt="Ballerina" />

  <audio id="balletAudio" preload="auto">
    <source src="/static/ballerina-cappucina/ballerina-cappucina.mp3" type="audio/mpeg" />
  </audio>

  <script src="/static/js/main.min.js"></script>
</body>
</html>
```
From some of the code, there is a clue, that we have to hit the ``/admin/flag`` endpoint with the POST method, along with the X-API-KEY header. Therefore, our current goal is to find out how to get the API KEY.
- If we examine further, there are two files that are not included in the zip by the author, namely ``/static/css/style.css`` and ``/static/js/main.min.js``. And so, let's take a look through inspect
<img width="298" height="86" alt="image" src="https://github.com/user-attachments/assets/4d33d31e-54ab-4e57-9abd-3d9dd524fb52" />

- And after I identified the two files. There is one file that is quite strange, namely in the `main.min.js` section.\
```js
function pingMailStatus() {
    fetch("/api/mail/status")
}
function fetchInboxPreview() {
    fetch("/api/mail/inbox?limit=5")
}
pingMailStatus(),
fetchInboxPreview(),
document.getElementById("start-btn")?.addEventListener("click", () => {
    document.getElementById("balletAudio").play(),
    document.getElementById("start-btn").style.display = "none",
    document.getElementById("audio-warning").style.display = "none";
    let i = document.getElementById("dancer")
      , o = document.getElementById("dancer-img")
      , l = (i.style.display = "block",
    o.style.display = "block",
    0)
      , a = window.innerWidth / 2
      , d = window.innerHeight / 2;
    !function e() {
        l += .05;
        var t = a + 100 * Math.cos(l)
          , n = d + 100 * Math.sin(l);
        i.style.left = t + "px",
        i.style.top = n + "px",
        o.style.left = t + "px",
        o.style.top = n + "px",
        requestAnimationFrame(e)
    }()
}
);
//test map file -> test-main.min.js.map, remove in prod 
```
- There is a comment, `test map file -> test-main.min.js.map, remove in prod`. Honestly, since I'm very new to ctf, I thought this comment wouldn't play a big role, and I was definitely wrong haha. That file has a big role for me to find the API KEY.
- Therefore, just access `https://web-mini-me-ab6d19a7ea6e.2025.ductf.net/static/js/test-main.min.js.map`, and the file will be automatically downloaded.
```js
function qyrbkc() { 
    const xtqzp = ["85"], vmsdj = ["87"], rlfka = ["77"], wfthn = ["67"], zdqo = ["40"], yclur = ["82"],
          bpxmg = ["82"], hkfav = ["70"], oqzdu = ["78"], nwtjb = ["39"], sgfyk = ["95"], utxzr = ["89"],
          jvmqa = ["67"], dpwls = ["73"], xaogc = ["34"], eqhvt = ["68"], mfzoj = ["68"], lbknc = ["92"],
          zpeds = ["84"], cvnuy = ["57"], ktwfa = ["70"], xdglo = ["87"], fjyhr = ["95"], vtuze = ["77"], awphs = ["75"];
        const dhgyvu = [xtqzp[0], vmsdj[0], rlfka[0], wfthn[0], zdqo[0], yclur[0], 
                    bpxmg[0], hkfav[0], oqzdu[0], nwtjb[0], sgfyk[0], utxzr[0], 
                    jvmqa[0], dpwls[0], xaogc[0], eqhvt[0], mfzoj[0], lbknc[0], 
                    zpeds[0], cvnuy[0], ktwfa[0], xdglo[0], fjyhr[0], vtuze[0], awphs[0]];

    const lmsvdt = dhgyvu.map((pjgrx, fkhzu) =>
        String.fromCharCode(
            Number(pjgrx) ^ (fkhzu + 1) ^ 0 
        )
    ).reduce((qdmfo, lxzhs) => qdmfo + lxzhs, ""); 
    console.log("Note: Key is now secured with heavy obfuscation, should be safe to use in prod :)");
}
```
- To get the key, we change the javascript code, to also console log variable lmsvdt, so that the key that has been obfuscated is reconverted into plain text, and we get `TUNG-TUNG-TUNG-TUNG-SAHUR`.
- And the next step is definitely we hit the endpoint `/admin/flag`
<img width="1479" height="125" alt="image" src="https://github.com/user-attachments/assets/324dbb4b-4a80-496b-ab30-6da3021eaac6" />
We get the flag🚩🚩
