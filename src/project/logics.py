from sqlalchemy.sql.expression import true

from users_service.factories import UsersServiceFactory
from validators.decorators import validate

from project.validations import CompanyValidator, BrandValidator
from project.models import Company, UserCompanies, Classification, Plan, Brand
from project.serializers import (
    CompanySerializer, ClassificationSerializer, PlanSerializer,
    BrandSerializer)
from project import db


class NotFound(Exception):
    pass


class Forbidden(Exception):
    pass


class InternalServerError(Exception):
    pass


class BadRequest(Exception):
    def __init__(self, message):
        self.message = message


class CompanyLogics:
    def __belongs_to_company(self, user, company):
        user_company = UserCompanies.query.filter_by(
            user_id=user.id,
            company_id=company.id).first()
        return user_company is not None

    def __get(self, id):
        company = Company.query.filter_by(id=id).first()

        if company is None:
            raise NotFound

        return company

    def __check_modify_company_permission(self, user, company):
        if not user.admin and not self.__belongs_to_company(user, company):
            raise Forbidden

    def get(self, user, id):
        company = self.__get(id)

        self.__check_modify_company_permission(user, company)

        return CompanySerializer.to_dict(company)

    def list_by_user(self, user):
        if user.admin:
            companies = Company.query.order_by(Company.id.asc()).all()
        else:
            companies = Company.query.join(Company.users, aliased=True)\
                        .filter(
                            UserCompanies.user_id == user.id,
                            Company.active == true())\
                        .order_by(Company.id.asc())

        return CompanySerializer.to_array(companies)

    @validate(CompanyValidator)
    def create(self, user, data):
        if not user.admin:
            raise Forbidden

        data['created_by'] = user.id
        company = Company(**data)

        db.session.add(company)
        db.session.commit()

        return CompanySerializer.to_dict(company)

    @validate(CompanyValidator)
    def update(self, user, id, data):
        company = self.__get(id)

        self.__check_modify_company_permission(user, company)

        if 'expiration' in data and data['expiration'] is not None and \
                data['expiration'].strip() == '':
            data['expiration'] = None

        data['updated_by'] = user.id
        Company.query.filter_by(id=id, active=True).update(data)
        db.session.commit()

        return self.get(user, id)

    def deactivate(self, id, updated_by):
        Company.query.filter_by(id=id).update({
            'active': False,
            'updated_by': updated_by.id
        })
        db.session.commit()

        return self.get(updated_by, id)

    def activate(self, id, updated_by):
        Company.query.filter_by(id=id).update({
            'active': True,
            'updated_by': updated_by.id
        })
        db.session.commit()

        return self.get(updated_by, id)


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
            _, users = users_service.get_admin_users()
        else:
            users_ids = self._get_same_company_users_ids(user)
            _, users = users_service.filter_by_ids(ids=users_ids)

        return users

    def list_by_company(self, id):
        users_ids = []
        company = Company.query.get(id)

        if company is None:
            raise NotFound

        for user in company.users:
            users_ids.append(user.user_id)

        if len(users_ids) == 0:
            return []

        _, users = UsersServiceFactory.get_instance().filter_by_ids(users_ids)

        return users

    def create_user_in_company(self, user_data, id, user):
        # users service crear usuario
        user_data['admin'] = False
        response, user = UsersServiceFactory.get_instance().create_user(
            user_data)

        if response.status_code == 201:
            user_company = UserCompanies(user_id=user['id'], company_id=id)

            db.session.add(user_company)
            db.session.commit()

            return user

        if response.status_code == 400:
            raise BadRequest(message=user['message'])

        else:
            raise InternalServerError()


class ClassificationLogics:
    def list(self):
        classifications = Classification.query.all()

        return ClassificationSerializer.to_array(classifications)


class PlanLogics:
    def list(self):
        plans = Plan.query.all()

        return PlanSerializer.to_array(plans)


class BrandLogics:
    def get(self, id):
        brand = Brand.query.filter_by(id=id).first()

        return BrandSerializer.to_dict(brand)

    def list(self, id):
        brands = Brand.query.filter_by(company_id=id)

        return BrandSerializer.to_array(brands)

    @validate(BrandValidator)
    def create(self, user, id, data):
        data['created_by'] = user.id
        data['company_id'] = id
        brand = Brand(**data)

        db.session.add(brand)
        db.session.commit()

        return BrandSerializer.to_dict(brand)

    def deactivate(self, updated_by, id):
        Brand.query.filter_by(id=id).update({
            'active': False,
            'updated_by': updated_by.id
        })
        db.session.commit()

        return self.get(id)

    def activate(self, updated_by, id):
        Brand.query.filter_by(id=id).update({
            'active': True,
            'updated_by': updated_by.id
        })
        db.session.commit()

        return self.get(id)

    @validate(BrandValidator)
    def update(self, user, id, data):
        data['updated_by'] = user.id
        Brand.query.filter_by(id=id, active=True).update(data)
        db.session.commit()

        return self.get(id)
