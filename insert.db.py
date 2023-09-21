import create_db
from sqlalchemy.orm import sessionmaker
import random

Session = sessionmaker(bind=create_db.engine)

session = Session()

for i in range(10,20):
    item_id = random.randint(0,500)
    price= random.randint(10,50)
    
    tr = create_db.transactions(i,'2023-09-20', item_id,price)

    session.add(tr)

session.commit()