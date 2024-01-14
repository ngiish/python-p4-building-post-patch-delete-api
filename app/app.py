#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():

    games = []
    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    
    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    
    if request.method == 'GET':
         reviews = []
         for review in Review.query.all():
             review_dict = review.to_dict()
             reviews.append(review_dict)

         response = make_response(
              jsonify(reviews),
              200
         )

         return response

    elif request.method == 'POST':
        new_review = Review(
            score=request.form.get("score"),
            comment=request.form.get("comment"),
            game_id=request.form.get("game_id"),
            user_id=request.form.get("user_id"),
        )

        db.session.add(new_review)
        db.session.commit()

        review_dict = new_review.to_dict()
        
        response = make_response(
            jsonify(review_dict),
            201
        )

        return response    
#     Handle requests with the POST HTTP verb to /reviews
# Access the data in the body of the request
# Use that data to create a new review in the database
# Send a response with newly created review as JSON
   
@app.route('/reviews/<int:id>', method=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):
    review = Review.query.filter_by(id=id).first()

    if review == None:
           response_body = {
                "message": "This record does not exist in our database. Please try again."
           }
           response = make_response(jsonify(response_body), 404)

           return response
    
    else:
        if request.method == 'GET':
            review_dict = review.to_dict()

            response = make_response(
               jsonify(review_dict),
               200
            )
            return response
    
        elif request.method == 'PATCH':
            review = Review.query.filter_by(id=id).first()

            for attr in request.form:
                setattr(review, attr, request.form.get(attr))

            db.session.add(review)
            db.session.commit()

            review_dict = review.to_dict()

            response = make_response(
                jsonify(review_dict),
                200
            )
            return response
        
# First, we locate the record we want to change.
# Second, we update the record's attributes using request.form.
        #  We use setattr() here because it allows us to use variable values as attribute names
        # - when we don't know which fields are being updated, this is important.
# From that point, this is very similar to our POST block from '/reviews'.
        #  We need to save the updated record to the database and then serve it to the client as JSON.
    
        elif request.method == 'DELETE':
            db.session.delete(review)
            db.session.commit()

            response_body = {
              "delete_successful": True,
              "message": "Review delete."
            }

            response = make_response(
               jsonify(response_body),
               200
            )
            return response

@app.route('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
