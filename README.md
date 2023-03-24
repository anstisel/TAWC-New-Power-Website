# CITS3200
New Power Forum Website

In development Create an issue with a description then create a branch on that issue and devlop in there. Merge once finished.

# Running Tests

Selenium test is in the testing folder. These testing will use geckodriver which is for firefox. To run the tests you will need to 
start up the server so everything is running. The testing will be looking for `'http://localhost:5001/'` To start the tests run:

Windows:
```
python testing\selenium_tests.py
```
Unix:
```
python3 testing\selenium_tests
```
*do message if these commands don't work, Idk the actual command for unix systems.

# Development
For development, see the README.mds in frontend and backend.

# Deployment
This application is ready to be deployed on an nginx server.
These instructions are customised for linux, but are applicable to other operating systems.
To do this, follow these steps:
1. Install all dependencies
```
$ sudo apt-get -y update
$ sudo apt-get -y install python3 python3-venv python3-dev
$ sudo apt-get -y install nginx git
```
2. git clone the project
3. Configure the backend
```
cd backend
source venv/bin/activate
pip install -r requirements.txt
python3 -m populate_db //demo data
python3 -m "from app import db; db.create_all()" // load empty db
```
4. Configure nginx
```
sudo rm /etc/nginx/sites-enabled/default
```
And copy the new_power.conf file to /etc/nginx/sites-enabled or wherever your nginx serves sites from.
Modify the certificate location in the new_power.conf file, and the dist location.
5. Run the backend and nginx
```
sudo nginx
cd backend
gunicorn -b localhost:8000 -w 4 new_power:app
```
See `https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux`
## References

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world