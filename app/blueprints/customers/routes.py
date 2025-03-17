from flask import request, jsonify
from . import customers_bp
from .schemas import customer_schema, customers_schema
from marshmallow import ValidationError
from app.models import Customers, db
from sqlalchemy import select, delete



#CREATE CUSTOMERS
@customers_bp.route("/", methods = ["POST"])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customers(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    
    db.session.add(new_customer)
    db.session.commit()
    
    return customer_schema.jsonify(new_customer), 201


#READ CUSTOMERS 
@customers_bp.route("/", methods = ["GET"])
def get_customers():
    query = select(Customers)
    result = db.session.execute(query).scalars().all()
    
    return customers_schema.jsonify(result), 200
    

#UPDATE CUSTOMERS
@customers_bp.route("/<int:customers_id>", methods = ["PUT"])
def update_customer(customers_id):
    query = select(Customers).where(Customers.id == customers_id)
    customer = db.session.execute(query).scalars().first()
    
    if customer == None:
        return jsonify({"message": "Invalid Customer ID"})
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in customer_data.items():
        setattr(customer, field, value)
        
    db.session.commit()
    return customer_schema.jsonify(customer), 200


#DELETE CUSTOMERS
@customers_bp.route("/<int:customers_id>", methods = ["DELETE"])
def delete_customer(customers_id):
    query = select(Customers).where(Customers.id == customers_id)
    customer = db.session.execute(query).scalars().first()
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"Message": f"Successfully deleted user {customers_id}"})
    