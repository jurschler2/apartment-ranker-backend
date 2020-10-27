from project import db
from project.models.models import Apartment, Rankings, Photo, User


db.drop_all()
db.create_all()

apartment1 = Apartment(apartment_url='craigslist.org/example')
apartment2 = Apartment(apartment_url='ft.com')
r1 = Rankings(r_apartment_url='craigslist.org/example')
r2 = Rankings(r_apartment_url='ft.com')
p1 = Photo(p_apartment_url='craigslist.org/example', photo_url='abc.jpg')
p2 = Photo(p_apartment_url='ft.com', photo_url='abc.jpg')
u1 = User(user_ip_address='255.255.255.255')

apartment1.apartment_address = 'Masonic Near Fell'

db.session.add_all([apartment1, apartment2, r1, r2, p1, p2, u1])
db.session.commit()
