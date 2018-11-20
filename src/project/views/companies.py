from flask import Blueprint
from project.auth import authenticate
from project.logics import CompanyLogics
from project.views.utils import success_response


companies_blueprint = Blueprint('companies', __name__)


@companies_blueprint.route('/companies', methods=['GET'])
@authenticate
def list(user):
    companies = CompanyLogics().list()
    return success_response(
        data=companies,
        status_code=200)
