from project.models import Company
from project.serializers import CompanySerializer


class CompanyLogics:
    def list(self):
        companies = Company.query.all()

        return CompanySerializer.to_array(companies)
