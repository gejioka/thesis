import logging
import argparse
from global_variables import *

logger = None

def configure_logging(args:argparse.ArgumentParser):
    """
    Description: Configure logging

    Args:
        args(object): A variable with all arguments of user
    Returns:
        -
    """
    global logger

    logger = logging.getLogger('Backbone for multi-layer ad hoc network')
    if args.store_log:
        handler = logging.FileHandler(args.log_file+args.file_id)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if args.logLevel:
        logger.setLevel(level=LEVELS.get(args.logLevel,logging.NOTSET))
    else:
        logger.setLevel(level=LEVELS.get("debug",logging.NOTSET))

def write_process_message(args:argparse.ArgumentParser,process_number:int,mcds:bool):
    """
    Description: Write log message for algorithm process

    Args:
        args(object): A variable with all arguments of user
        process_number(int): A variable which contains process number
    Returns:
        -
    """
    if args.algorithm == "1":
        if mcds:
            write_message(args,"Process "+str(process_number)+" of 5","INFO",True)
        else:
            write_message(args,"Process "+str(process_number)+" of 4","INFO",True)
    elif args.algorithm == "2":
        if mcds:
            write_message(args,"Process "+str(process_number)+" of 6","INFO",True)
        else:
            write_message(args,"Process "+str(process_number)+" of 5","INFO",True)
    else:
        if mcds:
            write_message(args,"Process "+str(process_number)+" of 4","INFO",True)
        else:
            write_message(args,"Process "+str(process_number)+" of 3","INFO",True)

def write_message(args:argparse.ArgumentParser,message:str,message_type:str,time_flag=False):
    """
    Description: Write log message to console

    Args:
        args(object): A variable with all arguments of user
        message(String): A variable with log message
    Returns:
        -
    """
    global logger 

    if args.log:
        if message_type.upper() == "DEBUG":
            logger.debug(message)
        elif message_type.upper() == "INFO":
            logger.info(message)
        elif message_type.upper() == "WARNING":
            logger.warning(message)
        elif message_type.upper() == "ERROR":
            logger.error(message)
    elif args.time:
        if time_flag:
            if message_type.upper() == "DEBUG":
                logger.debug(message)
            elif message_type.upper() == "INFO":
                logger.info(message)
            elif message_type.upper() == "WARNING":
                logger.warning(message)
            elif message_type.upper() == "ERROR":
                logger.error(message)