# Getaway
#### Getaway for a Smart Field project

Authored by: [Rivka](https://www.linkedin.com/in/rivka-gozlan/), [Miri](https://www.linkedin.com/in/miri-zakay-3b5a521aa/), Elisheva and Shir
<br/><br/>
#### ==Description==
This project is a sub-project for a "Smart Field" project.<br/>
(The other two sub-projects: [Cloud-to-Ground](https://github.com/sheindyfr/Cloud-to-Ground)), <br/>
The main project simulates a smart filed. The sensors (-IOT devices) transmit a lot of data (temperature, rainfall, etc.) to a client side- the 'GETWAY', and it transmits the necessary information to a server side- the cloud, that updates them in a DATABASE.<br/>
The goal of our project is to compress the data so that no load and duplication is created.<br/>
For this purpose, in our program, we are testing whether the data should be updated according to the deviation values that the user enters and then, using Data Compression Algorithm - the information is sent to the cloud.
<br/><br/>
#### ==Program Files==
**GWmanager.py-** User input and GETAWAY activation.<br/>
**Getaway.py-** Server and client, including data processing.<br/>
**Mat.py-** Realize a matrix for the data storage.<br/>
**Delta.py-** Data storage for limited sending to the cloud.

**client.py, server.py-** Simulations of the other two sub-projects.
<br/><br/>
#### ==How to compile?==
Open three command line, one of them runs the command: python GWmanager.py<br/>
Then insert data there according to the instructions. In the second- the command: python server.py (or [Cloud-to-Ground](https://github.com/sheindyfr/Cloud-to-Ground) program).<br/>
In the third- the command: python client.py (or the program of group 1)

If you do not run the Group 1 program but the client.py:<br/>
Enter a set of threshold values in the third instance, an example:<br/>
10,11,20,21.2,30,31,40,41,50,51,60,61,70,71,80,81,90,91,100,101<br/>
Then messages from the sensors, example message:<br/>
10,20,30,40,50,60,70,80,8,90,100,1,1,0

![Running image](https://github.com/rivkagozlan/Getaway/blob/master/Running%20image.JPG)
