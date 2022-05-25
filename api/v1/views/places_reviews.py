#!/usr/bin/python3
''' Module that handles all default RESTFul API '''

from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """method that retrieves a list of all reviews"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    reviews_list = []
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_one_review(review_id):
    """method that retrieves a review by id"""
    review = storage.get('Review', review_id)
    if review is not None:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """method that deletes a review by id"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """method to create a new review"""
    review = request.get_json()
    if not review:
        abort(400, 'Not a JSON')
    if 'user_id' not in review:
        abort(400, 'Missing user_id')
    if 'text' not in review:
        abort(400, 'Missing text')
    user = storage.get('User', request.json['user_id'])
    if user is None:
        abort(404)
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    new_review = Review(user_id=request.json['user_id'],
                        text=request.json['text'], place_id=place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """method to update a review by id"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    req = request.get_json()
    req['id'] = review.id
    req['user_id'] = review.user_id
    req['place_id'] = review.place_id
    req['created_at'] = review.created_at
    review.__init__(**req)
    review.save()
    return jsonify(review.to_dict()), 200
