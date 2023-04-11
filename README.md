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

# To safely contribute to the dev branch

Please note that in `uwconnect-backend` we use the `dev` branch for our development.
Since each pull request is tracked to a branch, we should create new branch for every task.

```shell
./create_branch_from_dev.sh <your_fancy_branch_name>
```
The script will automatically fetch the current remote dev branch to your local, and push it to your local new branch.