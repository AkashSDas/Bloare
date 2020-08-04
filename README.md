# Bloare

### 🔥 Bloare 👉 <ins>Blo</ins>g where we sh<ins>are</ins>

## 📝 Table of contents

*  [About](#about)
*  [Installation](#installation)
*  [License](#license)


## About

- Blog app build using **Django Framework** for backend, **Jinja2** template & **HTML CSS3 & Vanilla JavaScript** for frontend

- Key Features:
  - **🔐 Custom Authentication** (SignUp, Login, Logout, Password Reset using Email)
  - **😎 User Profile**
  - **📝 Posts** (Create, Update, Delete)
  - **🍻 Comments** on Post & **Replies** on Comment
  - **👍 Likes** & **👎 Dislikes** system for a post
  - **Pagination**


## Installation

>It is  **recommended** to use **`virtual enviroment`** for this project to avoid any issues related to dependencies.

> All dependencies are in requirements.txt file
 
Here **`pipenv`** is used for this project.

- First, start by closing the repository
```bash
git clone https://github.com/AkashSDas/Bloare
```

- Start by installing **`pipenv`** if you don't have it
```bash
pip install pipenv
```

- Once installed, access the venv folder inside the project folder

```bash
cd  Bloare/venv/
```

- Create the virtual environment

```bash
pipenv install
```

The **Pipfile** of the project must be for creating replicating project's virtual enviroment.

This will install all the dependencies and create a **Pipfile.lock** (this should not be altered).

- Enable the virtual environment

```bash
pipenv shell
```

- Go to source file directory

```bash
cd src/
```

- Start the server

```bash
python manage.py runserver
```

### 🔐 Password Reset Setup

- Go to the config folder

```bash
cd Bloare/venv/src/config
```

- Open **`email_info.py`** file & set your email & its password credentials

```python
EMAIL_HOST_USER = 'your@gmail.com'
EMAIL_HOST_PASSWORD = 'gmail-password'
```

## License

This project is licensed under the MIT License - see the [MIT LICENSE](LICENSE) file for details.
