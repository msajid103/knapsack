from flask import Flask, render_template, request
app = Flask(__name__)

def knapsack(capacity,weight,profit):

    # sorting values according to weight
    weight_value = sorted(weight)    
    profit_value = []
    for i in weight_value:
        profit_value.append(profit[weight.index(i)])

    # making table with first zero entries
    table = []
    for i in range(len(profit_value)+1):
        table.append([0]*(capacity+1))   

    # putting value into table
    for row in range(1,len(profit_value)+1):
        for colunm in range(1,capacity+1):
            if weight_value[row-1] <= colunm:
                table[row][colunm] = max(table[row-1][colunm],(table[row-1][colunm-weight_value[row-1]])+profit_value[row-1])
            else:
                table[row][colunm] = table[row-1][colunm]

    # back tracking
    last_index = capacity
    selected_values =sorted([])
    for i in range(len(profit_value),0,-1):
        if table[i][last_index] != table[i-1][last_index]:         
            selected_values.append(weight_value[i-1])
            last_index -= weight_value[i-1]

    return weight_value,profit_value,table,selected_values     

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        weight_capacity = int(request.form['weight_capacity'])
        weight_values = list(map(int, request.form['weight_values'].split(',')))
        profit_values = list(map(int, request.form['profit_values'].split(',')))

        # calling knapsack function for calcultaion
        weight_value,profit_value,table,selected_weights  =  knapsack(weight_capacity,weight_values,profit_values)       
        
        
        return render_template("index.html",weight=[0]+weight_value,profit =[0]+ profit_value, table=table, selected_weights=selected_weights)
    
    return render_template("index.html",weight = [],profit = [], table=[])

if __name__ == '__main__':
    app.run(debug=True)
