from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_cors import cross_origin
from search_entities import search_entities
from db_backend.token_validation import token_required
from service.user import ( register_user_logic, login_user_logic,
                          update_user_profile_logic, get_users_logic )
from service.movies import ( get_movies_logic, get_movie_details_logic,
                             get_user_fav_movies_logic, add_movie_to_favorites_logic,
                             remove_movie_from_favorites_logic, is_movie_favorited_logic,
                             get_movies_with_directors_logic, add_movie_logic,
                             update_movie_logic, update_additional_movie_data_logic,
                             get_movie_test_logic )
from service.subscriptions import ( get_subscription_plans_logic, subscribe_to_plan_logic,
                                    check_user_free_logic, get_user_subscription_plan_logic)
from service.entities import ( get_actor_with_movies_logic, get_director_with_movies_logic, get_genre_with_movies_logic )


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Endpoint testowy /health
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route('/register', methods=['POST'])
@cross_origin()
def register_user():
    data = request.get_json()

    result, status_code = register_user_logic(data)
    return jsonify(result), status_code


@app.route('/login', methods=['POST'])
@cross_origin()
def login_user():
    data = request.get_json()
    login = data.get("login")
    password = data.get("password")

    result, status_code = login_user_logic(login, password)
    return jsonify(result), status_code


@app.route("/update/user/<uuid:user_id>", methods=["POST"])
@token_required
def update_user_profile(user_id):
    data = request.get_json()
    status_code = update_user_profile_logic(user_id, data)
    return "", status_code


@app.route("/users", methods=["GET"])
@token_required
def get_users():
    users = get_users_logic()
    return jsonify(users), 200


@app.route("/movies", methods=["GET"])
# @token_required  # Uncomment if needed
def get_movies():
    movies = get_movies_logic()
    return jsonify(movies), 200


@app.route("/movie_details/<uuid:movie_id>", methods=["GET"])
def get_movie_details(movie_id):
    movie, status_code = get_movie_details_logic(movie_id)
    return jsonify(movie), status_code

@app.route("/subscriptions/plans", methods=["GET"])
def get_subscriptions_plans():
    plans = get_subscription_plans_logic()
    return jsonify(plans), 200


@app.route("/subscriptions/subscribe", methods=["POST"])
@cross_origin()
def subscribe_to_plan():
    data = request.get_json()
    user_id = data.get("user_id")
    plan_id = data.get("plan_id")
    response, status_code = subscribe_to_plan_logic(user_id, plan_id)
    return jsonify(response) if response else '', status_code


@app.route("/subscriptions/is_free/<uuid:user_id>", methods=["GET"])
def check_user_free(user_id):
    response, status_code = check_user_free_logic(user_id)
    return jsonify(response) if isinstance(response, bool) else jsonify(response), status_code


@app.route("/subscriptions/plan/<uuid:user_id>", methods=["GET"])
def get_user_subscription_plan(user_id):
    response, status_code = get_user_subscription_plan_logic(user_id)
    return jsonify(response), status_code

@app.route("/movies/fav/<uuid:user_id>", methods=["GET"])
@token_required
def get_user_fav_movies(user_id):
    movies = get_user_fav_movies_logic(user_id)
    return jsonify(movies), 200


@app.route("/movies/fav/add", methods=["POST"])
@token_required
def add_movie_to_favorites():
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")
    response, status_code = add_movie_to_favorites_logic(user_id, movie_id)
    return jsonify(response), status_code


@app.route("/movies/fav/remove", methods=["POST"])
@token_required
def remove_movie_from_favorites():
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")
    response, status_code = remove_movie_from_favorites_logic(user_id, movie_id)
    return jsonify(response), status_code


@app.route("/movies/fav/check", methods=["POST"])
def is_movie_favorited():
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")
    response, status_code = is_movie_favorited_logic(user_id, movie_id)
    return jsonify(response), status_code


# Endpoint /movies-with-directors
@app.route("/api/views/movies_with_directors", methods=["GET"])
def movies_with_directors():
    movies = get_movies_with_directors_logic()
    return jsonify(movies), 200

@app.route("/add/movies", methods=["POST"])
def add_movie():
    data = request.get_json()
    response, status_code = add_movie_logic(data)
    return jsonify(response), status_code


@app.route("/update/movies/<uuid:movie_id>", methods=["POST"])
def update_movie(movie_id):
    data = request.get_json()
    response, status_code = update_movie_logic(movie_id, data)
    return jsonify(response), status_code


@app.route("/update/additional_movie_data/<uuid:movie_id>", methods=["POST"])
def update_additional_movie_data(movie_id):
    data = request.get_json()
    response, status_code = update_additional_movie_data_logic(movie_id, data)
    return jsonify(response), status_code


@app.route("/movie_test/<uuid:movie_id>", methods=["GET"])
def movie_test(movie_id):
    response, status_code = get_movie_test_logic(movie_id)
    return jsonify(response), status_code

@app.route("/entity/actor/<string:name>", methods=["GET"])
def get_actor_with_movies(name):
    response, status_code = get_actor_with_movies_logic(name)
    return jsonify(response), status_code


@app.route("/entity/director/<string:name>", methods=["GET"])
def get_director_with_movies(name):
    response, status_code = get_director_with_movies_logic(name)
    return jsonify(response), status_code


@app.route("/entity/genre/<string:name>", methods=["GET"])
def get_genre_with_movies(name):
    response, status_code = get_genre_with_movies_logic(name)
    return jsonify(response), status_code


@app.route("/search/actors", methods=["GET"])
def get_search_actors():
    return search_entities("ACTORS")

@app.route("/search/directors", methods=["GET"])
def get_search_directors():
    return search_entities("DIRECTORS")

@app.route("/search/users", methods=["GET"])
@token_required
def get_search_users():
    return search_entities("USERS")

@app.route("/search/movies", methods=["GET"])
def get_search_movies():
    return search_entities("MOVIES")


if __name__ == "__main__":
    app.run(debug=True)
