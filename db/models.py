from pathlib import Path
from peewee import *
from peewee import SqliteDatabase


BASE_DIR = Path(__file__).resolve().parent.parent
db_true: SqliteDatabase = SqliteDatabase(BASE_DIR / 'data.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db_true
        order_by = 'id'


class Image(BaseModel):
    name = TextField(default='', null=True)
    folder = TextField(default='', null=True)
    expansion = TextField(default='', null=True)

    local = BooleanField(default=False)
    gdrive = BooleanField(default=False)

    class Meta:
        db_table = 'images'


class Inventory(BaseModel):

    number = IntegerField(default=0)
    SKU = TextField(default='', null=True)
    Width = TextField(default='', null=True)
    Height = TextField(default='', null=True)
    Materials = TextField(default='', null=True)
    Basis = TextField(default='', null=True)
    Product_Type = TextField(default='', null=True)
    Subject = TextField(default='', null=True)
    Lot_Title = TextField(default='', null=True)
    description = TextField(default='', null=True)
    Reserve = IntegerField(default=0)
    processed = BooleanField(default=False)
    sheet_name = TextField(default='', null=True)
    picture_id = ForeignKeyField(Image, 'id', on_delete='CASCADE', null=True)

    class Meta:
        db_table = 'inventory'

db_true.connect()
db_true.create_tables([Image, Inventory])