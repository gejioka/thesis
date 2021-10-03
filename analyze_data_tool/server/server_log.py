import logging

# Folder for server logging 
_logfile  = "/root/thesis/.log"

logger = None

# A dictionary with all levels of logging
LEVELS = {  "debug"     : logging.DEBUG,        
            "info"      : logging.INFO,
            "warning"   : logging.WARNING,
            "error"     : logging.ERROR,
            "critical"  : logging.CRITICAL
}

def configure_logging():
    """
    Description: Create server log and set cofiguration

    Args:
        -
    Returns:
        -
    """
    global logger
    
    logger = logging.getLogger("Server logging")
    handler = logging.FileHandler(_logfile)
    
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level=LEVELS.get("debug",logging.NOTSET))

def write_log(message:str,level:str):
    """
    Description: Method that use server to write log messages

    Args:
        message(string): Message that server write to log file
        level(string): Log level of message (DEBUG, INFO, WARNING, ERROR). 
    Returns:
        -
    """
    if level == "debug":
        logger.debug(message)
    elif level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
configure_logging()