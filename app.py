from flask import Flask, render_template, request
app = Flask(__name__)

def knapsack(capacity,weight,profit):
    weight_value, profit_value = map(list, zip(*sorted(zip(weight, profit))))

    # sorting values according to weight
    # weight_value = sorted(weight)    
    # profit_value = []
    # for i in weight_value:
    #     profit_value.append(profit[weight.index(i)])

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
    prof = 0
    for i in range(len(profit_value),0,-1):
        if table[i][last_index] != table[i-1][last_index]:         
            selected_values.append(i)
            prof += profit_value[i-1]
            last_index -= weight_value[i-1]
   

    return prof, weight_value,profit_value,table,selected_values     


def fractional_knapsack(capacity,weight,profit):

    fractional_value = []
    for i in range(len(weight)):
        if weight[i] != 0:
            fractional_value.append(round(profit[i]/weight[i],2))
        else:
            fractional_value.append(0)


    sorted_values = sorted(zip(fractional_value, profit, weight), reverse=True)
    fraction, profit_value, weight_value = map(list, zip(*sorted_values))

# Print the sorted lists
    print(profit_value)
    print(weight_value)
 
    # fraction = sorted(fractional_value, reverse=True)    
    # profit_value = []
    # weight_value = []
    # for i in fraction:
    #     profit_value.append(profit[fractional_value.index(i)])
    #     weight_value.append(weight[fractional_value.index(i)])
        
    profit_no = 0
    remainin_weight = capacity
    ind = 0
    for i in range(len(weight_value)):
        ind += 1
        if remainin_weight > weight_value[i]:
            profit_no += profit_value[i]
            remainin_weight -= weight_value[i]        
        elif weight_value[i] != 0:
            profit_no += (remainin_weight/weight_value[i])*profit_value[i]
            break
    return round(profit_no,2),fraction, profit_value  , weight_value ,ind 




    

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        weight_capacity = int(request.form['weight_capacity'])
        weight_values = list(map(int, request.form['weight_values'].split(',')))
        profit_values = list(map(int, request.form['profit_values'].split(',')))
       
        # calling knapsack function for calcultaion
        prof,weight_value,profit_value,table,selected_weights  =  knapsack(weight_capacity,weight_values,profit_values) 

        profit_val,fraction, profit_ls, weight_ls, ind  = fractional_knapsack(weight_capacity,weight_values,profit_values)           
        return render_template("index.html",prof = prof, weight=[0]+weight_value,profit =[0]+ profit_value, table=table, selected_weights=selected_weights,profit_val =profit_val,fraction = fraction, profit_ls = profit_ls, weight_ls=weight_ls,ind = ind)
    
           
    return render_template("index.html",weight = [],profit = [], table=[])

if __name__ == '__main__':
    app.run(debug=True)
