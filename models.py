# models.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, desc
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reviews = relationship("Review", back_populates="customer")

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self, session):
        return max(self.reviews, key=lambda review: review.rating).restaurant

    def add_review(self, session, restaurant, rating):
        new_review = Review(customer=self, restaurant=restaurant, rating=rating)
        self.reviews.append(new_review)
        session.add(new_review)

    def delete_reviews(self, session, restaurant):
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
            self.reviews.remove(review)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    reviews = relationship("Review", back_populates="restaurant")

    def all_reviews(self, session):
        reviews = session.query(Review).filter_by(restaurant_id=self.id).all()
        return [f"Review for {self.name} by {review.customer.full_name()}: {review.rating} stars." for review in reviews]

    def average_star_rating(self, session):
        ratings = [review.rating for review in self.reviews]
        return sum(ratings) / len(ratings) if ratings else 0

    @classmethod
    def fanciest(cls, session):
        return session.query(Restaurant).order_by(desc(Restaurant.price)).first()
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer = relationship("Customer", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")
    
    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.rating} stars."

    @classmethod
    def all(cls, session):
        return session.query(Review).all()
