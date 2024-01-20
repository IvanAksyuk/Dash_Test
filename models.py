from peewee import *

db = SqliteDatabase('DataBaseTest.db')

class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'

class Services(BaseModel):
   
    service_name = CharField()

    class Meta:
        db_table = 'Services'

class Status(BaseModel):
    
    service_name = CharField()
    form = CharField()
    version = CharField()
    date = DateField()
    services_id = ForeignKeyField(Services)

    class Meta:
        db_table = 'Status'
