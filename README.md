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
1 To get all the addresses
```
http://localhost:8000/addresses
```
2 To get addresses by id
```
http://localhost:8000/addresses/{id}
```
3 To get addresses by email_id
```
http://localhost:8000/addresses/email/{emailid}
```
4 To get the addresses by distance and lat long.
```
http://localhost:8000/addresses/{distance}/{lat}/{long}
```
5 To create an addresses
```
http://localhost:8000/addresses
```
6 To delete an addresses
```
http://localhost:8000/addresses/{id}
```
7 To update an addresses
```
http://localhost:8000/addresses/{id}
```