from bottle import Bottle, route, run, request, abort, response, get, post, delete, put
from pymongo import MongoClient
import json


uri = "mongodb://127.0.0.1"
dbname = "movies"

try:
    connection = MongoClient(uri, 27017)
    db = connection[dbname]
except Exception:
    print "Couldn't connect to database"

app = Bottle()

#a set to keep a list of movie names
_names = set()

#dummy data
movies = [{'title' : 'Blade Runner', 'rel_date' : '25 June 1982', 'prod_company' : 'Warner Bros.'},
          {'title': 'Snatch', 'rel_date': '19 January 2001', 'prod_company': 'Columbia Pictures'},
          {'title': 'The Godfather', 'rel_date': '24 March 1972', 'prod_company': 'Paramount Pictures'},
          {"title": "Fight Club", "rel_date": "21 September 1999", "prod_company": "20th Century Fox" }]

#Populate database if it doesnt exist
if dbname not in connection.database_names():
    db[dbname].insert(movies)

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


#looks for the specified movie in the movie list.
#if found return the movie.
@get('/movies/<name>')
def get_one_movie(name):

    data = db[dbname].find_one({'title' : name}, {'_id': False})

    #if such name doesnt exist in db return a 404
    if not data:
        abort(404, "Sorry, we don't have information about the movie called '{}'.".format(name))
    return json.dumps(data)

#pulls the data from the request in a form of jason and creates a dictionary for the new movie.
#adds new movie to the list of movies
#known bugs: adds duplicates
@post('/movies')
def add_movie():

    #extract data
    try:
        new_movie = {'title' : request.json.get('title'), 'rel_date' : request.json.get('rel_date'), 'prod_company' : request.json.get('prod_company')}
    except request.exceptions.RequesExceptions as e:
        return ("Error getting the input : {}".format(e))

    #validate data is not empty
    if new_movie is None:
        abort(400, "No value was passed")

    #pull title from the new data
    try:
        name = new_movie['title']
    except (TypeError, KeyError):
        raise  ValueError

    #check for existence to avoid dups.
    if db[dbname].find({'title' : name}):
        abort(409, "Duplicate title")

    #add new movie to the db
    db[dbname].save(new_movie)

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return {'Message' : 'Movie added'}

#delets a movie from he list
@delete('/movies/<name>')
def remove_movie(name):
    data = db[dbname].find_one({'title': name})
    if not data:
        abort(404, "Sorry, we don't have information about the movie called '{}'.".format(name))

    db[dbname].remove(data)
    return {'Message' : '{} was deleted'.format(name)}

@put('/movies/<name>')
def update_movies_list(name):

    # extract data
    try:
        new_data = {'title': request.json.get('title'), 'rel_date': request.json.get('rel_date'),
                     'prod_company': request.json.get('prod_company')}
    except request.exceptions.RequesExceptions as e:
        return ("Error getting the input : {}".format(e))

    # validate data is not empty
    if new_data is None:
        abort(400, "No value was passed")

    db[dbname].delete_one({'title' : name})
    db[dbname].insert_one(new_data)

    response.headers['Content-Type'] = 'application/json'
    return ({'Message' : 'Movie updated'})



#implement patch
#known bugs: possible to creat a new field in the collection if data did not exist prior to patch request
@route('/movies/<name>', method='PATCH')
def update_movie(name):

    data = request.json
    if not data:
        abort(400, 'No data received')

    try:
        db[dbname].update_one({'title' : name}, {'$set': data})
    except Exception as e:
        print (e)

    response.headers['Content-Type'] = 'application/json'
    return {'Message' : 'The movie was updated'}



if __name__ == '__main__':
    run(host='localhost', port='8080', debug=True, reloader=True)
