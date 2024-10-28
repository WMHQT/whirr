import psutil
import GPUtil
import time
import logging
from logger_module import log_message

def log_performance(logger_name='my_logger', cpu_threshold=80, ram_threshold=80, gpu_threshold=80):
    logger = logging.getLogger(logger_name)
    
    
    cpu_usage = psutil.cpu_percent()
    ram_info = psutil.virtual_memory()
    ram_usage = ram_info.percent
    
    try:
        gpus = GPUtil.getGPUs()
        gpu_usage = gpus[0].load * 100 if gpus else 0  
    except Exception as e:
        logger.error(f"Ошибка при получении данных о GPU: {e}")
        gpu_usage = 0

    
    log_message('info', f'CPU Usage: {cpu_usage}%, RAM Usage: {ram_usage}%, GPU Usage: {gpu_usage}%', logger_name)

    
    if cpu_usage > cpu_threshold:
        log_message('warning', f'Предупреждение: CPU Usage превышает {cpu_threshold}% ({cpu_usage}%)', logger_name)
    
    if ram_usage > ram_threshold:
        log_message('warning', f'Предупреждение: RAM Usage превышает {ram_threshold}% ({ram_usage}%)', logger_name)
    
    if gpu_usage > gpu_threshold:
        log_message('warning', f'Предупреждение: GPU Usage превышает {gpu_threshold}% ({gpu_usage}%)', logger_name)

def start_monitoring(interval=60, logger_name='my_logger'):
    while True:
        log_performance(logger_name)
        time.sleep(interval)
