from dash import html, dcc, Dash, Input, Output, callback
from dash import dash_table
import pandas as pd
import datetime
from model import *

with db:
    #db.create_tables([Expense, Payment])
    
    #print(expenses.id, expenses.name)

    #allpayments = Payment.select().join(Expense).where(Expense.id ==2)
    expenses = Expense.select()#.get(Expense.id==2)
    allpayments = Payment.select()#.where(Payment.expense_id ==2)
    #print(allpayments)
    for pay in allpayments:
        print(pay.amount, pay.payment_date, pay.expense_id.name)
    
    #payments = [
        
    #    {'amount':13, 'payment_date':datetime.date(2021,2,13),'expense_id':expenses[0]},
    #    {'amount':14, 'payment_date':datetime.date(2021,2,14),'expense_id':expenses[1].id},
    #    {'amount':15, 'payment_date':datetime.date(2021,2,15),'expense_id':expenses[2].id},
    #    {'amount':16, 'payment_date':datetime.date(2021,2,16),'expense_id':expenses[1].id},
    #]
    #Payment.insert_many(payments).execute()
    #kom = Expense(name='Kom').save()
    #benzin = Expense.create(name='benz')
    #inet = Expense.insert(name='Int').execute()
df_expenses = pd.DataFrame(list(expenses.dicts()))
df_allpayments = pd.DataFrame(list(allpayments.dicts()))

print('Done')

app = Dash("DataBase")

dashTable_1 = dash_table.DataTable(
    data = df_expenses.to_dict('records'),
    columns = [{"name":i,"id":i} for i in df_expenses.columns ]
    )
dashTable_2 = dash_table.DataTable(
    data = df_allpayments.to_dict('records'),
    columns = [{"name":i,"id":i} for i in df_allpayments.columns ]
    )


app.layout = html.Div(
    [dashTable_1, dashTable_2]
)







#df1 = pd.read_csv('Названия сервисов.txt', header=None)
#print(df1)
#df2 = pd.read_csv('Таблица 2.txt')

#print(df2)



if __name__ == '__main__':

    app.run(debug=True)

#    print('end')
