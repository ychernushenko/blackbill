// New

Install
git clone ...
sudo pip install -U docker-compose // Might take some time

Run
docker-compose build
docker-compose start mysql
docker-compose up

Stop
Ctrl+C

Use
Open localhost:5000 in browser
Note: if you use mac your need to run "docker-machine ls" to get the ip of container and then access it via ip_address:5000 in browser

Connect to database:
mysql -h 127.0.0.1 -P 3306 -u root -p


// Troubleshooting
If you get next error while running "docker-compose up": "[ERROR] Plugin 'InnoDB' registration as a STORAGE ENGINE failed." You don't have enough memory on the machine, try to free it ferxt (closing unused applications)
docker stop $(docker ps -a -q)
docker-machine rm default
docker-machine create --driver virtualbox default 


// TODO 
change mysql passwords
testing