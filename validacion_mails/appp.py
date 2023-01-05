from pathlib import Path
from flask import Flask, render_template, redirect, request
import secrets, csv, cripto
import correo as crr
from cryptography.fernet import Fernet
 
BASE_DIR = Path(__file__).resolve().parent.parent
 
globals()["token"] = ""
 
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/espera", methods = ["POST"])
def espera():
    
    token = secrets.token_urlsafe(20)
    globals()["token"] = token
    
    mail = request.form["txtmail"]
    
    key = Fernet.generate_key()
    globals()["clave"] = Fernet(key)
    globals()["mail"] = globals()["clave"].encrypt(mail.encode())
    globals()["mail_str"] = str(globals()["mail"])

    html = render_template("correo.html", token = token, mail = globals()["mail"])

    crr.enviar("validacion de mail", "-", mail, html, "")
    return render_template("espera.html")


@app.route("/<token>/<mail>")
def validar(token, mail):
    
    if token == globals()["token"]:
        salida = token
    else:
        salida = "error"
    
    return redirect(f"/confirmado/{salida}/{mail}")


@app.route("/confirmado/error/<mail>")
def error_validacion(mail):
    return render_template("error.html")


@app.route("/confirmado/<token>/<mail>")
def confirmar(token, mail):

    mail = mail.split("=")[1]

    if mail + "='"== globals()["mail_str"]:
        mail_ = [globals()["clave"].decrypt(globals()["mail"]).decode()]
        
        mail_cripto = [cripto.encriptar(mail_[0])]
        
        try: 
            with open(f"{BASE_DIR}\\validacion_mails\\correos.csv", "a",newline = "\n") as csv_file:      
                escrito = csv.writer(csv_file, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
                escrito.writerow(mail_cripto)
        except IndexError:
            print("El archivo no esta delimitado por comas, reviselo. '{directorio}\\validacion_mails\\{nombre}.csv'")

        except FileNotFoundError:
            print(f"Archivo no encontrado, revise el directorio. '{BASE_DIR}\\validacion_mails\\correos.csv'")
            
        except IOError:
            print(f"Archivo corrupto. '{BASE_DIR}\\validacion_mails\\correos.csv'")
    
        texto = f"Mail confirmado con exito {mail_[0]}"
    else:     
        mail_ = [globals()["clave"].decrypt(globals()["mail"]).decode()]
        texto = f"Error al confirmar el Correo: {mail_}" 
        
    return render_template("confirmado.html", texto = texto)

app.run(host='0.0.0.0', debug=True, port=8080)