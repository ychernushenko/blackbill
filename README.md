## Scope
Main requirements (no optional things) + interface  
Task description in the file SeniorBackendApplicantTest.pdf

## Demo
https://www.dropbox.com/sh/8in8jp85g9xuipf/AACGyQkPzTv0U1uVhQ5v66Fza?dl=0

## Install
git clone https://github.com/yury-chernushenko/blackbill.git  
sudo pip install -U docker-compose // Might take some time

## Usage
### Run
docker-compose build  
docker-compose start mysql  
docker-compose up  

### Stop
Ctrl+C

### Use
Open **localhost:5000** in browser  

*Note*: if you use mac your need to run "docker-machine ls" to get the ip of container and then access it via ip_address:5000 in browser

