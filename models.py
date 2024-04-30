from peewee import *

db = SqliteDatabase('Users.db')

class User(Model):
    name = CharField(max_length=50)
    email = CharField(max_length=50, unique=True)
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=30)

    class Meta:
        database = db

class Emission(Model):
    total_emission = FloatField()
    electricity = FloatField()
    private_travel = FloatField()
    gas_connection = FloatField()
    wood_used = FloatField()
    air_travel = FloatField()
    waste_generated = FloatField()
    train_travel = FloatField()
    food = FloatField()
    bus_travel = FloatField()
    month = CharField()
    year = IntegerField()

    user = ForeignKeyField(User, backref='emissions')

    class Meta:
        database = db

def add_user(user_data):
    try:
        new_user = User.create(
            name = user_data['name'],
            username = user_data['username'],
            email = user_data['email'],
            password = user_data['password']
        )
        print('user added')

        return new_user
    except IntegrityError as e:
        print("email or username is not unique")

def get_emission(username, month, year):
    user = User.get(User.username == username)
    emissions = Emission.select().where(Emission.user == user, Emission.month == month, Emission.year == year).first()

    return emissions

def get_user(username):
    user = User.get(User.username == username)
    return user

def add_emission(emission_data, the_user):
    emission = Emission.create(
        electricity = emission_data['electricity'],
        gas_connection = emission_data['gas_connection'],
        air_travel = emission_data['air_travel'],
        train_travel = emission_data['train_travel'],
        bus_travel = emission_data['bus_travel'],
        private_travel = emission_data['private_travel'],
        wood_used = emission_data['wood_used'],
        waste_generated = emission_data['waste'],
        food = emission_data['food'],
        user = the_user,
        total_emission = emission_data['total_emission'],
        month = emission_data['month'],
        year = emission_data['year']
    )

    print("Emission instance successfully added")

    return emission

# if Emission.table_exists():
#     db.connect()
#     Emission.drop_table()
#     print("dropped")
#     db.close()

db.connect()
db.create_tables([User, Emission])
