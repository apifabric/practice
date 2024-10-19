# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()
DATABASE_URI = 'sqlite:///system/genai/temp/create_db_models.sqlite'

class Customer(Base):
    """
    description: Holds customer personal details and identifiers.
    """
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    registered_date = Column(DateTime, default=datetime.utcnow)

class Address(Base):
    """
    description: Stores address information for each customer.
    """
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)

class Product(Base):
    """
    description: Information regarding the products available for sale.
    """
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)

class Category(Base):
    """
    description: Categories that products can belong to.
    """
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

class ProductCategory(Base):
    """
    description: Link table connecting products to their categories.
    """
    __tablename__ = 'product_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

class Order(Base):
    """
    description: Customer orders with summary information.
    """
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)

class OrderDetail(Base):
    """
    description: Detailed listing of items within an order.
    """
    __tablename__ = 'order_detail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)

class Supplier(Base):
    """
    description: Suppliers providing stock for sale.
    """
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact_name = Column(String)
    phone = Column(String)
    email = Column(String)

class Inventory(Base):
    """
    description: Tracks inventory levels for products from suppliers.
    """
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('supplier.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    supplier_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

class Cart(Base):
    """
    description: Represents shopping carts of users.
    """
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

class CartItem(Base):
    """
    description: Items within shopping carts.
    """
    __tablename__ = 'cart_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('cart.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

class Review(Base):
    """
    description: Customer reviews for products.
    """
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    review_date = Column(DateTime, default=datetime.utcnow)
    rating = Column(Integer, nullable=False)  # Assume a rating scale of 1-5
    comment = Column(String)

# Create the database and tables
engine = create_engine(DATABASE_URI, echo=False)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Sample Data Insertion
# Insert a few customers
session.add_all([
    Customer(first_name="John", last_name="Doe", email="john.doe@example.com"),
    Customer(first_name="Jane", last_name="Smith", email="jane.smith@example.com"),
    Customer(first_name="Jim", last_name="Beam", email="jim.beam@example.com"),
    Customer(first_name="Betty", last_name="Boop", email="betty.boop@example.com"),
])

# Insert some addresses
session.add_all([
    Address(customer_id=1, street="123 Elm St", city="Somewhere", state="NY", zip_code="12345"),
    Address(customer_id=2, street="456 Maple St", city="Anywhere", state="CA", zip_code="67890"),
    Address(customer_id=3, street="789 Oak St", city="Everywhere", state="TX", zip_code="11223"),
])

# Insert some products
session.add_all([
    Product(name="T-Shirt", description="Comfortable cotton T-Shirt", price=19.99, stock_quantity=100),
    Product(name="Jeans", description="Stylish denim jeans", price=49.99, stock_quantity=50),
    Product(name="Sneakers", description="Sporty running sneakers", price=69.99, stock_quantity=30),
])

# Insert categories
session.add_all([
    Category(name="Apparel", description="Clothing items"),
    Category(name="Footwear", description="Shoes and sandals"),
])

# Link products to categories
session.add_all([
    ProductCategory(product_id=1, category_id=1),
    ProductCategory(product_id=2, category_id=1),
    ProductCategory(product_id=3, category_id=2),
])

# Insert suppliers
session.add_all([
    Supplier(name="Supplier A", contact_name="Alice", phone="555-1234", email="alice@supplier.com"),
    Supplier(name="Supplier B", contact_name="Bob", phone="555-5678", email="bob@supplier.com"),
])

# Insert inventory
session.add_all([
    Inventory(supplier_id=1, product_id=1, supplier_price=15.0, quantity=500),
    Inventory(supplier_id=2, product_id=2, supplier_price=35.0, quantity=200),
])

# Insert some orders
session.add_all([
    Order(customer_id=1, order_date=datetime(2023, 10, 22), total_amount=199.97),
    Order(customer_id=2, order_date=datetime(2023, 10, 23), total_amount=49.99),
])

# Insert order details
session.add_all([
    OrderDetail(order_id=1, product_id=1, quantity=2, unit_price=19.99, line_total=39.98),
    OrderDetail(order_id=1, product_id=2, quantity=3, unit_price=49.99, line_total=149.97),
    OrderDetail(order_id=2, product_id=3, quantity=1, unit_price=69.99, line_total=69.99),
])

# Insert carts
session.add_all([
    Cart(customer_id=3),
    Cart(customer_id=4),
])

# Insert cart items
session.add_all([
    CartItem(cart_id=1, product_id=1, quantity=2),
    CartItem(cart_id=1, product_id=3, quantity=1),
    CartItem(cart_id=2, product_id=2, quantity=1),
])

# Insert reviews
session.add_all([
    Review(product_id=1, customer_id=1, rating=5, comment="Great quality!"),
    Review(product_id=3, customer_id=3, rating=4, comment="Very comfortable."),
])

# Commit transactions
session.commit()

# Close the session
session.close()
