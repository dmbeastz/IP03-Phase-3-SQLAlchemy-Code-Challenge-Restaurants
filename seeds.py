from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer, Restaurant, Review

def create_session():
    engine = create_engine('sqlite:///restaurants.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def seed_data(session):
    # Seed Customers, Restaurants, and Reviews
    customers_restaurants_reviews = [
        ("John", "Doe", "Good Eats", 4),
        ("Jane", "Doe", "Tasty Bites", 5)
    ]

    for first_name, last_name, restaurant_name, rating in customers_restaurants_reviews:
        customer = Customer(first_name=first_name, last_name=last_name)
        restaurant = Restaurant(name=restaurant_name)
        review = Review(customer=customer, restaurant=restaurant, rating=rating)

        session.add_all([customer, restaurant, review])

    session.commit()

def display_reviews(session):
    all_reviews = session.query(Review).all()
    for review in all_reviews:
        print(f"Review ID: {review.id}, Customer: {review.customer.full_name()}, "
              f"Restaurant: {review.restaurant.name}, Rating: {review.rating}")

if __name__ == '__main__':
    with create_session() as session:
        try:
            # Clear existing data (optional)
            with session.begin():
                session.query(Customer).delete()
                session.query(Review).delete()
                session.query(Restaurant).delete()

            # Seed new data
            with session.begin():
                seed_data(session)

            # Display information about the generated data
            display_reviews(session)

        except Exception as e:
            print(f"An error occurred: {e}")

    print("Finished seeding data.")
