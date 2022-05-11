# Welcome to the I/O Store! :convenience_store: :100:

## Development Environment
1. `Python v3.10.4`
1. Python virtual environment containing requirements from `requirements.txt` file (`Django` is included there)

## Development workflow

### Standard acronyms to start a commit message:
* API: an (incompatible) API change
* BENCH: changes to the benchmark suite
* BLD: change related to building iostore
* BUG: bug fix
* DEP: deprecate something, or remove a deprecated object
* DEV: development tool or utility
* DOC: documentation
* ENH: enhancement
* MAINT: maintenance commit (refactoring, typos, etc.)
* REV: revert an earlier commit
* STY: style fix (whitespace, PEP8)
* TST: addition or modification of tests
* REL: related to releasing iostore

example: `BUG: fixed the `foo` function bug from issue #1234`

## Django
### How to run the Django server?
1. open terminal (ctrl + `)
1. navigate to the folder containing `manage.py` file and run: 
```bash
py manage.py runserver
```
1. open your browser and type the url: 
```browser
localhost:8000
```

### How to Update DB?
TODO: Complete Instructions

### Tips

* When you start a new app with `Django` don't forget to add it to `apps.py` file and add the name of the class to the `INSTALLED_APP`.
* It is better practice to keep most of the logic in `models.py` and not `views.py` (will result less db io)

## Python Virtual Environment (venv)

### Some Terminal Commands
> :warning: You can click `copy to clipboard` button and just paste in terminal

#### Before Activating Environment

```bash
py -m venv venv                             # Create a virtual environment
```
```bash
py -m venv venv --upgrade-deps              # Update core dependencies
```
```bash
venv\Scripts\activate                       # Activate the virtual environment
```

#### After Activating Environment
```bash
deactivate                                  # Deactivate the virtual environment
```
```bash
pip install -r requirements.txt --upgrade   # Update packages for activated env
```

### Install new Python package

1. add the package and desired version to the requirements.txt file
2. run
```bash
pip install -r requirements.txt --upgrade
```
3. Tell the rest of the team so they will update their env as well :)

## Git

### Setting up your credentials
In order to commit changes to git, you must configure name and email.
After opening a `GitHub` account you will get a pseudo email, that will route to the email you logged in `GitHub` with, so you don't have to put your personal email open for public.
To configure your credentials open `GIT Bash` and enter the following commands:
```bash
git.config --global user.name "John wick"
```
```bash
git.config --global user.email "john.wick@gmail.com"
```

## Encountering "WTF?!!" Issues?
1. Rerun `Django` server
1. Refresh page and clear cache on browser using ctrl + shift + r

## Tutorials
* [Python Django 7 Hour Course](https://youtu.be/PtQiiknWUcI) by Traversy Media
* [Django Tutorials](https://youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p) by Corey Schafer
* [Python Tutorial: VENV (Windows)](https://youtu.be/APOPm01BVrk) by Corey Schafer

## Documentations
* [Django v4.x Documentation](https://docs.djangoproject.com/en/4.0/)

## References

