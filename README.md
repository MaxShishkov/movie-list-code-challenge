# rest api
Build Simple REST API on Bottle and MongoDB!

## Dependency:

* Python
Python v2.7

* Bottle
```
pip install bottle==0.12
```

* pymongo
```
pip install pymongo==3.5.1
```

* Alternativly
```
pip install -r requirements.txt

```

* MongoDB : 
You will need to install MongoDB v3.4.10 
Instructions can be found here : https://docs.mongodb.com/manual/installation/

## Example: Basic Rest API

```python
@get('/')
def index():
    return ({'Message' : 'This is my api. Thanks for visiting'})

@get('/movies')
def get_movies():
    data = db[dbname].find({},{'_id': False})
    if not data:
        abort(404, "Sorry, We don't have any information")
    result =[item for item in data]

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps({'Movies' : result})
```


## Usage:
1. Start MongoDB:
```
mongod
```

2. Run the api:

```
python api.py
```

3. Ways to test:
You can test the api with Postman.
https://www.getpostman.com/docs/postman/launching_postman/installation_and_updates

or use curl command

Examples of curl
a.
```
$ curl GET localhost:8080/ 
returns JSON object {'Message' : 'This is my api. Thanks for visiting'}
```

b. Get a list of movies

```
$ curl GET localhost:8080/movies

```

Returns JSON object with a list of movies

c. Get a movie by name

```
$ curl GET localhost:8080/movies/<name> 

```
returns a movie if it exists in the database


## Built With

* [Bottle](http://bottlepy.org/docs/dev/) - The web framework used
* [MongoDB](https://www.mongodb.com/) - Database

## Authors

* **Max Shishkov** - *Initial work*
