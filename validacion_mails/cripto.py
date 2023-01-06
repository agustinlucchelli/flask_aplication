def encriptar(mail):
    mail = mail.split("@")
    mail_ = list(mail[0])
    lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for i in range(len(mail_)):
        if i % 2 == 0:
            if mail_[i] in lista:
                mail__ = str(lista.index(mail_[i]))
            else:
                mail__= mail_[i] + "."
            mail_[i] = "0" + mail__ + "0"
        else:
            if mail_[i] in lista:
                mail__ = str(lista.index(mail_[i]))
            else:
                mail__ = mail_[i] + "."
            mail_[i] = "!_" + mail__ +"!_"
            
    return "".join(mail_) + ";row;" + mail[1]

def desencriptar(mail):
    
    lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    mail_parm = mail.split(";row;")
    mail = mail_parm[0].split("!_")
    if mail[len(mail)-1] == "":
        mail.pop(len(mail)-1)

    for i in range(len(mail)):
        
        if len(mail[i]) > 2:
            mail[i] = mail[i][1:len(mail[i])-1]
        if "." not in mail[i]:    
            mail[i] = lista[int(mail[i])]
        else:
            mail[i] = mail[i].replace(".", "")
                
    return "".join(mail) + "@" +mail_parm[1]
