# Locust Mysql 
A simple demo for sending random test data to a mysqlDB using Locust. 

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
STEP 1 - start mysql
```
./bin/mysql-reset 
```

STEP 2 - setup mysql table
```
./bin/mysql-reset 
```

STEP 3 - run locust to start populating random test data
```
poetry run locust -f src/main.py 
```


Cleanup docker and data from your local
```
./bin/mysql-remove 
```
