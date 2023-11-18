from elasticsearch import Elasticsearch
from flask import Flask,jsonify,url_for,redirect,render_template,request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from math import ceil


app = Flask(__name__)



# create connection with elasticsearch version 8.11.0

client = Elasticsearch(
    "http://localhost:9200",  # Elasticsearch endpoint
    )

def get_all_movies():
    query = {
        "query": {
             "match_all": {}
        }
    }
    result = client.search(index='movies_index', body=query)
    total_movies = result['hits']['total']['value']
    return total_movies



def get_movies(page=1, size=10):
    if page <= 0:
        page = 1
    query = {
        "query": {
            "match_all": {}
        },
        "from": (page - 1) * size,
        "size": size
    }
    result = client.search(index='movies_index', body=query)
    return result['hits']['hits']

def get_top_movies():
  query = {
    "query": {
        "match_all": {}
    },
    "sort": [
        {
            "vote_count": {
                "order": "desc"
            }
        }
    ]
  }
  result = client.search(index='movies_index', body=query,size=5)
  return result['hits']['hits']



@app.route('/api/movies/<string:movie_id>', methods=['GET'])
def get_movie(movie_id):
  try:
    movie_details = client.get(index="movies_index", id=movie_id)
    details = movie_details['_source']
    return render_template("details.html",movie_details=details)
  except Exception as e:
    return jsonify({"error": f"Movie with ID {movie_id} {e} not found"}), 404



@app.route('/', methods=['GET'])
def index():
    page = int(request.args.get('page', 1))
    if(page <= 0):
       page = 1
    size = int(request.args.get('size', 10))
    movies = get_movies(page,size)
    top_movies = get_top_movies()
    total_movies = get_all_movies()
    total_pages = ceil(total_movies / size)
    return render_template("index.html",movies=movies,top_movies=top_movies, page=page, size=size, total_pages=total_pages)    

if __name__ == '__main__':
    app.run(debug=True)