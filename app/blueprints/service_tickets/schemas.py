from app.models import ServiceTickets
from app.extensions import ma


class Service_Ticket_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTickets
        fields = ['VIN', 'service_date', 'service_desc', 'customer_id','service_mechanics_ids']

service_ticket_schema = Service_Ticket_Schema()
service_tickets_schema = Service_Ticket_Schema(many=True)
        