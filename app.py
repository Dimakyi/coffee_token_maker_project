from flask import Flask, render_template, redirect, url_for, request
import stripe
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

stripe.api_key = "your_stripe_secret_key_here"

coffee_menu = [
    {"id": 1, "name": "Espresso", "price": 45.00},
    {"id": 2, "name": "Cappuccino", "price": 47.50},
    {"id": 3, "name": "Latte", "price": 36.00},
    {"id": 4, "name": "Mocha", "price": 34.50}
]

@app.route('/')
def home():
    return render_template('index.html', coffee_menu=coffee_menu)

@app.route('/order', methods=['POST'])
def order():
    coffee_ids = request.form.getlist('coffee_ids')  # Get selected coffee items
    total_price = sum([item['price'] for item in coffee_menu if str(item['id']) in coffee_ids])

    return render_template('payment.html', total_price=total_price, coffee_ids=coffee_ids)

@app.route('/payment', methods=['POST'])
def payment():
    coffee_ids = request.form.getlist('coffee_ids')
    total_price = float(request.form['total_price'])
    
    token = request.form['stripeToken']  # Get Stripe token from form
    try:
        charge = stripe.Charge.create(
            amount=int(total_price * 100),  # Convert to cents
            currency="usd",
            description="Coffee Order",
            source=token,
        )
        # Create a receipt
        receipt = {
            'order_id': str(uuid.uuid4()),  # Generate a unique token for this order
            'items': [item['name'] for item in coffee_menu if str(item['id']) in coffee_ids],
            'total_price': total_price,
        }
        return render_template('receipt.html', receipt=receipt)

    except stripe.error.StripeError as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)


