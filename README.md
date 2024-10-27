## **Distraction Prevention App**
Please note: An iOS device and MacBook Pro has been used throughout the entire development process. The installation on windows may be slightly different to Mac.A local database was created, meaning it was unable to be added to the GitHub. Steps have been provided below to demonstrate how to install the MongoDB database and add a user for login. If installation does not work, a video of demonstrating the app has been included in the submission folder.

# **Instructions for installation**
To install the project, please follow these steps:
1. Clone the Github repository 'https://github.com/jl2357/MobileSystems-MobileApp'
2. cd into the project folder 'cd PWA_MobileSys'
3. Install dependencies 'pip install -r requirements.txt' or 'pip3 install -r requirements.txt'
4. Obtain computer's IPv4 address by following these steps: https://www.avast.com/c-how-to-find-ip-address 
5. Replace all IPv4 addresses on the session.js and app.py file with the current computer's IPv4 address. For example, under sendFrames() in session.js, change the HTTP request http://192.168.1.150:5500/process_frames to http://<Your_IPv4_Address>:5500/process_frames. Do this for all HTTP addresses in session.js and app.py
6. Run the flask server 'python3 app.py'
7. To access the PWA on a mobile device, open a browser and type 'http://<Your_IPv4_Address>:5500' in the address bar. 
8. Add the app to the device's home screen
9. The app should be accessible from the home screen

# **Important Note**
Media capture may not be available on the browser (Due to running on an HTTP site). Thus, media capture needs to be enabled for the camera to work. 
If using an iOS device and MacBook:
1. Open the app, remain on the login page
2. Plug the iOS device into the macbook
3. Open a safari browser
4. Under the develop tab, choose the connected device and click on the app's link
5. A developer window should open, click on the small phone icon on the top left corner
6. A list of options should open, check the box 'allow media capture on insecure sites'

# **Enable database on Mac** 
A local database was used. To enable this and add logins
1. Install mongodb 'brew tap mongodb/brew'
2. Install mongo community 'brew install mongodb-community'
3. Start mongodb 'brew services start mongodb-community'
4. Confirm mongodb is running run 'brew services list'
5. Open another terminal, run 'mongosh'
6. Keep these two windows running
7. Since a register feature is unavailable, to add a login, download the Postman platform desktop. 
8. Sign in to Postman and POST the login username and password by setting the method to POST and using the HTTP request 'http://<Your_IPv4_Address>:5500/users'.
