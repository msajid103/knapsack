from flask import Flask, render_template, request
app = Flask(__name__)
n = 12
weights = [2, 4, 6, 3]
items =   [5, 8, 14, 10]
items = [x for _, x in sorted(zip(weights,items))]
weights = sorted(weights)
table = []
# print(weights)
for i in range(len(items)+1):
    table.append([0]*(n+1))

for i in range(1,len(items)+1):
    for w in range(1,n+1):
        if weights[i-1] <= w:
            table[i][w] = max(table[i-1][w],(table[i-1][w-weights[i-1]])+items[i-1])
        else:
            table[i][w] = table[i-1][w]

l = n
ls = []
for i in range(len(items),0,-1):
    if table[i][l] == table[i-1][l]:
        ls.append(0)

    else:
        ls.append(weights[i-1])
        l -= weights[i-1]
print(ls)


@app.route('/')
def index():
    return render_template("index.html", ta = table)

if __name__ == '__main__':
    app.run(debug=True)