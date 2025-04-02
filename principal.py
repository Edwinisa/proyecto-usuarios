from conexion import *
from flask import Flask, render_template, request, redirect, session, send_from_directory




@principal.route("/uploads/<nombre>")
def uploads(nombre):
    return send_from_directory(principal.config['CARPETAU'],nombre)

@principal.route("/")
def index():
    return render_template("index.html")

@principal.route("/login", methods=["POST"])
def login():

    id = request.form['id']
    contra = request.form['contra']
    
    cifrada = hashlib.sha512(contra.encode("utf-8")).hexdigest()
    cursor = mi_DB.cursor()
    sql = f"SELECT nombre FROM usuarios WHERE id_usuario='{id}' and contrasena='{cifrada}'"
    cursor.execute(sql)
    
    resultado = cursor.fetchall()
    
    if len(resultado)>0:
        session["login"] = True
        session["id"] = id
        session["nombre"] = resultado[0][0]
        
        return redirect("/opciones")
    else:
        
        return render_template("index.html",msg = "Credenciales incorrectas")

@principal.route("/opciones")
def opciones():
    
    if session.get('login') == True:
        nom=session.get('nombre')
        return render_template("opciones.html", msg="Bienvenido(a) "+nom)
    else:
        return redirect("/")


@principal.route("/pacientes")
def pacientes():
    if session.get('login') == True:
        cursor = mi_DB.cursor()
        sql = "SELECT * FROM pacientes WHERE borrado=0"
        cursor.execute(sql)
    
        pacientes = cursor.fetchall()
        return render_template("pacientes.html", paci = pacientes)
    else:
        return redirect("/")

@principal.route("/nuevopaciente")
def nuevopaciente():
    if session.get('login') == True:
        return render_template("nuevopaciente.html")
    else:
        return redirect("/")

@principal.route("/guardapaciente", methods=["POST"])
def guardapaciente():
    id = request.form['id']
    nom = request.form['nom']
    cel = request.form['cel']
    foto = request.files['foto']
    cursor = mi_DB.cursor()
    sql = f"SELECT nombre FROM pacientes WHERE id_paciente='{id}'"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        ahora = datetime.now()
        tiempo = ahora.strftime("%Y%m%d%H%M%S")
        nombre,extension = os.path.splitext(foto.filename)
        nuevonombre = "P" + tiempo + extension
        foto.save("uploads/"+nuevonombre)
        sql = f"INSERT INTO pacientes (id_paciente,nombre,celular,foto) VALUES ('{id}','{nom}','{cel}','{nuevonombre}')"
        cursor.execute(sql)
        mi_DB.commit()
        return redirect("/pacientes")
    else:
        return render_template("nuevopaciente.html", msg="Id ya existe")

@principal.route("/editapaciente/<id>")
def editapaciente(id):
    if session.get('login') == True:
        cursor = mi_DB.cursor()
        sql = f"SELECT * FROM pacientes WHERE id_paciente='{id}'"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return render_template("editarpaciente.html", paci = resultado[0])
    else:
        return redirect("/")
@principal.route("/confirmapaciente", methods=['POST'])
def confirmapaciente():
    id = request.form['id']
    nom = request.form['nom']
    cel = request.form['cel']
    foto = request.files['foto']
    mi_cursor = mi_DB.cursor()
    if foto.filename!="":
        sql = f"SELECT foto FROM pacientes WHERE id_paciente='{id}'"
        mi_cursor.execute(sql)
        nombre = mi_cursor.fetchall()[0][0]
        os.remove(os.path.join(principal.config['CARPETAU'],nombre))
        ahora = datetime.now()
        tiempo = ahora.strftime("%Y%m%d%H%M%S")
        nombre,extension = os.path.splitext(foto.filename)
        nuevonombre = "P" + tiempo + extension
        foto.save("uploads/"+nuevonombre)
        sql = f"UPDATE pacientes SET foto='{nuevonombre}' WHERE id_paciente='{id}'"
        mi_cursor.execute(sql)
        mi_DB.commit()
    sql = f"UPDATE pacientes SET nombre='{nom}', celular='{cel}' WHERE id_paciente='{id}'"
    mi_cursor.execute(sql)
    mi_DB.commit()
    return redirect("/pacientes")

@principal.route("/borrapaciente/<id>")
def borrapaciente(id):
    if session.get('login') == True:
        cursor = mi_DB.cursor()
        sql = f"UPDATE pacientes SET borrado=1 WHERE id_paciente='{id}'"
        cursor.execute(sql)
        mi_DB.commit()
        return redirect("/pacientes")
    else:
        return redirect("/")



@principal.route("/usuarios")
def usuarios():
    if session.get('login') == True:
        cursor = mi_DB.cursor()
        sql = "SELECT * FROM usuarios WHERE borrado=0"
        cursor.execute(sql)
        usuarios = cursor.fetchall()
        return render_template("usuarios.html", usu = usuarios)
    else:
        return redirect("/")

@principal.route("/nuevousuario")
def nuevousuario():
    if session.get('login') == True:
        return render_template("nuevousuario.html")
    else:
        return redirect("/")
    
@principal.route("/guardausuario", methods=["POST"])
def guardausuario():
    id = request.form['id']
    nom = request.form['nom']
    contra = request.form['contra']
    cifrada = hashlib.sha512(contra.encode("utf-8")).hexdigest()
    email = request.form['email']
    cursor = mi_DB.cursor()
    sql = f"SELECT nombre FROM usuarios WHERE id_usuario='{id}'"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        sql = f"INSERT INTO usuarios (id_usuario,nombre,contrasena,email) VALUES ('{id}','{nom}','{cifrada}','{email}')"
        cursor.execute(sql)
        mi_DB.commit()
        return redirect("/usuarios")
    else:
        return render_template("nuevousuario.html", msg="Id ya existente")
    
@principal.route("/editausuario.html/<id>")
def editausuario(id):
    if session.get('login') == True:
        cursor = mi_DB.cursor()
        sql = f"SELECT * FROM usuarios WHERE id_usuario='{id}'"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return render_template("editarpaciente.html", usu = resultado[0])
    else:
        return redirect("/")

    
if __name__=="__main__":
    principal.run(host="0.0.0.0", port=9090, debug=True)

