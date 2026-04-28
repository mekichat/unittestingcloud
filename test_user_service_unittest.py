import unittest
from user_service import User
from user_service import UserService
from user_service import InvalidUserDataError
from user_service import UserAlreadyExistsError
from user_service import UserNotFoundError


class FakeUserRepository:
    def __init__(self):
        self.users_by_email = {}
        self.next_id = 1

    def find_by_email(self, email):
        return self.users_by_email.get(email)
    
    def save(self, user):
        if user.id is None:
           user.id = self.next_id
           self.next_id = self.next_id + 1
        self.users_by_email[user.email] = user
        return user
    
    def list_all(self):
        return list(self.users_by_email.values())
    
class TestUserService(unittest.TestCase):
    def setUp(self):
        self.repository = FakeUserRepository()
        self.service = UserService(self.repository)


    def test_register_user_saves_user(self):
        user = self.service.register_user("Yahya", "yahya@hotmail.com")

        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "Yahya")
        self.assertEqual(user.email, "yahya@hotmail.com")
        self.assertTrue(user.active)



    def test_register_user_strips_username_and_lowercases_email(self):
        user = self.service.register_user("Yahya", "YAHYA@HOTMAIL.COM")

        self.assertEqual(user.username, "Yahya")