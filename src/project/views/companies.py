from flask import Blueprint
from auth.decorators import authenticate
from project.logics import CompanyLogics, UserLogics, DoesNotExist
from project.views.utils import success_response, failed_response


companies_blueprint = Blueprint('companies', __name__)


@companies_blueprint.route('/companies', methods=['GET'])
@authenticate
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
    except DoesNotExist:
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
    except DoesNotExist:
        return failed_response(message='not found.', status_code=404)
