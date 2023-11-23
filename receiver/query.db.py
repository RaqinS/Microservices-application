import create_db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=create_db.engine)

session = Session()

for data in session.query(create_db.transactions).filter(create_db.transactions.price>30):
    print(data.transaction_id, "__",data.price)