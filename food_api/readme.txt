Steps to run the code.

Step 1:
	Open terminal.
	Create a python virtual environment in a particular folder for dependencies.
	Use "python -m venv myenv"
	then, "myenv\Scripts\activate"
Step 2:
	Install the required python packages.
	Use "pip install flask flask-restful pandas"

Step 3:
	Extract the file int the same folder.

Step 4:
	Open the terminal and run the "app.py" file in the extracted folder.
	Use "python app.py"
Step 5:
	Open new terminal in the same flolder.
	Upload the data in the database.
	Use "curl -X POST -F "file=@data.csv" http://localhost:5000/api/upload/data"
Step 6:
	Get data using product name
	Use "curl http://localhost:5000/api/product/product-name" 
	(change product-name with the specific product name)
Step 6:
	Get data using filter
	Use -> curl "http://localhost:5000/api/filter?brand=product-brand&score=product-score" 
	(Change product-brand and product-score with specific values)