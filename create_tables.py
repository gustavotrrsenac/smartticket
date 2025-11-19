from models import db, Usuario, Ticket

db.connect()
db.create_tables([Usuario, Ticket])
db.close()
