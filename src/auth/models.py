class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.admin = False if 'admin' not in data else data['admin']
        self.hash = data['hash']
        self.permissions = data['permissions'] if 'permissions' in data else []

    def is_authorized(self, required_permissions):
        if self.admin:
            return True

        for permission in required_permissions:
            if permission not in self.permissions:
                return False

        return True
