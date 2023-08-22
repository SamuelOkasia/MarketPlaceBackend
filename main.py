from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
#when adding new fields to databse you need to
#db.create_all()
#db.session.commit()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
db = SQLAlchemy(app)
app.app_context().push()

class Product(db.Model):
    link = db.Column(db.String(500), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(200))
    description = db.Column(db.String(1000))
    transmission = db.Column(db.String(100))
    image = db.Column(db.String(500))
    added_on = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.String(500))
    mileage = db.Column(db.String(500))
    listed = db.Column(db.String(500))

    def to_dict(self):
        return {
            'link': self.link,
            'name': self.name,
            'description': self.description,
            'transmission': self.transmission,
            'image': self.image,
            'price': self.price,
            'mileage': self.mileage,
            'listed': self.listed,
            'added_on':self.added_on,
        }

@app.route('/api/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    #product_link = data.get("link")

    existing_product = Product.query.filter_by(link=data['link']).first()
    if existing_product:
        return jsonify({"message": "Product with this link already exists!"}), 409  # 409 Conflict

    product = Product(
        link=data['link'],
        name=data.get('name', ''),  # The `get` method provides a default value if the key doesn't exist
        description=data.get('description', ''),
        transmission=data.get('transmission', ''),
        image=data.get('image', ''),
        price=data.get('price',''),
        mileage=data.get('mileage',''),
        listed=data.get("listed",'')
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product added successfully!"})

@app.route('/api/delete', methods=['POST'])
def delete():
    Product.query.delete()
    db.session.commit()
    return jsonify(message="All products deleted successfully"), 200


@app.route('/api/get_products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

if __name__ == '__main__':
    app.run(debug=True)
