from flask import Blueprint

from auth.decorators import authenticate
from project.views.utils import success_response

from project.logics import PlanLogics


plans_blueprint = Blueprint('plans', __name__)


@plans_blueprint.route('/companies/plans', methods=['GET'])
@authenticate
def list(user):
    plans = PlanLogics().list()

    return success_response(
        data=plans,
        status_code=200)
