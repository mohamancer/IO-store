# Welcome to the I/O Store! :convenience_store: :100:

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


## How to run the project?
1. open terminal (ctrl + `)
1. navigate to the `...\iostore\frontend` directory
1. build the project running the command: `npm run dev`
1. open another terminal (ctrl + Shift + `)
1. navigate to the folder containing `...\iostore\manage.py` and run: `py manage.py runserver`
1. open your browser and type the url: `localhost:8000`

There is no need to follow these instructions every time you make changes, usually it will update automatically.

### encounter any problems?
1. kill all terminals (click on the garbage can icon for each terminal)
1. remove all the content from `..\iostore\frontend\static\frontend\` directory
1. rerun the project as stated above

## Python

### Run environment
1. open `Windows PowerShell`
1. navigate to the project home directory
1. run the command:
    ```
    venv\Scripts\activate
    ```
In order to deactivate, simply run:
```
deactivate
```

### Upgrade Python packages

1. [run the environment](#run-the-environment)
1. run the command: 
    ```
    pip install -r requirements.txt --upgrade
    ```

### Install new Python package

1. add the package and desired version to the requirements.txt file
1. [Upgrade Python packages](#upgrade-python-packages)

### Upgrade Python's virtual environment core dependencies

1. open `Windows PowerShell`
1. navigate to the project home directory
1. run the command:
    ```
    py -m venv venv --upgrade-deps
    ```
Referenced from `venv` documentation [^1]

### Tutorials
* [venv](https://youtu.be/APOPm01BVrk)

## Django
* When you startapp with `Django` don't forget to go to the new app `apps.py` file and add the name of the class to the `INSTALLED_APP`.
* It is better to keep most of the logic in `models.py` and not `views.py`

## TypeScript
In order to use `tsc` write `npx tsc` in the terminal

## Documentations
* [npm Documentation](https://docs.npmjs.com/)
* [Django v4.x Documentation](https://docs.djangoproject.com/en/4.0/)

## References
* [Django REST with React](https://www.valentinog.com/blog/drf/#Django_REST_with_React_Django_and_React_together)
* [Setting up Django and React](http://v1k45.com/blog/modern-django-part-1-setting-up-django-and-react/)
* [Django & React - Full Stack Web App Tutorial](https://youtube.com/playlist?list=PLzMcBGfZo4-kCLWnGmK0jUBmGLaJxvi4j)
* [Full Stack React & Django](https://youtube.com/playlist?list=PLillGF-RfqbbRA-CIUxlxkUpbq0IFkX60)

[^1]: https://docs.python.org/3.10/library/venv.html#creating-virtual-environments
