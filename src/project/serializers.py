class CompanySerializer:
    @staticmethod
    def to_dict(company):
        return {
            'id': company.id,
            'identifier': company.identifier,
            'name': company.name,
            'classification': {
                'id': company.classification.id,
                'name': company.classification.name
            },
            'expiration':
                str(company.expiration) if company.expiration else None,
            'active': company.status,
            'created': company.created,
            'created_by': company.created_by,
            'updated': company.updated,
            'updated_by': company.updated_by,
        }

    @staticmethod
    def to_array(companies):
        return list(
            map(
                lambda company: CompanySerializer.to_dict(
                    company), companies))


class ClassificationSerializer:
    @staticmethod
    def to_dict(classification):
        return {
            'id': classification.id,
            'name': classification.name
        }

    @staticmethod
    def to_array(classifications):
        return list(
            map(
                lambda classification: ClassificationSerializer.to_dict(
                    classification), classifications))
