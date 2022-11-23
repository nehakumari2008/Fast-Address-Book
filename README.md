## Fast Address Book

### How to run
Create python virtual environment 
```
python3 -m virtualenv venv
```
Install requirements file 
```
pip install -r requirements.txt
```

Run
```
uvicorn main:app --reload
```

### APIs
To get all the addresses
```
GET http://localhost:8000/addresses
```
To get addresses by id
```
GET http://localhost:8000/addresses/{id}
```
To get addresses by email_id
```
GET http://localhost:8000/addresses/email/{emailid}
```
To get the addresses by distance and lat long.
```
GET http://localhost:8000/addresses/{distance}/{lat}/{long}
```
To create an addresses
```
POST http://localhost:8000/addresses
```
To delete an addresses
```
DELETE http://localhost:8000/addresses/{id}
```
To update an addresses
```
PATCH http://localhost:8000/addresses/{id}
```
