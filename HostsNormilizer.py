import os
import ipaddress
path = "c:\\Users\\User\\OneDrive\\Documentos\\GIT\\hostsNormalizer\\input"

errorList = []
hostnamesList = []

class Ip:
  def __init__(self,id, host,comentado,ambiente):
    self.id = id
    self.host = host
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


def main():
    print("START")
    filesToExecute = [f for f in os.listdir(path)]
    print(f"Execute {len(filesToExecute)} arquivos")
    for file in filesToExecute:
        arquivos = open(os.path.join(path,file), "r", newline="")
        for arquivo in arquivos:
            textLine = " ".join(arquivo.split())

            ipList = textLine.split()
            if len(ipList) > 0: 
                ipNumber = ipList[0]
                comentado = False
                if validFirstCharacter(ipNumber[0],"#"): 
                    comentado = True
                    ipNumber = ipNumber[1:]
                validIpAddress = validate_ip_address(ipNumber)
                if not validIpAddress and ipNumber != "": errorList.append(ipNumber)


                ##### SABEMOS SE  É VALIDO E SE ESTA COMENTADO
                if validIpAddress:    
                    for hostname in ipList:
                        if hostname != ipList[0]:
                            if not validFirstCharacter(hostname[0],"#"):
                                hostnamesList.append(Ip(ipNumber,hostname,comentado,"NO"))
       
       
       
        print("errorlist")
        print(errorList)
        print("hostnamesList")
        print(len(hostnamesList))
        for x in hostnamesList:
            print(x.host)
                

if __name__ == "__main__":
    main()