from elasticsearch import Elasticsearch
from flask import Flask,jsonify,url_for,redirect,render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)



# create connection with elasticsearch version 8.11.0

client = Elasticsearch(
    "http://localhost:9200",  # Elasticsearch endpoint
    )

def get_movies():
    query = {
        "query": {
             "match_all": {
            }
        }
    }
    result = client.search(index='movies_index', body=query,size=30)
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
    # return jsonify(movie_details["_source"])
    return render_template("details.html",movie_details=details)
  except Exception as e:
    return jsonify({"error": f"Movie with ID {movie_id} {e} not found"}), 404



@app.route('/', methods=['GET'])
def index():
    movies = get_movies()
    top_movies = get_top_movies()
    return render_template("index.html",movies=movies,top_movies=top_movies)
    

if __name__ == '__main__':
    app.run(debug=True)