[![Language](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg?style=for-the-badge)]()
[![Available](https://img.shields.io/badge/Available-%20Debian-red.svg?style=for-the-badge)]()
[![Available](https://img.shields.io/badge/Available-%20Windows-red.svg?style=for-the-badge)]()
[![Download](https://img.shields.io/badge/Size-21MO-brightgreen.svg?style=for-the-badge)]()
<br>
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# 

### Author : Grégoire Bézier

## Table of contents
* [General info](#general-info)
* [Dependencies](#dependencies)
* [Setup](#setup)
* [IMPORTANT](#important)

## General info
Ceci est un script avec la librairie sélénium pour communiquer avec chatGPT sans utiliser l'API payante via le terminal, je vous laisse imaginer les possibilités de ce que vous pouvez faire avec...

## Setup
--------------------------------------------------------
#### Only the first time
- Open a new Terminal and write this:
```
~$ git clone https://github.com/gregoirebezier/chatgpt_selenium.git
~$ cd chatgpt_selenium
```
--------------------------------------------------------
- Create `.env` file and add this line:
```
PASSWORD=<Password>
EMAIL=<Email>
```
--------------------------------------------------------
- Then in your terminal, execute this commands:
```
~$ sudo pip3 install -r requirements.txt
```
```
~$ python3 chatgpt_automatisation.py
```


  ## Dependencies
* Python (3.10+)
* Selenium (4.12.0)
* python-decouple (3.8)
* undetected-chromedriver (3.5.3)

## IMPORTANT
- `The script supports only Chrome version 116 (You have to change the version in the code if you want another one) ! `
- `You have to have a ChatGPT account ! A Connexion with Oauth2 won't work (ex: Google, Microsoft etc..)`
