from flask import Flask,jsonify, request
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)

conexion=MySQL(app)

@app.route('/')
def index():
    return "Welcome"

@app.route('/expenses', methods=['GET'])
def listar_expenses():
    """This function brings all the data of the expenses made by all the users

    Returns:
        JSON : All expenses
    """
    try:
        cursor= conexion.connection.cursor()
        sql="SELECT * FROM expenses"
        cursor.execute(sql)
        datos = cursor
        expenses=[]
        for fila in datos:
            expense={'expense_id':fila[0],'user':fila[1],'amount':fila[2],'description':fila[3],'category_id':fila[4],'date':fila[5]}
            expenses.append(expense)
        return jsonify({'expenses':expenses,'mensaje':"list of expenses"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

@app.route('/expensesUser', methods=['GET'])
def leer_expenses():
    """This function brings all the data of the expenses made by the user who requests it

    Returns:
        JSON : Expenses per user
    """
    try:
        args = request.args
        user = args.get("user")
        cursor= conexion.connection.cursor()
        sql="SELECT * FROM expenses WHERE user = '{0}'".format(user)
        cursor.execute(sql)
        datos = cursor
        expenses=[]
        if datos != None:
            for fila in datos:
                expense={'expense_id':fila[0],'user':fila[1],'amount':fila[2],'description':fila[3],'category_id':fila[4],'date':fila[5]}
                expenses.append(expense)
            return jsonify({'expenses':expenses,'mensaje':"list of expenses"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})
    
@app.route("/adduser", methods=['POST'])
def agregaruser():
    """This function allows you to create a user
    
    Returns:
        JSON : messaje
    """
    try:
        cursor= conexion.connection.cursor()
        sql="SELECT * FROM users WHERE user = '{0}'".format(request.json['user'])
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos == None:
            sql="""INSERT INTO users (user, name, password)
            VALUES ('{0}','{1}',{2})""".format(request.json['user'],request.json['name'],request.json['password'])
            cursor.execute(sql)
            conexion.connection.commit() #confirma la accion de insert
            return jsonify({'mensaje':"Usuario registrado"})
        else:
            return jsonify({'mensaje':'El usuario no esta disponible'})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})
    
@app.route("/addcat", methods=['POST'])
def agregarcat():
    """This function allows you to create a new category

    Returns:
        JSON : Messaje
    """
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM categories WHERE name = '{0}'".format(request.json['name'])
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos == None:
            sql="INSERT INTO categories (name) VALUES('{0}')".format(request.json['name'])
            cursor.execute(sql)
            conexion.connection.commit() #confirma la accion de insert
            return jsonify({'mensaje': "Categoria almacenada"})
        else:
            return jsonify({'mensaje': "La categoria ya se encuentra registrada"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route("/cat", methods=['GET'])
def listarCategorias():
    """This function returns all categories

    Returns:
        JSON : List all categories
    """
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM categories"
        cursor.execute(sql)
        datos = cursor
        categories=[]
        for fila in datos:
            categorie={'category_id':fila[0],'name':fila[1]}
            categories.append(categorie)
        return jsonify({'expenses':categories,'mensaje':"list of expenses"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})
    
@app.route("/addexpenses", methods=['POST'])
def addExpenses():
    try:
        cursor = conexion.connection.cursor()
        sql = f"SELECT * FROM users WHERE user = '{request.json['user']}'"
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            sql = f"""INSERT INTO expenses (expense_id, user, amount, description, category_id, date)
            VALUES (NULL, '{request.json['user']}', {request.json['amount']}, '{request.json['description']}', {request.json['category_id']}, NOW())
            """
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "Gasto almacenado"})
        else:
            return jsonify({'mensaje': "No se encontro el usuario"})
    except Exception as ex:
        return jsonify({'mensaje': f"Error {str(ex)}"})
    
def pagina_no_encontrada(error):
    """This function sends a message if the page is not found
    Args:
        error (404): no found

    Returns:
        string: messaje no found formtat html
    """
    return "<h1> La pagina que intentas buscar no existe </h1>",404

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()