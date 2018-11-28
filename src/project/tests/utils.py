import random
import string

from users_service.factories import UsersServiceFactory

from project import db
from project.models import UserCompanies


def random_string(length=32):
    return ''.join(
        [random.choice(
            string.ascii_letters + string.digits
        ) for n in range(length)]
    )


def add_user(admin=False):
    users_service = UsersServiceFactory.get_instance()
    user = {
        'id': random.randint(0, 100000),
        'first_name': random_string(),
        'last_name': random_string(),
        'email': '{}@test.com'.format(random_string),
        'admin': admin
    }
    users_service.add_user(user)
    return user


def add_user_to_company(user, company):
    user_company = UserCompanies(user_id=user['id'], company_id=company.id)

    db.session.add(user_company)
    db.session.commit()

    return user_company
