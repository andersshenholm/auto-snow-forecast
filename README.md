# Auto Snow Forecast
Welcome to Auto Snow Forecast! This is a rough proof of concept for a snow-forecasting command shell that uses takes surface-level data from snow-forecast.com. Currently a user can get a 1-7 day snow forecast for any US mountain on snow-forecast.com or get forecasts for a list of pre-selected moutains. There is a ton of room for improvement. Some ideas are listed in TODO.txt.

## Startup Info For Mac/Linux
First, clone the github repository, install python venv, pip, Google Chrome and maybe download an updated release of the Selenium chromedriver.
#### Install a python virtual environment:
    python3 -m venv [path to virtual environment]
#### Start the virtual environment and install required packages:
    source [path to virtual environment]/bin/activate
    pip install -r requirements.txt
    mv chromedriver env/bin
#### Run the shell:
    python3 main.py
#### Run commands:
    f, forecast [mountain] [days]
    h, home
#### Exit the shell:
    ctrl-C
#### Exit the virtual environment:
    deactivate
