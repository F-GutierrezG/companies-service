from flask import Blueprint, jsonify, request

from auth.decorators import authenticate
from validators.exceptions import ValidatorException
from project.views.utils import success_response, failed_response

from project.logics import (BrandLogics, NotFound, Forbidden)


brands_blueprint = Blueprint('brands', __name__)


@brands_blueprint.route('/companies/<id>/brands', methods=['GET'])
@authenticate
def brands(user, id):
    brands = BrandLogics().list(id)

    return jsonify(brands), 200


@brands_blueprint.route('/companies/<id>/brands', methods=['POST'])
@authenticate
def create(user, id):
    data = request.get_json()

    try:
        brand = BrandLogics().create(user, id, data)
        return success_response(
            data=brand,
            status_code=201)
    except Forbidden:
        return failed_response('forbidden.', 403)
    except ValidatorException as e:
        return failed_response('invalid payload.', 400, e.errors)


@brands_blueprint.route(
    '/companies/brands/<id>/deactivate',
    methods=['PUT'])
@authenticate
def deactivate(user, id):
    try:
        brand = BrandLogics().deactivate(user, id)
        return success_response(data=brand, status_code=200)

    except NotFound:
        return failed_response(message='not found.', status_code=404)


@brands_blueprint.route(
    '/companies/brands/<id>/activate',
    methods=['PUT'])
@authenticate
def activate(user, id):
    try:
        brand = BrandLogics().activate(user, id)
        return success_response(data=brand, status_code=200)

    except NotFound:
        return failed_response(message='not found.', status_code=404)


@brands_blueprint.route('/companies/brands/<id>', methods=['PUT'])
@authenticate
def update(user, id):
    data = request.get_json()

    try:
        brand = BrandLogics().update(user, id, data)
        return success_response(
            data=brand,
            status_code=200)
    except NotFound:
        return failed_response('not found.', 404)
    except Forbidden:
        return failed_response('forbidden.', 403)
    except ValidatorException as e:
        return failed_response('invalid payload.', 400, e.errors)
