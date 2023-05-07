from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    # recuperer les informations
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # mettre dans fichier csv
    with open('messages.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, email, message])

    return redirect(url_for('contact'))

@app.route('/filter_product', methods=['POST'])
def filter_product():
    category = request.form['category']
    product_list = toDico()
    if category == "":
        return render_template('products.html', products=product_list)
    selected_products = [x for x in product_list if x['category'] == category]
    return render_template('products.html', products=selected_products)

def toDico():
    file = open("database.csv", "r")
    infos = file.readlines()
    infos = [info.strip('\n') for info in infos]
    file.close()
    labels = infos[0].split(",")
    products_list = []
    for info in infos:
        if info == infos[0]:
            continue
        product = info.split(",")
        dico = {labels[x] : product[x] for x in range(len(product))}
        products_list.append(dico)
    return products_list

@app.route('/products')
def products():
    products_list = toDico()
    print(products_list)
    return render_template('products.html', products=products_list)

@app.route('/product/<id>')
def product_detailed(id):
    products_list = toDico()
    x = 0
    while products_list[x]['id'] != id and x <= len(products_list):
        x+=1
    product_info = products_list[x]
    # passer info a la page html
    return render_template('product.detail.html', product=product_info)

if __name__ == '__main__':
    app.run(debug=True)