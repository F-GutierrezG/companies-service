from sqlalchemy.sql.expression import true

from project.models import Company, UserCompanies
from project.services import UsersServiceFactory
from project.serializers import CompanySerializer


class DoesNotExist(Exception):
    pass


class CompanyLogics:
    def list_by_user(self, user):
        companies = Company.query.join(Company.users, aliased=True)\
                    .filter(
                        UserCompanies.user_id == user.id,
                        Company.active == true())

        return CompanySerializer.to_array(companies)


class UserLogics:
    def list_by_company(self, id):
        users_ids = []
        company = Company.query.get(id)

        if company is None:
            raise DoesNotExist

        for user in company.users:
            users_ids.append(user.user_id)

        return UsersServiceFactory.get_instance().filter_by_id(users_ids)
