# BlindVison Camera Detection Tool
**A Python-based application that uses OCR to detect text via a camera and convert it into speech.**


---

## Table of Contents  
1. [How to Download](#🟢-how-to-download)  
2. [How to Use](#🔵-how-to-use)  
3. [Features in Update v1.1](#🟢-update-v11)  
4. [Using Your Own Database](#🟠-if-you-want-to-use-source-own-database)  
5. [Database Options](#🔴-if-you-dont-have-database)  
6. [FAQ](#❓faq)

---


## 🟢 How to Download  
Download the script from [GitHub](https://github.com/esi0077/OCR):  

```bash
git clone https://github.com/esi0077/OCR.git
```

### 🔵 How to use 

first you need to install dependencies by using

```bash
 pip install -r requirements.txt
```
### 🟢 update V1.1

Auto-installation in main app of requirements no need to install dependencies manually anymore.

### 🟠 if you want to use source (own database)

> simply open the python file , edit line 68 to 75 or search for mydb and edit that part and build it with your database.

> if you dont want to build the app you can run it by this command 

```bash
python main.py
```

### 🔴 if you dont have database 

> A pre-built version of the app (with a database) is included in the main folder.

> Simply run the .exe file to start using the application.

### 🟣 Connect it to your database

To connect to a database:

 1. Copy the SQL commands from the db.sql file.
 2. Paste them into your database program.

<hr>
you can use this databases 
<br>
<br>

- [XAMPP](https://www.apachefriends.org) - Windows  
- [WAMP](https://www.wampserver.com/en/) - Windows and Linux  
- [MariaDB](https://mariadb.com/) - Windows and Linux

<br>
<br>
you can read this tutarial for learning how to setup ubunto on rasberry pi and install mariadb

[link](https://github.com/esi0077/catalog_with_database)

<hr>



### ❓FAQ

#### what is OCR ?
> Optical character recognition that can scan words and convert it to digital words.

#### What does this app ?

> The app/source helps you with typing words by using camera and convert it to speach 




