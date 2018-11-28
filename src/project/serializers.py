class CompanySerializer:
    @staticmethod
    def to_dict(company):
        return {
            'id': company.id,
            'identifier': company.identifier,
            'name': company.name,
        }

    @staticmethod
    def to_array(companies):
        companies_list = []

        for company in companies:
            companies_list.append(CompanySerializer.to_dict(company))

        return companies_list
