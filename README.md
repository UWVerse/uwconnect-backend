# uwconnect-backend



### Installing packages

```shell
pip install -r requirements.txt
```

### Run the backend server

1. Get the `config.ini` file which contain MongoDB URI and put it in the directory `.`
2. In `.`, run `python3 server.py`
3. check http://127.0.0.1:5000/dummy to read dummy message
4. check http://127.0.0.1:5000/dummy/ping_db to read the status of MongoDB server
