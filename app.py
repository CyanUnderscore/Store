from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


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
    # transferer info cers html

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