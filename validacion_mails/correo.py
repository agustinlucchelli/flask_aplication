import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def enviar(asunto, directorio, destinatario_, html_archivo, parm):
    try:

        #pedir datos

        username = "baselocaldevcop@gmail.com"

        while "@" not in username or "." not in username:
            
            return "Error correo invalido"


        password = "dyrpgevcgkxyhbar"
        destinatario = destinatario_


        if "@" not in destinatario or "." not in destinatario:
            
            return "Correo invalido, ingrese nuevamente."
            

        #crear mensaje
        mensaje = MIMEMultipart("alternative")
        mensaje["Subject"] = asunto
        mensaje["From"] = username
        mensaje["To"] = destinatario

        try:
            if parm == "-":
                with open(html_archivo,"r") as html_:
                    
                    texto = html_.read()

                    html = f"""

                        {texto}

                """
            else:
                
                html = html_archivo
                
            #el contenido del mensaje como html
            parte_html = MIMEText(html, "html")
            
            #agrego el html al mensaje
            mensaje.attach(parte_html)

            if directorio != "-":
                with open(directorio, "rb") as adjunto:
                    
                    contenido = MIMEBase("aplication", "octet-stream")
                    contenido.set_payload(adjunto.read())
                    encoders.encode_base64(contenido)
                    
                    directorio = directorio.split("\\")
                    directorio = "tabla_" + directorio[len(directorio)-1]
                    
                    #se configura el encabezado
                    contenido.add_header("Content-Disposition", f"attachment; filename = {directorio}", )

                    mensaje.attach(contenido)
                
        except FileNotFoundError:
            return "directorio no encontrado, revise el directorio."
                
        except IOError:
            return "directorio corrupto."
            
        mensaje_final = mensaje.as_string()

        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com",465, context = contexto) as server:
            
            server.login(username, password)
            server.sendmail(username, destinatario, mensaje_final)
            
    except smtplib.SMTPAuthenticationError:
        return "correos o contraseñas equivocados."