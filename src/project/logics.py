from sqlalchemy.sql.expression import true

from project.models import Company, UserCompanies
from users_service.factories import UsersServiceFactory
from project.serializers import CompanySerializer
from project import db


class NotFound(Exception):
    pass


class Forbidden(Exception):
    pass


class CompanyLogics:
    def __belongs_to_company(self, user, id):
        user_company = UserCompanies.query.filter_by(
            user_id=user.id,
            company_id=id).first()
        return user_company is not None

    def get(self, user, id):
        company = None
        if user.admin or self.__belongs_to_company(user, id):
            company = Company.query.filter_by(id=id).first()

        if company is None:
            raise NotFound

        return CompanySerializer.to_dict(company)

    def list_by_user(self, user):
        companies = Company.query.join(Company.users, aliased=True)\
                    .filter(
                        UserCompanies.user_id == user.id,
                        Company.active == true())

        return CompanySerializer.to_array(companies)

    def create(self, user, data):
        if not user.admin:
            raise Forbidden

        data['created_by'] = user.id
        company = Company(**data)

        db.session.add(company)
        db.session.commit()

        return CompanySerializer.to_dict(company)


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
            raise NotFound

        for user in company.users:
            users_ids.append(user.user_id)

        return UsersServiceFactory.get_instance().filter_by_ids(users_ids)
