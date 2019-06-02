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
            'plan': {
                'id': company.plan.id,
                'name': company.plan.name
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


class PlanSerializer:
    @staticmethod
    def to_dict(plan):
        return {
            'id': plan.id,
            'name': plan.name
        }

    @staticmethod
    def to_array(plans):
        return list(
            map(
                lambda plan: PlanSerializer.to_dict(
                    plan), plans))


class BrandSerializer:
    @staticmethod
    def to_dict(brand):
        return {
            'id': brand.id,
            'name': brand.name,
            'active': brand.active,
            'created': brand.created,
            'created_by': brand.created_by,
            'updated': brand.updated,
            'updated_by': brand.updated_by,
        }

    @staticmethod
    def to_array(brands):
        return list(
            map(
                lambda brand: BrandSerializer.to_dict(
                    brand), brands))
