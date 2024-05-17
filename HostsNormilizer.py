import os
import ipaddress

path = "C:\\Users\\g.botelho.alves\Downloads\\HostsNormalizer-master\\HostsNormalizer-master\\input"
outputPath = "C:\\Users\\g.botelho.alves\Downloads\\HostsNormalizer-master\\HostsNormalizer-master\\output"

ambientes = ["OLD", "", "DEV", "QA4", "PRODLIKE", "QA1", "QA6", "QA3", "PROD"]

class Host:
  def __init__(self,ip, name,comentado,ambiente,tunnel):
    self.ip = ip
    self.name = name
    self.comentado = comentado
    self.ambiente = ambiente
    self.ambientunnelte = tunnel


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
def processTextLine(cleanTextLine,hostsList, errorList):
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
                    auxList = []
                    ambiente = ""
                    tunnelInfo = ""
                    commentTag = False
                    for hostname in ipList:
                        #print(hostname)
                        if hostname != ipList[0]:
                            if not validFirstCharacter(hostname[0],"#"):
                                if not commentTag:
                                    auxList.append(hostname)
                                else:
                                    if hostname[0] == "@": ambiente = hostname[1:]
                                    if hostname[0] == "%": tunnelInfo = hostname[1:]
                            else: commentTag = True
                    for e in auxList:
                        hostsList.append(Host(ipNumber,e,comentado,ambiente,tunnelInfo))

                #Se o primeiro elemento não é um ip valido regitra o input error               
                if not validIpAddress: errorList.append(cleanTextLine)

def categorizeHosts(hostsList, tunnelList, singleList, multiList):
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
                            if(h.ip == "127.0.0.1" or h.ip=="::1"):
                                tunnelList.append(h)
                            else:
                                allReferencesOfHostname.append(h)

                    #se um mesmo hostname se referir a ips diferente ele é multi ambientes
                    isSInglereference = True
                    for r in allReferencesOfHostname:
                        if r.ip != host.ip and host.ip != "127.0.0.1": isSInglereference = False

                    for ref in allReferencesOfHostname:
                        if isSInglereference: 
                            singleList.append(ref)
                        else:
                            multiList.append(ref)

def saveNewFile(fileName, tunnelList, singleList, multiList, errorList, final):
        file_path = os.path.join(outputPath,fileName)
        with open(file_path, 'w') as file:
            file.write("\n#################### START Invalid Lines ####################\n")
            for x in errorList:
                file.write("\n"+x)
            file.write("\n####################  END  Invalid Lines ####################\n")

            #SINGLE_REFERENCE: hostname associado a um unico ip -> default descomentado
            file.write("\n\n#################### SINGLE_REFERENCE ####################")
            if(final): singleList = contraiMultHost(singleList)
            for x in singleList:
                if(x.ambiente == ""): 
                    if(x.comentado): file.write("\n#"+x.ip+"   "+x.name)
                    else:  file.write("\n"+x.ip+"   "+x.name)
                else: multiList.append(x)

            #MULTI_REFERENCE: hostname associado a mais de um ip -> deve ficar descomentado apenas uma referencias
            for a in ambientes:
                name = a
                if(a == ""): name = "CONFLITO"
                file.write(f"\n\n#################### {name} ####################")
                for x in multiList:
                    if x.ambiente == a:
                        if(x.comentado): file.write("\n#"+x.ip+"   "+x.name+" # @"+ name)
                        else:  file.write("\n"+x.ip+"   "+x.name+" # @"+ name)
                                            
            #TUNNEL_REFERENCE: Ip = 127.0.0.1 -> default comentado
            file.write("\n\n#################### TUNNEL_REFERENCE ####################")
            for x in tunnelList:
                    if(x.comentado): file.write("\n#"+x.ip+"   "+x.name)
                    else:  file.write("\n"+x.ip+"   "+x.name)
            
        print(f"\nFile '{file_path}' created successfully.")
    
def contraiMultHost(singleList):
    out = []
    for e in singleList:
        isExec = False
        for i in out:
            if i.ip == e.ip and i.ambiente == e.ambiente : isExec = True
        if(not isExec): 
            out.append(e)
        if(isExec): 
            i.name = i.name + " " + e.name
    return  out

def removeDuplicates(hostsList):
    out = []
    for e in hostsList:
        isExec = False
        isNotDiferente = True
        if(e.ip == "10.22.18.204"): print(e.name)
        for i in out:
            if(i.name == e.name and i.ip == e.ip): isExec = True
            if(isExec and i.ambiente == "" and e.ambiente != ""): 
                i.ambiente = e.ambiente
            if(isExec and i.ambiente == e.ambiente): 
                isNotDiferente = False
        if(not isExec): 
            out.append(e)
            #print("not isExec"+ e.name)
        elif(isNotDiferente):
            out.append(e)
    return  out

def main():
    print("START")
    filesToExecute = [f for f in os.listdir(path)]
    print(f"Executar {len(filesToExecute)} arquivos")

    finalVersion = []
    for file in filesToExecute:
        print(f"Iniciando execução de {file} ")
        text = open(os.path.join(path,file), "r", newline="")
        hostsList = []
        errorList = []
        tunnelList = []
        singleList = []
        multiList = []
        for textLine in text:
            #Limpa o textLine
            #Converte o textLine em Hosts-obj
            processTextLine(cleanText(textLine), hostsList, errorList)
        text.close()

        #remove hosts Duplicados
        cleanHostsList = removeDuplicates(hostsList)
        finalVersion = finalVersion + cleanHostsList
        #Categoriza todos os Hosts encontrados no arquivo   
        categorizeHosts(cleanHostsList, tunnelList, singleList, multiList)

        #Save in output
        saveNewFile(file, tunnelList, singleList, multiList, errorList, False)


        print(f"\nFinalizando execução de {file} ")
    tunnelList = []
    singleList = []
    multiList = []
    errorList = []
    print(len(finalVersion))
    cleanedList = removeDuplicates(finalVersion)
    print(len(cleanedList))

    categorizeHosts(cleanedList, tunnelList, singleList, multiList)
    saveNewFile("finalFile", tunnelList, singleList, multiList, errorList, True)

    print("END")

if __name__ == "__main__":
    main()