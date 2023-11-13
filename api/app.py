from elasticsearch import Elasticsearch
from flask import Flask,jsonify,url_for,redirect,render_template


app = Flask(__name__)



# create connection with elasticsearch version 8.11.0

client = Elasticsearch(
    "http://localhost:9200",  # Elasticsearch endpoint
    )



# Define the Elasticsearch query
es_query = {
    "_source": ["title", "status", "overview", "name_production_company", "original_language", "tagline", "video", "vote_average", "vote_count"],
    "query": {"match_all": {}}
}

# Perform the Elasticsearch search
result = client.search(index="movies", body=es_query)

# Extract only the _source field from the Elasticsearch result
movies_source = [hit["_source"] for hit in result["hits"]["hits"]]


# result = client.search(index="movies", query={
#     "match_all": {}
# })


# get all movies [ALL]

@app.route('/api/movies', methods=['GET'])
def all_movies():
    return jsonify(movies_source)

# get movies by [ID]

@app.route('/api/movie/<string:movie_id>', methods=['GET'])
def movie_by_id(movie_id):
    try:
        movie = client.get(index="movies", id=movie_id)
        return jsonify(movie["_source"])
    except Exception as e:
        return jsonify({"error": f"Movie with ID {movie_id} not found"}), 404




@app.route('/', methods=["GET"])
def index():
    return render_template("index.html", content=movies_source)










# redirect the users to the api

# @app.route('/', methods=['GET'])
# def redirect_home():
#     return redirect(url_for("index"))



if __name__ == '__main__':
    app.run(debug=True)