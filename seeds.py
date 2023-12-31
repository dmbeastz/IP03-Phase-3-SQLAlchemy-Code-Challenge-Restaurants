# seeds.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer, Restaurant, Review

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


customer1 = Customer(first_name="John", last_name="Doe")
restaurant1 = Restaurant(name="Good Eats")
review1 = Review(customer=customer1, restaurant=restaurant1, rating=4)

session.add(customer1)
session.add(restaurant1)
session.add(review1)

session.commit()


all_reviews = session.query(Review).all()
for review in all_reviews:
    print(f"Review ID: {review.id}, Customer: {review.customer.full_name()}, Restaurant: {review.restaurant.name}, Rating: {review.rating}")

average_rating = restaurant1.average_star_rating(session)
print(f"Average Star Rating for {restaurant1.name}: {average_rating}")


restaurant_reviews = restaurant1.reviews
for review in restaurant_reviews:
    print(f"Review ID: {review.id}, Rating: {review.rating}")


restaurant_customers = restaurant1.all_reviews
for customer in restaurant_customers:
    print(f"Customer: {customer.full_name()}")

found_customer = Customer.find_by_name("John Doe")
print(f"Found Customer: {found_customer.full_name()}")

customers_with_given_name = Customer.find_all_by_given_name("John")
for customer in customers_with_given_name:
    print(customer.full_name())

print(customer1.full_name())
print(customer1.favorite_restaurant().name)

customer2 = Customer(first_name="Jane", last_name="Doe")
restaurant2 = Restaurant(name="Tasty Bites")
review2 = Review(customer=customer2, restaurant=restaurant2, rating=5)

session.add(customer2)
session.add(restaurant2)
session.add(review2)

session.commit()
