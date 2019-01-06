from flask import Blueprint
from project.views.utils import success_response

from project.logics import ClassificationLogics


classifications_blueprint = Blueprint('classifications', __name__)

@classifications_blueprint.route('/companies/classifications', methods=['GET'])
def list():
    classifications = ClassificationLogics().list()

    return success_response(
        data=classifications,
        status_code=200)
