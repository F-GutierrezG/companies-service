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
    def _get_same_company_users_ids(self, user):
        user_company = UserCompanies.query.filter_by(user_id=user.id).first()

        if user_company is None:
            return []

        companies = UserCompanies.query.filter_by(
            company_id=user_company.company_id).all()

        ids = []

        for user_company in companies:
            ids.append(user_company.user_id)

        return ids

    def list_users(self, user):
        users_service = UsersServiceFactory.get_instance()

        if user.admin:
            users = users_service.get_admin_users()
        else:
            users_ids = self._get_same_company_users_ids(user)
            users = users_service.filter_by_ids(ids=users_ids)

        return users

    def list_by_company(self, id):
        users_ids = []
        company = Company.query.get(id)

        if company is None:
            raise DoesNotExist

        for user in company.users:
            users_ids.append(user.user_id)

        return UsersServiceFactory.get_instance().filter_by_ids(users_ids)
