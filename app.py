from dash import html, dcc, Dash, Input, Output, callback
from dash import dash_table

import dash_ag_grid as dag
from create_db import *

cols_names = ['service_name', 'form', 'version','date']

#Создание таблицы
def create_app():
    
    services = Services.select()
    status = Status.select()

    df_status = pd.DataFrame(list(status.dicts()))
    df_services = pd.DataFrame(list(services.dicts()))

    app = Dash("DataBase")

    table_2_dict = dict(map(lambda i,j : (i,j) , df_status.columns[1:-1],
    ["Название сервиса", "Образ", "Версия", "Дата обновления"]))

   
    
    
    dagTable_Status = dag.AgGrid(
        id = 'data-dagtable',
        rowData = df_status[df_status.columns[1:-1]].to_dict('records'),
        columnDefs=
        [
            {
            "field": i, 
            "headerName":table_2_dict[i], 
            "sortable": True if i=="service_name" else False,
            } 
            for i in df_status.columns[1:-1]
        ],
        columnSize="sizeToFit",
        style = {'height':'100vh'}

    )

    dropDown_Services = dcc.Dropdown(df_services.service_name,id='service-name-dropdown')

    dash_input = dcc.Input(
        id='my-input', 
        type='text',
        )




    app.layout = html.Div(
        [dash_input,
        dagTable_Status]
        
    )
    

    return app

@callback(
        Output('data-dagtable', 'rowData'),
        Input('my-input', 'value'),
        Input('data-dagtable','rowData'))
def update_data_table(selected_service, df_status_dict):
        
        df_status = pd.DataFrame((df_status_dict), columns = cols_names)
        
        if selected_service is None: selected_service=""
        
        if(selected_service==""):
            return pd.DataFrame(list(Status.select().dicts()), columns = cols_names).to_dict('records')
        return df_status[ [
            selected_service.replace(" ","").lower() in name
            for name in df_status.service_name
            .str.replace(" ","")
            .str.lower()]
            ].to_dict('records')

if __name__ == '__main__':
    try:
        app = create_app()
    except: 
        create_db()
        app = create_app()
    
    service_local_id_ = 1
    services_id_ = Status.get(Status.id == service_local_id_).services_id
    #print(services_id_)

    answer = Services.get(Services.id == services_id_).service_name
    #print(answer)
    app.run(debug=True)
