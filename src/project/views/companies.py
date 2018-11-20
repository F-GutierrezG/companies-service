from flask import Blueprint
from project.logics import CompanyLogics
from project.views.utils import success_response


companies_blueprint = Blueprint('companies', __name__)


@companies_blueprint.route('/companies', methods=['GET'])
def list():
    companies = CompanyLogics().list()
    return success_response(
        data=companies,
        status_code=200)
