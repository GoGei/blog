import uuid
from factory import fuzzy, faker
# from core.Category.factories import CategoryFactory

password = str(uuid.uuid4())

post_form_data = {
    # 'category': CategoryFactory.create(),
    'title': fuzzy.FuzzyText(length=50),
    'text': fuzzy.FuzzyText(length=4000),
}

profile_form_data = {
    'email': faker.Faker('email').generate(),
    'first_name': faker.Faker('first_name').generate(),
    'last_name': faker.Faker('last_name').generate(),
    'phone': '+380%s' % (fuzzy.FuzzyText(chars='0123456789', length=9).fuzz()),
}

reset_password_data = {
    'password': password,
    'repeat_password': password,
}
