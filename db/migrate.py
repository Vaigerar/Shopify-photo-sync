from models import *


with db_true:
    db_true.create_tables([Inventory, Image])

print('Done')