from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_FILE = "products.db"

# Banco de dados: criação da tabela
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                category TEXT NOT NULL
            )
        """)
        conn.commit()

# Inicializa o banco de dados
init_db()

@app.route("/")
def index():
    """Lista todos os produtos."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    return render_template("index.html", products=products)

@app.route("/add", methods=["GET", "POST"])
def add_product():
    """Adiciona um novo produto."""
    if request.method == "POST":
        name = request.form.get("name")
        price = float(request.form.get("price"))
        quantity = int(request.form.get("quantity"))
        category = request.form.get("category")
        
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, quantity, category) VALUES (?, ?, ?, ?)",
                           (name, price, quantity, category))
            conn.commit()
        return redirect(url_for("index"))
    return render_template("form.html", action="Adicionar Produto")

@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    """Edita um produto existente."""
    if request.method == "POST":
        name = request.form.get("name")
        price = float(request.form.get("price"))
        quantity = int(request.form.get("quantity"))
        category = request.form.get("category")
        
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE products
                SET name = ?, price = ?, quantity = ?, category = ?
                WHERE id = ?
            """, (name, price, quantity, category, product_id))
            conn.commit()
        return redirect(url_for("index"))
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
    return render_template("form.html", product=product, action="Editar Produto")

@app.route("/delete/<int:product_id>")
def delete_product(product_id):
    """Exclui um produto."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
