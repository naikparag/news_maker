import logging

LOG_FILE = 'app.log'

def getLogger(name):
    logging.basicConfig(
        level=logging.INFO,
        filename=LOG_FILE,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', 
        datefmt='%d-%b-%y %H:%M:%S')
    return logging.getLogger(name)
