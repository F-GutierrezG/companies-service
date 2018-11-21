from sqlalchemy.sql.expression import true

from project.models import Company, UserCompanies
from project.serializers import CompanySerializer


class CompanyLogics:
    def list_by_user(self, user):
        companies = Company.query.join(Company.users, aliased=True)\
                    .filter(
                        UserCompanies.user_id == user.id,
                        Company.active == true())

        return CompanySerializer.to_array(companies)
