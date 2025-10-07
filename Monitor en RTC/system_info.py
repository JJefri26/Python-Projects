# -*- coding: utf-8 -*-

# Script de Test de psutil
import psutil
import datetime
import time
import os

while True:
    os.system('cls')
    
    # tasa de uso de cpu
    cup_per = psutil.cpu_percent()
    
    # Información de la memoria
    memory_info = psutil.virtual_memory()
    
    # Información del disco duro
    disk_info = psutil.disk_usage("/") # Información del disco del directorio raíz
    
    # Información de Internet
    net_info = psutil.net_io_counters()
    
    # Obtener la hora actual del sistema
    current_time = datetime.datetime.now().strftime("%F %T") #% F año mes día% T hora, minuto y segundo
    
    # Pantalla de mosaico
    log_str = "|---------------------|----------|----------|----------|-----------------------------|\n"
    log_str+= "|---------time--------|---cpu----|--memory--|---disk---|-------------net-------------|\n"
    log_str+= "|                     |  {}core  | {:.2f}G |  {:.2f}  |                             |\n".format(psutil.cpu_count(logical=False), 
                                                                                                          memory_info.total/1024/1024/1024, 
                                                                                                          disk_info.total/1024/1024/1024)
    log_str+= "| {} |   {}%%  |   {}%%  |   {}%%  | in:{} out:{} |\n".format(current_time, 
                                                                         cup_per, memory_info.percent, 
                                                                         disk_info.percent, 
                                                                         net_info.bytes_recv, 
                                                                         net_info.bytes_sent)
    print(log_str)
    
    time.sleep(2)