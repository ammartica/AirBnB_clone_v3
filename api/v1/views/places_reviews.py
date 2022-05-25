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
def all_reviews(place_id=None):
    """method retieves all reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    all_reviews = place.reviews
    reviews = []
    for review in all_reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def one_review(review_id=None):
    """method that retrieves a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """method that deletes a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id=None):
    """method to create a new review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    request = request.get_json()
    if not request:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    user = storage.get(User, request.get('user_id'))
    if not user:
        abort(404)
    review = Review(place_id=place.id, user_id=user.id,
                    text=request.get('text'))
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """method to update a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    request = request.get_json()
    if not request:
        abort(400, 'Not a JSON')
    request['id'] = review.id
    request['user_id'] = review.user_id
    request['place_id'] = review.place_id
    request['created_at'] = review.created_at
    review.__init__(**request)
    review.save()
    return jsonify(review.to_dict()), 200
