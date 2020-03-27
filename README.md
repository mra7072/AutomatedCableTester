# AutomatedCableTester

Installation -

Please install the following dependecnies before proceeding. 

OS 
- Raspbian Buster
This system  is 100% functional on this OS and has not been tested on different platforms. However, minor adjustsment may be needed in when installing the following dependecies. Choose your OS specific configurations when installing the following dependencies. 

SW Dependencies
- Python >=3.0 https://www.python.org/downloads/
- pyvisa https://pyvisa.readthedocs.io/en/1.8/getting.html

Python Library dependecies 
- tkinter https://tkdocs.com/tutorial/install.html
- RPI (GPIO Library) https://www.raspberrypi-spy.co.uk/2012/05/install-rpi-gpio-python-library/
- smbus (I2C Library) https://skpang.co.uk/blog/archives/575


For Users 
1. Download this repository and save to directory of your choice
2. Navigate to AutomatedCableTester/gui.py
3. Execute script to start GUI either by double-clicking script or through a command line interface by running "Python3 gui.py". System can be configured to run program on boot by editing your /rc.local enviorment 


For Developers
1.Clone this repository either through HTTP/SSH to the directory of your choice. Instructions to do this can be found here.https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository
2. Navigate AutomatedCableTester/

The following files contain the logic for the entire system.
- PayloadTester.py - Application/Backend 
- gui.py - UI/Frontend

