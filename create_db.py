from models import *
import pandas as pd


#Заполнение базы данных
def create_db():
    with db:
        try:
            db.drop_tables([Services, Status])        
        finally:
            db.create_tables([Services, Status])
        df_services = pd.read_csv("Названия сервисов.txt", names = ['service_name'],header=None)
        list_of_dicts_df_services = df_services.to_dict('records')
        
        Services.insert_many(list_of_dicts_df_services).execute()

        df_status = pd.read_csv("Таблица 2.txt",sep='\t', on_bad_lines='skip', names = ['service_name', 'form', 'version','date'])

        services = [Services.get(Services.service_name == str(service_name_)).id for service_name_ in df_status.service_name]
        
        df_status['services_id'] = services
        list_of_dicts_df_status = df_status.to_dict('records')
        
        Status.insert_many(list_of_dicts_df_status).execute()








