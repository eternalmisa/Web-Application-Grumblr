**url: http://ec2-52-33-198-15.us-west-2.compute.amazonaws.com**

##About this homework:
    Homework 6: Deployment                      
    BY:                                              
       Pan Li (AndrewID:panli)                    
       Electrical and Computer Engineering        
       Carnegie Mellon University                 
    DATE/Version:                                    
       Novemeber 14th, 2015 - V 1.0  

### Details of this application:  
####1.Project file list:
	000-default.conf 
			(the configuration file for AWS-EC2 ubuntu instance for this app)
    webapps/webapps
    	_init_.py 					_init_.pyc
    	settings.py *				settings.pyc
    	urls.py	*					urls.pyc
    	wsgi.py						wsgi.pyc
    webapps/media
    	avatar/
    	picture/ 		
    webapps/grumblr
    	_init_.py					_init_.pyc
    	admin.py					admin.pyc
    	models.py *					models.pyc
    	tests.py
    	urls.py	*					urls.pyc
    	views.py	*				views.pyc
    	forms.py 	*				forms.pyc
    	migrations/
    	static/ *
    		grumblr/ 
    			css/ 
    				bootstrap/	
    				base.css
    				login.css
    				stream.css
    				profile.css
    				edit.css
    			images/
    			js/
    				grumblr.js *
    	templates/ *
    		grumblr/
    			base.html
    				base_login.html
    					login.html
    					registration.html
    					send_email.html
    					reset_password.html
    				base_stream.html
    					global_stream.html
    					follower_stream.html
    				base_profile.html
    					self_profile.html
    					other_profile.html
    					block_profile.html
    				base_edit.html
    					edit_profile.html
    					change_password.html
	
####2.The process of Deployment:
######Part1 Using MySQl as database:
	As for this homework, I change my database from sqlite3 to MySQL and the only thing I need to do is modified the settings.py.
	DATABASES = {
    	'default': {
       		'ENGINE': 'django.db.backends.mysql',
        	'NAME': 'grumblr',
        	'USER': 'root',
        	'PASSWORD':'',
        	'HOST': 'localhost',
       		'PORT': '3306',
    	}
    }
	After that, using "mysql -uroot -p" command line to visit mysql and create a database for this project. And use makemigrations and migrate to create the database schema:
	• python manage.py makemigrations grumblr
	• python manage.py migrate
	Right now, I can use MySQL as the database to store data for my application. 
	
	(Using the following code to parse SECRET_KEY and the password of MySQL:
	with open('/home/ubuntu/6/webapp/webapps/password.txt','r') as file:
    	data=[]
    	for line in file:
        	data.append(line.strip())
    *password.txt store all of the password.)
######Part2 deployment on AWS EC2 server:    
     
    (1) AWS account Registeration and Launch instance
    First of all, I create an AWS account and creat a Key Pair named "eternalmisa.pem". After that, I launch a new new EC2 instance, which has the Public DNS @ec2-52-33-198-15.us-west-2.compute.amazonaws.com and using "Ubuntu" as the operating system.
    
    (2) Login the AWS instance using SSH
    Using command line "ssh –i  ~/eternalmisa.pem ubuntu@ec2-52-33-198-15.us-west-2.compute.amazonaws.com" to login the AWS instance.
    
    (3) Installing software in instance
    a. sudo apt-get install apache2
    b. sudo apt-get install libapache2-mod-wsgi
    c. sudo apt-get install python-django
    d. sudo apt-get install python-pip
    e. sudo apt-get install python-dev
    f. pip install PIL --allow-external PIL --allow-unverified PIL
    g. sudo pip install -U Django
    h. sudo apt-get install mysql-server python-mysqldb
    
    (4) Configure the enviroment of apache
    Go to /etc/apache2/sites-available/000-default.conf and change the site configuration of apache as below:
    WSGIScriptAlias / /home/ubuntu/6/webapp/webapp/wsgi.py        <Directory /home/ubuntu/6/webapp/webapps>                <Files wsgi.py>                        Require all granted                </Files>        </Directory>    
    (5) Add the application into apache
    Using command line ""sudo vi /etc/apache2/apache2.conf" and add "WSGIPythonPath /home/ubuntu/6/webapp" at last to add this application into apache.
    
    (6) Modified the urls.py for accessing static files
    According to the previous steps, I can access to the app with the url, but all of the static files are lost, like css, images and javascript. Therefore, I add these lines to my project urls.py (../webapps/urls.py):
    from django.conf import settings
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.contrib.staticfiles.urls import static
    urlpatterns += staticfiles_urlpatterns()
    
    (7) Modified the permisson
    In order to using some default setting, like default avatar, I need to modified some file's perrssion using command line "chmod 777 default.jpg"
    
    (8) Create database on ubuntu instance
    Like the part1, I create a database named "grumblr" for my application. And use makemigrations and migrate to create the database schema.
    
    (9) Restart the apache and visit the web site
    Right now, all of the configuration has been done. Using "sudo service apache2 restart" to restart the apache and type "ec2-52-33-198-15.us-west-2.compute.amazonaws.com" in the browser, you can visit my Grumblr.

####3.Existing users in Database:	
	[Note: The password of all of the users is "123".]
	etrnalmisa, why, sherry, Tina
