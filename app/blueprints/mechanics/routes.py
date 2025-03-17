from flask import request, jsonify
from app.blueprints.mechanics import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from marshmallow import ValidationError
from app.models import Mechanics, db
from sqlalchemy import select, delete



#CREATE MECHANICS
@mechanics_bp.route("/", methods = ["POST"])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanics(name=mechanic_data['name'], email=mechanic_data['email'], phone=mechanic_data['phone'], salary=mechanic_data['salary'])
    
    db.session.add(new_mechanic)
    db.session.commit()
    
    return mechanic_schema.jsonify(new_mechanic), 201


#READ MECHANICS
@mechanics_bp.route("/", methods = ["GET"])
def get_mechanics():
    query = select(Mechanics)
    result = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(result), 200
    

#UPDATE MECHANICS
@mechanics_bp.route("/<int:mechanics_id>", methods = ["PUT"])
def update_mechanic(mechanics_id):
    query = select(Mechanics).where(Mechanics.id == mechanics_id)
    mechanic = db.session.execute(query).scalars().first()
    
    if mechanic == None:
        return jsonify({"message": "Invalid mechanic ID"})
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in mechanic_data.items():
        setattr(mechanic, field, value)
        
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


#DELETE MECHANICS
@mechanics_bp.route("/<int:mechanics_id>", methods = ["DELETE"])
def delete_mechanic(mechanics_id):
    query = select(Mechanics).where(Mechanics.id == mechanics_id)
    Mechanic = db.session.execute(query).scalars().first()
    
    db.session.delete(Mechanic)
    db.session.commit()
    return jsonify({"Message": f"Successfully deleted Mechanic: {mechanics_id}"})
    