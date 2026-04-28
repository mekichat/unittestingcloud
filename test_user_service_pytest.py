import pytest

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
    
@pytest.fixture
def repository():
    return FakeUserRepository()

@pytest.fixture
def service(repository):
    return UserService(repository)


def test_register_user_saves_user(service):
    user = service.register_user("Yahya", "yahya@hotmail.com")

    assert user.id == 1
    assert user.username == "Yahya"
    assert user.email == "yahya@hotmail.com"
    assert user.active is True



def test_register_user_strips_username_and_lowercases_email(service):
    user = service.register_user("Yahya", "YAHYA@HOTMAIL.COM")

    assert user.username == "Yahya"
    assert user.email == "yahya@hotmail.com"
    



@pytest.mark.parametrize(
    "username, email",
   [
    ("", "yahya@hotmail.com"),
    ("y", "yahya@hotmail.com"),
    ("Yahya", "not an email")
   ]
)
def test_register_user_rejects_invalid_data(service, username, email):
    with pytest.raises(InvalidUserDataError):
        service.register_user(username, email)



def test_register_user_rejects_duplicate_email(service):
    service.register_user("Yahya", "yahya@hotmail.com")

    with pytest.raises(UserAlreadyExistsError):
        service.register_user("tomas", "yahya@hotmail.com")



def test_deactive_user_sets_active_to_false(service):
    service.register_user("Yahya", "yahya@hotmail.com")

    user = service.deactive_user("yahya@hotmail.com")
    assert user.active is False   

def test_get_active_users_only_returns_active_users(service):
        service.register_user("Yahya", "yahya@hotmail.com")
        service.register_user("tomas", "tomas@hotmail.com")
        service.register_user("Mekuria", "mekuria@hotmail.com")

        service.deactive_user("tomas@hotmail.com")

        active_users = service.get_active_users()

        assert len(active_users) == 2
        assert active_users[0].email == "yahya@hotmail.com"
        assert active_users[1].email == "mekuria@hotmail.com"

def test_change_username_updates_username(service):
        service.register_user("Yahya", "yahya@hotmail.com")
        user = service.change_username("yahya@hotmail.com", "    tomas     ")
        assert user.username == "tomas"

def test_change_username_rejects_short_username(service):
    service.register_user("Yahya", "yahya@hotmail.com")
    
    with pytest.raises(InvalidUserDataError):
        service.change_username("yahya@hotmail.com", "a")

def test_change_username_rejects_unknow_user(service):
    with pytest.raises(UserNotFoundError):
        service.change_username("missing@test.se", "yahya")