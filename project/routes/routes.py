""" Routes to show apartments """
from project import db
from flask_cors import CORS
from flask import request, Blueprint, g
from project.models.models import Apartment, Rankings, User
from project.helpers.decorators import jwt_required

apartment_ranker_api = Blueprint("apartment_ranker_api", __name__)

CORS(apartment_ranker_api)


@apartment_ranker_api.route('/api/apartments', methods=["POST"])
@jwt_required
def create_apartment():
    """ POST a new apartment and return JSON object of specific apartment """

    new_apt_url = request.json['url']

    output = Apartment.add_apartment(url=new_apt_url,
                                     user_random_id=g.user.user_random_id)

    return output.serialize()


@apartment_ranker_api.route('/api/apartments/<int:ranking_id>',
                            methods=["PATCH"])
@jwt_required
def update_rankings(ranking_id):
    """ PATCH an existing apartment's rankings """

    rankings = Rankings.query.get_or_404(ranking_id)

    updates = request.json['formData']

    for key in updates:
        setattr(rankings, key, updates[key])

    db.session.commit()

    apt = Apartment.query.get_or_404(rankings.r_apartment_url)

    output = apt.serialize()

    return output


@apartment_ranker_api.route('/api/apartments', methods=["GET"])
@jwt_required
def get_every_apartment():
    """ GET every apartment for the current user """

    output = Apartment.get_all_apartments(user_random_id=g.user.user_random_id)

    return output


@apartment_ranker_api.route('/api/users/signup', methods=["POST"])
def generate_user():
    """ POST a new user """

    user = User.create_user()

    if isinstance(user, User):
        return user.serialize()

    return (user, 400)


@apartment_ranker_api.route('/api/users/confirm', methods=["GET"])
@jwt_required
def confirm_user():
    """ GET an existing user via JWT, if existing provide confirmation """

    if g.user:
        return {"status": "confirmed"}
    else:
        return {"status": "invalid"}

# @apartment_ranker_api.route('/api/users/check', methods=["GET"])
# def check_user():
#     """
#     GET an existing user via the request's IP address.
#     If existing, return user, else return message indicating no user exists.
#     """

#     user = User.query.get(request.headers['X-Forwarded-For'][0])

#     if isinstance(user, User):
#         return user.serialize()

#     return {"status": "no existing user."}
