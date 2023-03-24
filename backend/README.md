# Flask Dev

Flask should be run using a virtual environment in Python, but this virtual environment isn't stored in the git repository, instead you can load it with the following steps.

## Deployment
The proper server will run on gunicorn.
```
gunicorn -b localhost:5000 -w 4 new_power:app
```

## Demodat admin
U: admin@coolmail.com
P: Th3_B0ss

## Initial Setup

### Linux
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Windows
```
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```
If you get an error saying that running scripts is disabled on this system, run the following then try again
```
$ Set-ExecutionPolicy Unrestricted -Scope Process
```
### Both - DB Initialisation
Linux & probably OSX
```
python3 -m populate_db
```
Windows
```
python -m populate_db.py
```

We had an issue on windows where `python3 -m populate_db` would use the global interpreter rather than the virtual environment.
Not sure if anyone has verified everything works on Mac yet.

## Using the Virtual Environment

Once the virtual environment is up (`source venv/bin/activate` or `venv/Scripts/activate`), you can run code in several ways.
1. `flask run` once the app is created to run it.
2. Set vscode (or your IDE) to the venv interpreter to run your code there.
2. Run a file with the venv: `python3 -m <file>`

## Updating Packages

Packages will be added to the virtual environment, so it's important to make sure you have the most up to date set.

### Updating your local set of packages

Simply activate the virtual environment and run
```
pip install -r requirements.txt
```

### Adding new packages

If you need additional packages installed first install them to the venv with pip, then save them to requirements.txt with
```
pip freeze -r requirements.txt
```