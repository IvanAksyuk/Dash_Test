from dash import html, dcc, Dash, Input, Output, callback
from dash import dash_table

import dash_ag_grid as dag
from create_db import *


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

    input_ = dcc.Input(
        id='my-input', 
        type='text',
        )




    app.layout = html.Div(
        [input_,
        dagTable_Status]
        
    )

    @callback(
        Output('data-dagtable', 'rowData'),
        Input('my-input', 'value'))
    def update_data_table(selected_service):
        if selected_service is None: selected_service=""
        return df_status[df_status.service_name
            .str.replace(" ","")
            .str.lower()
            .str.startswith(selected_service.replace(" ","").lower())].to_dict('records')
        

    return app


if __name__ == '__main__':
    try:
        app = create_app()
    except: 
        create_db()
        app = create_app()

    app.run(debug=True)
