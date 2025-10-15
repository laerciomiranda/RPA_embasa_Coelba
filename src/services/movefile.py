import os
import time
from datetime import datetime
import shutil
from pathlib import Path

class Movefile:
    
    def __init__(self):
        self.download_folder = os.path.expanduser("~\Downloads")
        self.dest_folder = os.path.join(os.getcwd(), "files\Faturas")
        
    def get_latest_file(self, unidade, competencia, empresa = "Coelba"):
        destino = self.dest_folder + "\\" + empresa + "\\" + unidade + "\\" + competencia.replace("/","_")
        if not os.path.exists(destino):
            os.makedirs(destino)
        
        files = []
        latest_file = None
        if empresa == "Embasa":
            print("embasa")
            files = [
                os.path.join(self.download_folder, f)
                for f in os.listdir(self.download_folder)
                if os.path.isfile(os.path.join(self.download_folder, f)) and "segunda" in f.lower()
            ]
            latest_file = max(files, key=os.path.getctime) if files else None
            
        if empresa == "Coelba":
            print("Coelba")
            files = [
                os.path.join(self.download_folder, f)
                for f in os.listdir(self.download_folder)
                if os.path.isfile(os.path.join(self.download_folder, f)) and "segunda" not in f.lower()
            ]
            latest_file = max(files, key=os.path.getctime) if files else None
            
        if empresa == "SAAE":
            print("SAAE")
            files = [
                os.path.join(self.download_folder, f)
                for f in os.listdir(self.download_folder)
                if os.path.isfile(os.path.join(self.download_folder, f)) and "segundaVia" in f.lower()
            ]
            latest_file = max(files, key=os.path.getctime) if files else None
            print(latest_file)
        
        if latest_file:
            print("achou o arquivo")
            file_extension = os.path.splitext(latest_file)[1]
            link = os.path.splitext(latest_file)[0].split("\\")
            index = len(link)
            file_name = link[index -1]
            
            if(file_extension != ".pdf"):
                return False
            
            if "Segunda" in file_name and empresa == "Embasa":
                new_filename = f"conta_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
                new_filepath = os.path.join(destino, new_filename)
                shutil.move(latest_file, new_filepath)
            
                return new_filepath
            
            if empresa == "Coelba":
                new_filename = f"conta_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
                new_filepath = os.path.join(destino, new_filename)
                shutil.move(latest_file, new_filepath)
            
                return new_filepath
            
            if empresa == "SAAE":
                new_filename = f"conta_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
                new_filepath = os.path.join(destino, new_filename)
                shutil.move(latest_file, new_filepath)
            
                return new_filepath
            
    
    def get_latest_file_1(self, unidade, competencia, empresa = "Coelba"):
        
        destino = os.path.join(self.dest_folder, empresa, unidade, competencia.replace("/","_"))
        if not os.path.exists(destino):
            os.makedirs(destino)
        
        files = []
        latest_file = None

        filter_criteria = {
            "Embasa": lambda f_name: "segunda" in f_name.lower(),
            "Coelba": lambda f_name: "segunda" not in f_name.lower(),
            "SAAE": lambda f_name: "segundavia" in f_name.lower(),
        }

        current_filter = filter_criteria.get(empresa)
        if not current_filter:
            print(f"Erro: Critério de filtro não definido para a empresa '{empresa}'.")
            return None

        files = [
            os.path.join(self.download_folder, f)
            for f in os.listdir(self.download_folder)
            if os.path.isfile(os.path.join(self.download_folder, f)) and current_filter(f)
        ]
        
        latest_file = max(files, key=os.path.getmtime) if files else None
                        
        if latest_file:
            file_extension = os.path.splitext(latest_file)[1]
            file_name = os.path.basename(latest_file)
            
            if file_extension.lower() != ".pdf":
                return False
            
            if (empresa == "Embasa" and "segunda" in file_name.lower()) or \
               (empresa == "Coelba") or \
               (empresa == "SAAE"):
                
                new_filename = f"conta_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
                new_filepath = os.path.join(destino, new_filename)
                
                try:
                    shutil.move(latest_file, new_filepath)
                    return new_filepath
                except Exception as e:
                    return False
            else:
                return False
        else:
            return False