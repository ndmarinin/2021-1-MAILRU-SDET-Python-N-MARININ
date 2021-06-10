import string
import random

from faker import Faker


def create_user(valid_email=True, valid_username=True, valid_password=True):
    faker = Faker()
    username = faker.name()
    email = faker.email()
    password = faker.password()
    username = username.split(' ')[0] + str(random.randint(0, 100))
    if len(username) < 6:
        username += 'qa'
        username += str(random.randint(0, 100))

    if not valid_email:
        email = password
    if not valid_username:
        username = faker.random_number(digits=3)
    if not valid_password:
        password = ''
    return username, email, password