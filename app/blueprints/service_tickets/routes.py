from flask import request, jsonify
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.service_tickets.schemas import service_ticket_schema
from marshmallow import ValidationError
from app.models import ServiceTickets, db
from sqlalchemy import select, delete
from app.models import Customers



#CREATE SERVICE TICKETS
@service_tickets_bp.route("/", methods = ["POST"])
def create_service_tickets():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service = ServiceTickets(
        VIN=service_ticket_data['VIN'],
        service_date=service_ticket_data['service_date'],
        service_desc=service_ticket_data['service_desc']
    )
    
    customer_id = service_ticket_data['customer_id']
    
    query = select(Customers).where(Customers.id == customer_id)
    customer = db.session.execute(query).scalar_one_or_none()
    
    if not customer:
        return jsonify({"message": "Customer ID not found"}), 400
        
    new_service.customer_id = customer_id
    
    db.session.add(new_service)
    db.session.commit()
    
    return service_ticket_schema.jsonify(new_service), 201

#READ SERVICE TICKETS
@service_tickets_bp.route("/", methods = ["GET"])
def get_service_tickets():
    query = select(ServiceTickets)
    result = db.session.execute(query).scalars().all()
    
    return service_ticket_schema.jsonify(result, many=True), 200