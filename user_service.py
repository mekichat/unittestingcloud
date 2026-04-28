class User:
    def __init__(self, id, username, email, active=True):
        self.id = id
        self.username = username
        self.email = email
        self.active = active
class UserAlreadyExistsError(Exception):
    pass
class InvalidUserDataError(Exception):
    pass
class UserNotFoundError(Exception):
    pass


class UserService:
    def __init__(self, repository):
        self.repository = repository
    def register_user(self, username, email):
        username = username.strip()
        email = email.strip().lower()         
        if len(username) < 2:
            raise InvalidUserDataError("Username must be atleast 2 character")   
        
        if "@" not in email:
            raise InvalidUserDataError("Email must contain @")
        
        existing_user = self.repository.find_by_email(email)
        if existing_user is not None:
            raise UserAlreadyExistsError("Email already registered")
        user = User(None, username, email, True)
        saved_user = self.repository.save(user)    
        return saved_user
    
    def deactive_user(self, email):
        email = email.strip().lower()
        
        user = self.repository.find_by_email(email)

        if user is None:
            raise UserNotFoundError("User not found")

        user.active = False

        saved_user = self.repository.save(user)

        return saved_user
    
    def get_active_users(self):
        users = self.repository.list_all()
        active_users = []
        for user in users:
            if user.active:
                active_users.append(user)
        return active_users

    def change_username(self, email, new_username):
        email = email.strip().lower()
        new_username = new_username.strip()
        if len (new_username) < 2:
            raise InvalidUserDataError("Username must be atleast 2 characters")
        
        user = self.repository.find_by_email(email)
        if user is None:
            raise UserNotFoundError("User not found")
        
        user.username = new_username
        saved_user = self.repository.save(user)
        return saved_user