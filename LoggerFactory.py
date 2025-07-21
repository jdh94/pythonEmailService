# -*- coding: utf-8 -*-

import logging
import logging.handlers
import datetime


def loggerFactory():
    # what is this code doing? expecailly the parameter of getLogger
    # getLogger는 로거 객체를 가져오는 메서드입니다. 인자로 전달된 문자열은 로거의 이름을 지정합니다.
    logger = logging.getLogger('bbumbbai')

    # Check handler exists
    if len(logger.handlers) > 0:
        return logger  # Logger already exists

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        u'[%(asctime)s] [%(levelname)s|%(name)s] [%(filename)s||%(funcName)s||%(lineno)d] :: %(message)s')

    # StreamHandler
    # how does it work?
    # StreamHandler는 로그 메시지를 콘솔에 출력하는 핸들러입니다.
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.DEBUG)

    # what is this code doing?
    # TimedRotatingFileHandler는 로그 파일을 매일 자정에 회전시키는 핸들러입니다.
    # when='midnight'는 자정에 회전하도록 설정하는 것입니다.
    # interval=1은 1일마다 회전하도록 설정하는 것입니다.
    # encoding='utf-8'은 로그 파일의 인코딩을 UTF-8로 설정하는 것입니다.
    # what is the difference between sh and fh?
    # sh는 콘솔에 로그를 출력하는 핸들러이고, fh는 파일에 로그를 저장하는 핸들러입니다.
    fh = logging.handlers.TimedRotatingFileHandler(
        filename='./logs/sendEmail.log',
        when='midnight',
        interval=1,
        encoding='utf-8'
    )
    fh.suffix = "%Y-%m-%d"
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)

    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger
