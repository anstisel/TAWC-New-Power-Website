# CITS3200
New Power Forum Website
By Elisha Anstiss, Benedyct Liew, Esther Lee, Jiahao Liang, Sean Sutton and Sohail Kharrazi. 
  
Please read Installation Guide for information on how to open this project.   
In short:  
Git clone to computer.     
have python3 installed (test by terminal: python3 --version).    
have node.js installed (test by terminal: node -v).     
have npm installed (for use of vue software) (test by terminal: npm -v).     
In terminal (inside TAWC-New-Power folder):        
  LINUX:  
    cd backend.      
    python3 -m venv venv.    
    source venv/bin/activate.    
    pip install -r requirements.txt.    
    python3 -m populate_db.         
    flask run.       
  WINDOWS:   
    cd backend.    
    python -m venv venv.    
    venv/Scripts/activate.     
    pip install -r requirements.txt.      
    python -m populate_db.py.    
    flask run.     
In NEW terminal (inside TAWC-New-Power folder):      
  cd frontend.    
  npm install.     
  npm run dev.    
       
click on the Local host URL provided (likely "http://localhost:5001").    
Play around with the website.   
 Submit posts and comments and watch them be posted to one's profile page.   
Login as an admin using:   
  Email: admin@coolmail.com.      
  Password: Th3_B0ss.           
Admin can approve or reject posts, once having done so you can see how the posts are pushed to the discussion board so other users can view and interact with the posts.   
   
-----------------------------------------------------------------------------------  
  
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
$ sudo apt-get -y update. 
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
