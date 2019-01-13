from flask import Blueprint, request

from auth.decorators import authenticate, authorize
from validators.exceptions import ValidatorException

from project.logics import (
    CompanyLogics, UserLogics, NotFound, Forbidden, BadRequest,
    InternalServerError)
from project.views.utils import success_response, failed_response


companies_blueprint = Blueprint('companies', __name__)


@companies_blueprint.route('/companies', methods=['GET'])
@authorize([])
def list(user):
    companies = CompanyLogics().list_by_user(user)
    return success_response(
        data=companies,
        status_code=200)


@companies_blueprint.route('/companies/<id>', methods=['GET'])
@authenticate
def view(user, id):
    try:
        company = CompanyLogics().get(user, id)
        return success_response(
            data=company,
            status_code=200)
    except Forbidden:
        return failed_response('forbidden.', 403)
    except NotFound:
        return failed_response(message='not found.', status_code=404)


@companies_blueprint.route('/companies/users', methods=['GET'])
@authenticate
def list_users(user):
    users = UserLogics().list_users(user)
    return success_response(
        data=users,
        status_code=200)


@companies_blueprint.route('/companies/<id>/users', methods=['GET'])
@authenticate
def users(user, id):
    try:
        users = UserLogics().list_by_company(id)
        return success_response(
            data=users,
            status_code=200)
    except NotFound:
        return failed_response(message='not found.', status_code=404)


@companies_blueprint.route('/companies', methods=['POST'])
@authenticate
def create(user):
    company_data = request.get_json()

    try:
        company = CompanyLogics().create(user, company_data)
        return success_response(
            data=company,
            status_code=201)
    except Forbidden:
        return failed_response('forbidden.', 403)
    except ValidatorException as e:
        return failed_response('invalid payload.', 400, e.errors)


@companies_blueprint.route('/companies/<id>', methods=['PUT'])
@authenticate
def update(user, id):
    company_data = request.get_json()

    try:
        company = CompanyLogics().update(user, id, company_data)
        return success_response(
            data=company,
            status_code=200)
    except NotFound:
        return failed_response('not found.', 404)
    except Forbidden:
        return failed_response('forbidden.', 403)
    except ValidatorException as e:
        return failed_response('invalid payload.', 400, e.errors)


@companies_blueprint.route('/companies/<id>/deactivate', methods=['PUT'])
@authenticate
def deactivate(user, id):
    try:
        company = CompanyLogics().deactivate(id, user)
        return success_response(data=company, status_code=200)

    except NotFound:
        return failed_response(message='not found.', status_code=404)


@companies_blueprint.route('/companies/<id>/activate', methods=['PUT'])
@authenticate
def activate(user, id):
    try:
        company = CompanyLogics().activate(id, user)
        return success_response(data=company, status_code=200)

    except NotFound:
        return failed_response(message='not found.', status_code=404)


@companies_blueprint.route('/companies/<id>/users', methods=['POST'])
@authenticate
def create_user(user, id):
    user_data = request.get_json()
    try:
        user = UserLogics().create_user_in_company(user_data, id, user)

        return success_response(data=user, status_code=201)
    except BadRequest as e:
        return failed_response(message=e.message, status_code=400)
    except InternalServerError:
        return failed_response(message="", status_code=500)
