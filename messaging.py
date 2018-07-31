import tenacity
import logging
import configparser

from praw.exceptions import APIException, ClientException
from prawcore.exceptions import RequestException, ResponseException, ServerError
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout

import logger
import util

RECOVERABLE_EXCEPTIONS = (APIException,
                          ClientException,
                          ConnectionError,
                          HTTPError,
                          ReadTimeout,
                          RequestException,
                          ResponseException,
                          ServerError)

RETRY_PARAMS = {'wait':tenacity.wait_fixed(5),
                'retry':tenacity.retry_if_exception_type(RECOVERABLE_EXCEPTIONS),
                'after':tenacity.after_log(logger.get_logger(logger.MSG_LOGGER), logging.WARNING),
                'reraise':True}

RETRY_PARAMS_SHORT = {'wait':tenacity.wait_fixed(1),
                'retry':tenacity.retry_if_exception_type(RECOVERABLE_EXCEPTIONS),
                'after':tenacity.after_log(logger.get_logger(logger.MSG_LOGGER), logging.WARNING),
                'reraise':True}

@tenacity.retry(**RETRY_PARAMS)
def process(r, message):
    if message.author.name in admins():
        admin_commands()
    else:
        forward(r, message, admins())

@tenacity.retry(**RETRY_PARAMS_SHORT)
def scan_inbox(r):
    unread = r.inbox.unread()
    for new in unread:
        process(r, new)
        new.mark_read()

def send_message(r, header, body, user=None, users=None):
    if user is not None and users is not None:
        raise ValueError("send_message takes only either a user argument or a users argument")
    if user is None and users is None:
        raise ValueError("send_message expects user argument")

    @tenacity.retry(**RETRY_PARAMS)
    def try_send(r, header, body, user):
        r.redditor(user).message(header, body)

    if user:
        try_send(r, header, body, user)
    if users:
        for u in users:
            try_send(r, header, body, u)

def forward(r, message, recipients):
    altered_header = message.author + " sent:- " + message.subject
    send_message(r, altered_header, message.body, users=recipients)

def read_ini():
    cfg = configparser.ConfigParser()
    cfg.read(util.relative_file_path(__file__, 'privileges.ini'))
    return cfg

def admin_commands():
    pass

def admins():
    return read_ini()['privileges']['admin'].split(',')

