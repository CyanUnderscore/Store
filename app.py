from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    #get the num
    file = open("site.csv", "r")
    content = file.readline()
    file.close()
    # clear
    file = open("site.csv", "w")
    visit_num = int(content) + 1
    #change
    file.write(str(visit_num))
    file.close
    return render_template('home.html', visit_num=visit_num)

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

@app.route('/sign_page')
def sign_page():
    return render_template('sign_page.html', sign_up_error ="")

@app.route('/sign_up', methods=['POST'])
def sign_up():
    # recuperer les informations
    pseudo = request.form['pseudo']
    email = request.form['email']
    cellNum = request.form['cellNum']
    password = request.form['Password']
    entered_data = [pseudo, email, password, cellNum]

    with open('suscriber.csv') as file:
        file_data = file.readlines()
        file_data = [info.strip('\n') for info in file_data]
        file_data = [x.split(',') for x in file_data]
    
    for row in range(len(entered_data)):
        for line in range(len(file_data)):
            if entered_data[row] == file_data[line][row] and row != 2:
                match row:
                    case 0:
                        sign_up_error = "pseudo déja pris"
                    case 1:
                        sign_up_error = "email déja utiliser pour un compte"
                    case 3:
                        sign_up_error = "un comte est deja assosié a un compte"

                return render_template('sign_page.html', sign_up_error=sign_up_error)

    with open('suscriber.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(entered_data)

    return redirect(url_for('sign_page'))

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

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)