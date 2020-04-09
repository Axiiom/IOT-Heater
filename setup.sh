#!/bin/bash

# enable i2c and spi
# follow: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

echo "This should output: /dev/i2c-1 /dev/spidev0.0 /dev/spidev0.1"
ls /dev/i2c* /dev/spi*

echo "Installing dependencies"
sudo apt-get install libgpiod2

echo "Installing Python dependencies"
sudo apt-get install python3 python3-dev python3-venv
pip3 install RPI.GPIO
pip3 install adafruit-blinka


echo "Creating virtual environment"
python3.8 -m venv venv

echo "Install python requirements"
source venv/bin/activate
pip3 install -r requirements.txt
