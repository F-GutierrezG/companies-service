from project.models import Company
from project.serializers import CompanySerializer


class CompanyLogics:
    def list_by_user(self, user):
        companies = Company.query.join(Company.users, aliased=True)\
                    .filter_by(user_id=user.id)

        return CompanySerializer.to_array(companies)
