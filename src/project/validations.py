from validators import BaseValidator
from validators import rules
from project.models import Company


class CompanyValidator(BaseValidator):
    def get_rules(self):
        return {
            'identifier': [
                rules.Required(),
                rules.Length(max=Company.IDENTIFIER_MAX_LENGTH)
            ],
            'name': [
                rules.Required(),
                rules.Length(max=Company.NAME_MAX_LENGTH)
            ]
        }


class BrandValidator(BaseValidator):
    def get_rules(self):
        return {
            'name': [
                rules.Required(),
                rules.Length(max=Company.NAME_MAX_LENGTH)
            ]
        }
