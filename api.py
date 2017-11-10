from bottle import run, get, post, delete, request

#dummy data for now.
movies = [{'title' : 'Blade Runner', 'rel_date' : '25 June 1982', 'prod_company' : 'Warner Bros.'},
          {'title': 'Snatch', 'rel_date': '19 January 2001', 'prod_company': 'Columbia Pictures'},
          {'title': 'The Godfather', 'rel_date': '24 March 1972', 'prod_company': 'Paramount Pictures'}]

@get('/')
def index():
    #template for a for if i need it
    #return '''
     #   <form action="/login" method="post">
      #      Name: <input name="name" type="text" />
       #     <input value="Submit" type="submit" />
        #</form>
    #'''
    #just retursn a list of movies for now
    return{'movies' : movies}

#looks for the specified movie in the movie list.
#if found return the movie.
@get('/<name>')
def get_movie(name):
    the_movie = [movie for movie in movies if movie['name'] == name]
    return {'movie' : the_movie[0]}

#pulls the data from the request in a form of jason and creats a dictionary for the new movie.
#adds new movie to the list of movies
@post('/')
def add_movie():
    new_movie = {'title' : request.json.get('title'), 'rel_date' : request.json.get('rel_date'), 'prod_company' : request.json.get('prod_company')}
    movies.append(new_movie)
    return {'movies' : movies}

#delets a movie from he list
@delete('/<name>')
def remove_movie(name):
    the_movie = [movie for movie in movies if movie['name'] == name]
    movies.remove(the_movie[0])
    return {'movies' : movies}


#implement patch



if __name__ == '__main__':
    run(host='localhost', port='8080', debug=False,reloader=True)
