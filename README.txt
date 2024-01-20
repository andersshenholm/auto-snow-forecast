Welcome to Auto Snow Forecast! This is a rough proof of concept for a snow-forecasting command shell that uses takes surface-level data from snow-forecast.com. 
Currently a user can get a 1-7 day snow forecast for any US mountain on snow-forecast.com with the command 'f [mountain] [days]' or get forecasts for a list of pre-selected moutains with the command 'h.'
There is a ton of room for improvement. Some ideas are listed in TODO.txt.

Startup info for mac/linux:

Clone the github repository, install python venv, pip, Google Chrome and maybe download an updated release of the Selenium chromedriver. 
Install a python virtual environment:
    python3 -m venv [path to virtual environment]
To start virtual environment and install required packages:
    source [path to virtual environment]/bin/activate
    pip install -r requirements.txt
    mv chromedriver env/bin
To run the shell:
    python3 main.py
To exit the shell:
    ctrl-C
To exit the virtual environment:
    deactivate
