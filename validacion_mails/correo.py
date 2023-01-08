import smtplib, ssl, os, imaplib, webbrowser, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header


def enviar(asunto, directorio, destinatario_, html_archivo, parm):
    try:

        #pedir datos

        username = "mail"

        while "@" not in username or "." not in username:
            
            return "Error correo invalido"


        password = "password_api"
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
    
    
def leer_correo():
    
    #datos del correo
    username = "mail"
    password = "password_api"
    
    #crear conexion 
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    
    #iniciar sesion
    imap.login(username, password)
    status, mensaje = imap.select("INBOX")
    
    #cantidad total de mensajes
    
    mensaje = int(mensaje[0])
    
    N = 5 + int(mensaje/10)
    
    for i in range(mensaje, mensaje - N, -1):
        
        try:
            
            res, mensaje = imap.fetch(str(i), "(RFC822)")
        except:
            
            break
        
        for respuesta in mensaje:
            
            if isinstance(respuesta, tuple):
                
                #obtener contenido
                mensaje = email.message_from_bytes(respuesta[1])
                
                #decodificar el contenido
                subject = decode_header(mensaje["Subject"])[0][0]
                if isinstance(subject, bytes):
                    #convertir a string
                    subject = subject.decode()
                    
                #de donde viene el correo
                from_ = mensaje.get("From")
                data_ = mensaje.get("Date")
                #print("Subject: " , subject )
                #print("From: " , from_)
                #print("Date: " , data_)
                
                #si el correo es html
                if mensaje.is_multipart():
                    
                    #recorrer las partes del correo 
                    for part in mensaje.walk():
                        
                        #extraer el contenido
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        
                        try:
                            
                            #Cuerpo del mensaje
                            body = part.get_payload(decode = True).decode()

                        except:
                            pass
                        
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            
                            #mostrar el cuerpo del correo
                            texto_salida_plana = body
                        
                        elif "attachment" in content_disposition:
                            
                            #download attachment
                            nombre_archivo = part.get_filename()
                            if nombre_archivo:

                                if subject == "Envio_csv":
                                    if not os.path.isdir(subject):
                                        
                                        #crear una carpeta para el mensaje
                                        os.mkdir(subject)
                                
                                    ruta_archivo = os.path.join(subject, nombre_archivo)
                                    
                                    #download attachment and save it
                                    
                                    open(ruta_archivo, "wb").write(part.get_payload(decode = True))
                                else:
                                    pass
