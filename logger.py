import os
from datetime import datetime

def logMessages(name, data, folderPath=r"C:\VINTEGO-Technik\Logs", fileName=f"profileCleanerLog.txt"):

    os.makedirs(folderPath, exist_ok=True)
    fullPath = os.path.join(folderPath, fileName)
    
    puffer = len(name)
    
    dashes : int = (50 - puffer) / 2
    
    with open(fullPath, "a", encoding="utf-8") as file:
        file.write("\n\n")
        
        for i in range(dashes):
            file.write("-")
        file.write(f" {name} ")
        for i in range(dashes):
            file.write("-")

        for i in data:
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
            file.write(f"{timestamp}" + " - " + f"{str(i)} "+" \n")
            
        for i in range(dashes-3):
            file.write("-")
        file.write(f" End{name} ")
        for i in range(dashes-3):
            file.write("-")