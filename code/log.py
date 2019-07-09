import logging
import argparse
from global_variables import *

logger = None

def configure_logging(args):
    """
    Description: Configure logging

    Args:
        args(object): A variable with all arguments of user
    Returns:
        -
    """
    global logger

    logger = logging.getLogger('Backbone for multi-layer ad hoc network')
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if args.logLevel:
        logger.setLevel(level=LEVELS.get(args.logLevel,logging.NOTSET))
    else:
        logger.setLevel(level=LEVELS.get("debug",logging.NOTSET))

def write_message(args,message,message_type):
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