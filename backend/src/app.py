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
            return jsonify({'mensjae': "La categoria ya se encuentra registrada"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

def pagina_no_encontrada(error):
    return "<h1> La pagina que intentas buscar no existe </h1>",404

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()