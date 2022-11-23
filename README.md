## Fast Address Book

### How to run
1 Create python virtual environment 
```
python3 -m virtualenv venv
```
2 Install requirements file 
```
pip install -r requirements.txt
```

2 Run
```
- uvicorn main:app --reload
```

### APIs
To get all the addresses
```
http://localhost:8000/addresses
```
To get addresses by id
```
http://localhost:8000/addresses/{id}
```
To get addresses by email_id
```
http://localhost:8000/addresses/email/{emailid}
```
To get the addresses by distance and lat long.
```
http://localhost:8000/addresses/{distance}/{lat}/{long}
```
To create an addresses
```
http://localhost:8000/addresses
```
To delete an addresses
```
http://localhost:8000/addresses/{id}
```
To update an addresses
```
http://localhost:8000/addresses/{id}
```
