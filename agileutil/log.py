#coding=utf-8

import sys
try:
    from imp import reload
except:
    pass
reload(sys)
try:
    sys.setdefaultencoding('utf-8')
except:
    pass

import logging
from logging.handlers import WatchedFileHandler


class Log:

    __slots__ = [
        '__path', '__switch', '__fileHandler', '__logger', '_errorCallBack',
        '_warningCallBack', '_isOutput'
    ]

    __logList = {}
    __fmt = '%(asctime)s-%(filename)s-%(process)d-%(thread)d-%(funcName)s-[line:%(lineno)d]-%(levelname)s-%(message)s'
    #__fmt = '[%(levelname)s] [%(threadName)s] [%(process)d] %(asctime)s [line:%(lineno)d] %(message)s'
    __level = logging.DEBUG

    def __init__(self, path):
        self.__path = path
        self.__switch = True
        fmter = logging.Formatter(Log.__fmt)
        self.__fileHandler = WatchedFileHandler(self.__path)
        self.__fileHandler.setFormatter(fmter)
        self.__logger = logging.getLogger(path)
        self.__logger.addHandler(self.__fileHandler)
        self.__logger.setLevel(Log.__level)
        self._errorCallBack = None
        self._warningCallBack = None
        self._isOutput = False

    def setOutput(self, tag):
        self._isOutput = tag

    def getOutput(self):
        return self._isOutput

    def setSwitch(self, switch):
        self.__switch = switch

    def getSwitch(self):
        return self.__switch

    def getPath(self):
        return self.__path

    def debug(self, loginfo):
        if self.__switch: self.__logger.debug(loginfo)
        if self._isOutput: print(logInfo)

    def info(self, logInfo):
        if self.__switch: self.__logger.info(logInfo)
        if self._isOutput: print(logInfo)

    def warning(self, logInfo):
        if self.__switch: self.__logger.warning(logInfo)
        if self._isOutput: print(logInfo)
        try:
            if self._warningCallBack: self._warningCallBack(logInfo)
        except:
            pass

    def error(self, logInfo):
        if self.__switch: self.__logger.error(logInfo)
        if self._isOutput: print(logInfo)
        try:
            if self._errorCallBack: self._errorCallBack(logInfo)
        except:
            pass

    def setErrorCallBack(self, func):
        self._errorCallBack = func

    def setWarningCallBack(self, func):
        self._warningCallBack = func
