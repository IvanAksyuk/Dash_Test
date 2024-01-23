from peewee import *

db = SqliteDatabase('DataBaseTest.db')

class BaseModel(Model):
    id = PrimaryKeyField(unique=True)
    service_name = CharField(column_name='Название сервиса')
    class Meta:
        database = db
        order_by = 'id'

class Services(BaseModel):

    class Meta:
        db_table = 'Services'

class Status(BaseModel):
    
    form = CharField(column_name='Образ')
    version = CharField(column_name='Версия')
    date = DateField(column_name='Дата обновления')
    services_id = ForeignKeyField(Services)

    class Meta:
        db_table = 'Status'
