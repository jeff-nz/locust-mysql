# Locust Mysql 


### Local Lib requirement
```
sudo pacman -S python-mysqlclient
```

### PIP
```
pip install locust mysql-connector-python --break-system-packages
```

### Poetry
Go to root project directory ./ and run...
```
poetry install
```


### Run
```
poetry run locust -f src/main.py 
```