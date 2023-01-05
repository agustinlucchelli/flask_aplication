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
            mail_[i] = "0" + mail__
        else:
            if mail_[i] in lista:
                mail__ = str(lista.index(mail_[i]))
            else:
                mail__ = mail_[i]
            mail_[i] = "!_" + mail__
            
    return "".join(mail_) + ";row;" + mail[1]

def desencriptar(mail):
    mail = mail.split("!_")

    for i in range(len(mail)):
        
        mail[i] = mail[i].replace("0", "-")
        if mail[i] == "--":
            mail[i] = "a"
        elif "--" in mail[i]:
            mail[i] = mail[i].replace("--", "a")

    for i in range(len(mail)):
        
        if "-" in mail[i]:
            mail_ = mail[i].split("-")
            if "." in mail_[0]:
                mail[i] = mail_[0].replace(".", "") + lista[int(mail_[1])]
            elif "." in mail_[1]:
                mail[i] = lista[int(mail_[0])] + mail_[1].replace(".", "")
            else:
                mail[i] = lista[int(mail_[0])] + lista[int(mail_[1])]
                
                
        elif len(mail[i]) > 1:
            if mail[i].index("a") == 0:
                mail[i] = "a" + lista[int(mail[i].replace("a", ""))]
            else:
                mail[i] = lista[int(mail[i].replace("a", ""))] + "a"
                
    return "".join(mail)

    