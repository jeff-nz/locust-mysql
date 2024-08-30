# Locust Mysql 


### Local Lib requirement
```
sudo pacman -S python-mysqlclient
```

### PIP
```
pip install locust mysql-connector-python mysql --break-system-packages
```

### Poetry
Go to root project directory ./ and run to set poetry to the correct python env...
```
poetry env use $(pyenv which python)
```

then install all required modules
```
poetry install
```


### Run
```
poetry run locust -f src/main.py 
```