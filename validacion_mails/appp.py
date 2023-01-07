from flask import Flask, render_template, redirect, request
import secrets,cripto, csv
import correo as crr
from cryptography.fernet import Fernet

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

    crr.leer_correo()

    val = True

    with open("Envio_csv/tabla_correo.csv", newline = "") as csv_info:

        informacion = csv.reader(csv_info, dialect = "excel", delimiter = ",")
        informacion = list(informacion)

        info = list(informacion)

    if len(info) > 1:
        for i in range(1, len(info)):
            if cripto.desencriptar(info[i][0]) == str(mail):
                val = False
    if val:
        key = Fernet.generate_key()
        globals()["clave"] = Fernet(key)
        globals()["mail"] = globals()["clave"].encrypt(mail.encode())
        globals()["mail_str"] = str(globals()["mail"])
        globals()[mail] = 0

        html = render_template("correo.html", token = token, mail = globals()["mail"])

        crr.enviar("validacion de mail", "-", mail, html, "")

        texto = "Para validar el correo ingrese al enlace del mail enviado."

    else:

        texto = "Correo ya validado!!"

    return render_template("espera.html", texto = texto)


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
        
        globals()[mail_[0]] += 1
        
        if globals()[mail_[0]] == 1:

            mail_cripto = [cripto.encriptar(mail_[0])]

            with open("correo.csv", "a",newline = "\n") as csv_info:

                escrito = csv.writer(csv_info, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
                escrito.writerow(mail_cripto)

            print(crr.enviar("Envio_csv", "correo.csv", "baselocaldevcop@gmail.com", "templates/correo_csv.html", "-"))

            texto = f"Mail confirmado con exito {mail_[0]}"

        else:
            
            mail_ = [globals()["clave"].decrypt(globals()["mail"]).decode()]
            texto = f"Error al confirmar el Correo: {mail_[0]}"
        
    else:
        mail_ = [globals()["clave"].decrypt(globals()["mail"]).decode()]
        texto = f"Correo ya validado!!: {mail_[0]}"

    return render_template("confirmado.html", texto = texto)

app.run(host='0.0.0.0', port=8080)