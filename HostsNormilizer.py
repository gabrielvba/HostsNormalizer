import os
import ipaddress
path = "c:\\Users\\User\\OneDrive\\Documentos\\GIT\\hostsNormalizer\\input"

errorList = []
tunnelList = []
multiList = []
singleList = []


class Host:
  def __init__(self,ip, name,comentado,ambiente):
    self.ip = ip
    self.name = name
    self.comentado = comentado
    self.ambiente = ambiente


def validFirstCharacter(word, key):
    return word[0] == key

def validate_ip_address(ip_string):
   try:
       ip_object = ipaddress.ip_address(ip_string)
       return True
   except ValueError:
       return False

#Remove os espacos
def cleanText(text):
    return " ".join(text.split())

#Se o primeiro elemento da lista for um ip valido associa ele a cada hostname da linha
def processTextLine(cleanTextLine,hostsList):
            ipList = cleanTextLine.split()
            #validando se a linha não é vazia 
            if len(ipList) > 0: 
                #validando se o primeiro character representa um comentario
                #Se sim remove o character de comentario para poder validar se é um ip valido
                ipNumber = ipList[0]
                comentado = False
                if validFirstCharacter(ipNumber[0],"#"): 
                    comentado = True
                    ipNumber = ipNumber[1:] 

                #validando se o primeiro elemento é um ip valido
                validIpAddress = validate_ip_address(ipNumber)
                
                #Se sim cria um obj Host para cada hostname associado ao ip
                if validIpAddress:    
                    for hostname in ipList:
                        if hostname != ipList[0]:
                            if not validFirstCharacter(hostname[0],"#"):
                                hostsList.append(Host(ipNumber,hostname,comentado,"NO"))

                #Se o primeiro elemento não é um ip valido regitra o input error               
                if not validIpAddress and ipNumber != "": errorList.append(ipNumber)

def categorizeHosts(hostsList):
        hostnameExecuted = []
        #Iniciando tratamento
        for host in hostsList:
                #1. vamos pegar todas as referencias de um hostname e agrupar
                #Validar se o Hostname ja foi executado
                hostNameIsExecuted = False
                for exec in hostnameExecuted:
                    if exec == host.name: hostNameIsExecuted = True
                
                if not hostNameIsExecuted:
                    hostnameExecuted.append(host.name)

                    #agrupando todas as referencias de um mesmo hostname
                    allReferencesOfHostname = []
                    for h in hostsList:
                        if h.name == host.name:
                            #se o ip for 127.0.0.1 vai direto para categoria de tunnel 
                            if(h.ip == "127.0.0.1"):
                                tunnelList.append(host)
                            else:
                                allReferencesOfHostname.append(h)

                    #se um mesmo hostname se referir a ips diferente ele é multi ambientes
                    isSInglereference = True
                    for r in allReferencesOfHostname:
                        if r.ip != host.ip: isSInglereference = False

                    
                    for ref in allReferencesOfHostname:
                       if isSInglereference: 
                            singleList.append(ref)
                       else:
                            multiList.append(ref)

def main():
    print("START")
    filesToExecute = [f for f in os.listdir(path)]
    print(f"Executar {len(filesToExecute)} arquivos")
    for file in filesToExecute:
        print(f"Iniciando execução de {file} ")
        text = open(os.path.join(path,file), "r", newline="")
        hostsList = []
        for textLine in text:
            #Limpa o textLine
            #Converte o textLine em Hosts-obj
            processTextLine(cleanText(textLine), hostsList)

        #pega todos os Hosts encontrados no arquivo e categoriza    
        categorizeHosts(hostsList)
        
        #SINGLE_REFERENCE: hostname associado a um unico ip -> default descomentado
        print("\n##### SINGLE_REFERENCE #####")
        for x in singleList:
            print(x.ip+" "+x.name)

        #MULTI_REFERENCE: hostname associado a mais de um ip -> deve ficar descomentado apenas uma referencias
        print("\n##### MULTI_REFERENCE #####")
        for x in multiList:
            print(x.ip+" "+x.name)
                                        
        #TUNNEL_REFERENCE: Ip = 127.0.0.1 -> default comentado
        print("\n##### TUNNEL_REFERENCE #####")
        for x in tunnelList:
            print(x.ip+" "+x.name)

        print(f"\nFinalizando execução de {file} ")
       
       
       
        print("\nerrorlist")
        print(errorList)
                

if __name__ == "__main__":
    main()