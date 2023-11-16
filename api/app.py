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
    result = client.search(index='movies_index', body=query,size=10)
    return result['hits']['hits']


@app.route('/api/movies/<string:title>', methods=['GET'])
def get_movie(title):
    try:
        movies = get_movies()
        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": f"Movie with ID {title} not found"}), 404


@app.route('/', methods=['GET'])
def index():
    movies = get_movies()
    return render_template("index.html",movies=movies)

maping = {
  "mappings": {
    "properties": {
      "budget": {
        "type": "long"
      },
      "genres_name": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "name_production_company": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "original_language": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "original_title": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "overview": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "popularity": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "release_date": {
        "type": "date"
      },
      "status": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "tagline": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "title": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "video": {
        "type": "boolean"
      },
      "vote_average": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "vote_count": {
        "type": "long"
      }
    }
  }
}


if __name__ == '__main__':
    app.run(debug=True)







































# app = Flask(__name__)



# # create connection with elasticsearch version 8.11.0

# client = Elasticsearch(
#     "http://localhost:9200",  # Elasticsearch endpoint
#     )



# # Define the Elasticsearch query
# es_query = {
#     "_source": ["title", "status", "overview", "name_production_company", "original_language", "tagline", "video", "vote_average", "vote_count"],
#     "query": {"match_all": {}}
# }

# # Perform the Elasticsearch search
# result = client.search(index="movies", body=es_query)

# # Extract only the _source field from the Elasticsearch result
# movies_source = [hit["_source"] for hit in result["hits"]["hits"]]


# result = client.search(index="movies", query={
#     "match_all": {}
# })


# # get all movies [ALL]

# @app.route('/api/movies', methods=['GET'])
# def all_movies():
#     return jsonify(movies_source)

# # get movies by [ID]

# @app.route('/api/movie/<string:movie_id>', methods=['GET'])
# def movie_by_id(movie_id):
#     try:
#         movie = client.get(index="movies", id=movie_id)
#         return jsonify(movie["_source"])
#     except Exception as e:
#         return jsonify({"error": f"Movie with ID {movie_id} not found"}), 404




# @app.route('/', methods=["GET"])
# def index():
#     return render_template("index.html", content=movies_source)










# # redirect the users to the api

# # @app.route('/', methods=['GET'])
# # def redirect_home():
# #     return redirect(url_for("index"))



# if __name__ == '__main__':
#     app.run(debug=True)