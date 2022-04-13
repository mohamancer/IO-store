# Development Environment Setup

I have found this way for configuring the environment we need to be the easiest.
Nevertheless you are welcome to use any tool you like as long you use the following versions:
* `Python v3.10.x`
* Python virtual environment containing requirements from `requirements.txt` file
* `Node.js v16.14.2`
* Softwares, Packages and frameworks stated at `packge.json` file


## Python Environment

First download and install [Python 3.10.x](https://www.python.org/downloads/)
> :warning: If you choose to custom install, make sure you install `pip` in the process

1. run `Windows PowerShell` as administrator (right click -> run as administrator)
2. run the commands:
    ```Windows PowerShell
    Set-ExecutionPolicy Unrestricted
    Y
    ```
3. exit the `Windows PowerShell` as admin and reopen not as admin
4. Navigate to the project directory
1. run the commands:
    ```Windows PowerShell
    py -m venv venv                     # Create the virtual environment
    venv\Scripts\activate               # Activate the virtual environment
    pip install -r requirements.txt     # Install required packages (Django, Pillow, etc.)
    ```
And your done!


## JavaScript Environment

> :warning: It is always recommended to **remove any existing installations of Node.js or npm** from your operating system before installing a version manager as the different types of installation can lead to strange and confusing conflicts.

1. install [nvm-windows](https://github.com/coreybutler/nvm-windows)
1. run `Windows Power Shell` as an administrator (right click -> run as administrator)
1. run the following command:
```nvm-windows
nvm install 16.14.2
nvm use 16.14.2
```


## Git

### Setting up your credentials
In order to commit changes to git, you must configure name and email.
After opening a `GitHub` account you will get a pseudo email, that will route to the email you logged in `GitHub` with, so you don't have to put your personal email open for public.
To configure your credentials open `GIT Bash` and enter the following commands:
```
git.config --global user.name "John wick"
git.config --global user.email "john.wick@gmail.com"
```


## VSCode

[Download VSCode](https://code.visualstudio.com/Download)
Clone the repository, and open the folder with VSCode

Select the python environment for our project:
1. click `ctrl + shift + p`
1. search for `Python: Select Interperter`
1. choose the environment we have created (called `venv`)

installing frontend environment:
1. open terminal in VSCode (click ctrl + `)
1. navigate to `...\iostore\frontend\` dictionary
1. run the command: `npm install`


## Finally!
From now on we can use VSCode for all our needs, everything is in the integrated terminal, just click ctrl + `


## References

* [Install NodeJS on Windows](https://docs.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-windows)