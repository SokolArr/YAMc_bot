from datetime import datetime
import logging

FORMAT = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(filename="/logs/main.log", level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

def dttm() -> str:
    return str(datetime.now()) + ' | '

def write_log(message, global_options = None, chat_id = None, thread_id = None, exception = None, state = 'Info'):
    try:
        if(exception or state == 'Error'):
            state = 'Error'
            if(global_options):
                if(global_options.get_mode() == 1):
                    log_message = 'chat_id: ' + str(chat_id) + '; thread_id: ' + str(thread_id) + '; message: ' + str(message) + '; exception: ' + str(exception)
                    print(dttm(),state + ': ' + log_message)
                    logger.error(log_message)
                else:
                    log_message = 'message: ' + str(message) + '; exception: ' + str(exception)
                    print(dttm(),state + ': ' + log_message)
                    logger.error(log_message)
            else:
                log_message = 'message: ' + str(message) + '; exception: ' + str(exception)
                print(dttm(),state + ': ' + log_message)
                logger.error(log_message)
        elif(state == 'Warn'):
            if(global_options):
                if(global_options.get_mode() == 1):
                    log_message = 'chat_id: ' + str(chat_id) + '; thread_id: ' + str(thread_id) + '; message: ' + str(message)
                    print(dttm(),state + ': ' + log_message)
                    logger.warn(log_message)
                else:
                    log_message = 'message: ' + str(message)
                    print(dttm(),state + ': '  + log_message)
                    logger.warn(log_message)
            else:
                log_message = 'message: ' + str(message)
                print(dttm(),state + ': ' + log_message)
                logger.warn(log_message)
        else:
            if(global_options):
                if(global_options.get_mode() == 1):
                    log_message = 'chat_id: ' + str(chat_id) + '; thread_id: ' + str(thread_id) + '; message: ' + str(message)
                    print(dttm(),state + ': ' + log_message)
                    logger.info(log_message)
                else:
                    log_message = 'message: ' + str(message)
                    print(dttm(),state + ': ' + log_message)
                    logger.info(log_message)
            else:
                log_message = 'message: ' + str(message)
                print(dttm(),state + ': ' + log_message)
                logger.info(log_message)
    except Exception as e:
        print(str(e))