import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course_title):
    stripe_product = stripe.Product.create(name=course_title)
    return stripe_product.get('id')


def create_stripe_price(course_price, stripe_product_id):
    stripe_price = stripe.Price.create(
        currency='rub',
        unit_amount=course_price * 100,
        product_data={'name': 'payment'},
        product=stripe_product_id,
    )
    return stripe_price


def create_stripe_session(stripe_price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{
            "price": stripe_price.get('id'),
            "quantity": 1,
        }],
        mode="payment"
    )
    return session.get('id'), session.get('url')

