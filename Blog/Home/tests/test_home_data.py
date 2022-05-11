import uuid
from factory import fuzzy, faker

password = str(uuid.uuid4())

registration_data = {
    'email': faker.Faker('email').generate(),
    'first_name': faker.Faker('first_name').generate(),
    'last_name': faker.Faker('last_name').generate(),
    'phone': '+380%s' % (fuzzy.FuzzyText(chars='0123456789', length=9).fuzz()),
    'password': password,
    'repeat_password': password,
}

login_data = {
    'email': faker.Faker('email').generate(),
    'password': password,
    'remember_me': True
}
