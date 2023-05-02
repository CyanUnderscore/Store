from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/products')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    # lis fichier csv 
    # transferer info cers html
    products_list = [[]]
    return render_template('products.html', products=products_list)

@app.route('/product/<id>')
def product_detailed(id):
    # lire csv et recup info
    # passer info a la page html
    product_info = [[]]
    return render_template('product.detailed.html', product=product_info)

if __name__ == '__main__':
    app.run(debug=true)