from flask import Flask, request, jsonify
import mysql.connector
import pandas as pd

app = Flask(__name__)


# In-memory data
# foods = [
    # Add more food items as needed
# ]


# MySQL database 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="my_food_app"
)
cursor = db.cursor(dictionary=True)

# Create the 'foods' table in the database
create_table_query = """
CREATE TABLE IF NOT EXISTS foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(255),
    serving_size FLOAT,
    serving_unit VARCHAR(50),
    score INT
)
"""
cursor.execute(create_table_query)
db.commit()

# Create an upload API endpoint( e.g. /api/upload/data) to insert data into database
@app.route('/api/upload/data', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            data = pd.read_csv(file)
            for _, row in data.iterrows():
                insert_query = "INSERT INTO foods (name, brand, serving_size, serving_unit, score) VALUES (%s, %s, %s, %s, %s)"
                data_values = (row["name"], row["brand"], row["serving_size"], row["serving_unit"], row["score"])
                cursor.execute(insert_query, data_values)
                db.commit()
            return jsonify({"message": "Data uploaded successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Create a Get API endpoint( e.g. /api/product/{name}) to get product details based on product name.
@app.route('/api/product/<string:name>', methods=['GET'])
def get_product(name):
    # Search for products with a name that matches or contains the provided name
    query = "SELECT * FROM foods WHERE name LIKE %s"
    cursor.execute(query, (f"{name}",))
    products = cursor.fetchall()
    
    if products:
        return jsonify(products)
    else:
        # If no exact matches are found, check for similar products
        similar_query = "SELECT name FROM foods WHERE name LIKE %s"
        cursor.execute(similar_query, (f"%{name}%",))
        similar_products = cursor.fetchall()

        if similar_products:
            similar_product_names = [product["name"] for product in similar_products]
            return jsonify({
                "error_code": 404,
                "error_message": "Product not found, however, some products exist with similar names",
                "similar_products": similar_product_names
            }), 404
        else:
            return jsonify({"error": "Product not found"}), 404

# Create a filter API ( /api/filter) to filter data based on brand and score
@app.route('/api/filter', methods=['GET'])
def filter_data():
    brand = request.args.get('brand')
    score = int(request.args.get('score', 0))
    
    query = "SELECT * FROM foods WHERE brand LIKE %s AND score = %s"
    cursor.execute(query, (f"%{brand}%", score))
    filtered_data = cursor.fetchall()
    
    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
