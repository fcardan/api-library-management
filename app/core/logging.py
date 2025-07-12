# app/core/advanced_logger.py
import sys
import time
import functools
import inspect
from datetime import datetime
from typing import Optional, Callable, Any, Dict, Type
import inspect
from fastapi import HTTPException
from enum import Enum

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    # Fallback para ambientes sem colorama
    class Fore: RED = YELLOW = GREEN = CYAN = MAGENTA = BLUE = WHITE = ''
    class Back: BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ''
    class Style: RESET_ALL = BRIGHT = DIM = NORMAL = ''

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class AlertType(Enum):
    SUCCESS = ("✔", Fore.GREEN)
    INFO = ("ℹ", Fore.CYAN)
    WARNING = ("⚠", Fore.YELLOW)
    ERROR = ("✖", Fore.RED)
    CUSTOM = ("◈", Fore.WHITE)

class BaseAPIException(Exception):
    """Classe base para todas as exceções da API"""
    
    status_code: int = 500
    detail: str = "Erro interno do servidor"
    internal_message: Optional[str] = None
    headers: Optional[Dict[str, Any]] = None
    
    def __init__(
        self,
        detail: Optional[str] = None,
        internal_message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.detail = detail or self.detail
        self.internal_message = internal_message or self.detail
        self.headers = headers
        super().__init__(self.detail)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.detail}"

# ======================
# Hierarquia de Exceções
# ======================
class UnauthorizedException(BaseAPIException):
    status_code = 401
    detail = "Credenciais inválidas"

class ForbiddenException(BaseAPIException):
    status_code = 403
    detail = "Acesso negado"

class BadRequestException(BaseAPIException):
    status_code = 400
    detail = "Requisição inválida"

class NotFoundException(BaseAPIException):
    status_code = 404
    detail = "Recurso não encontrado"

class ConflictException(BaseAPIException):
    status_code = 409
    detail = "Conflito de recursos"

class ValidationException(BadRequestException):
    detail = "Erro de validação nos dados"

class DatabaseException(BaseAPIException):
    detail = "Erro no banco de dados"

class ServiceUnavailableException(BaseAPIException):
    status_code = 503
    detail = "Serviço temporariamente indisponível"

# Exceções específicas do domínio
class BookNotFoundException(NotFoundException):
    detail = "Livro não encontrado"

class AuthorNotFoundException(NotFoundException):
    detail = "Autor não encontrado"

class UserNotFoundException(NotFoundException):
    detail = "Usuário não encontrado"

class BookUnavailableException(ConflictException):
    detail = "Livro não disponível para empréstimo"

class AdvancedLogger:
    def __init__(self, 
                 log_level: LogLevel = LogLevel.INFO,
                 show_timestamp: bool = True,
                 show_caller: bool = False,
                 log_file: Optional[str] = None):
        self.log_level = log_level
        self.show_timestamp = show_timestamp
        self.show_caller = show_caller
        self.log_file = log_file
        self._alert_palette = {
            AlertType.SUCCESS: ("SUCCESS", '🟢'),
            AlertType.INFO: ("INFO", '🔵'),
            AlertType.WARNING: ("WARNING", '🟡'),
            AlertType.ERROR: ("ERROR", '🔴')
        }
        self.exception_map = {
            # Mapeamento de exceções para níveis de log
            UnauthorizedException: LogLevel.WARNING,
            ForbiddenException: LogLevel.WARNING,
            BadRequestException: LogLevel.INFO,
            NotFoundException: LogLevel.INFO,
            ConflictException: LogLevel.WARNING,
            DatabaseException: LogLevel.ERROR,
            ServiceUnavailableException: LogLevel.CRITICAL
        }
        
    def _get_caller_info(self) -> str:
        frame = inspect.currentframe().f_back.f_back
        return f"{frame.f_code.co_filename}:{frame.f_lineno}" if frame else ""

    def _write_log(self, message: str, level: LogLevel, color: str, icon: str):
        timestamp = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " if self.show_timestamp else ""
        caller = f" ({self._get_caller_info()})" if self.show_caller else ""
        log_line = f"{color}{icon} {timestamp}{message}{caller}{Style.RESET_ALL}"
        
        print(log_line)
        
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"{icon} {timestamp}{message}{caller}\n")

    def log(self, level: LogLevel, message: str):
        if level.value < self.log_level.value:
            return
        
        colors = {
            LogLevel.DEBUG: Fore.CYAN,
            LogLevel.INFO: Fore.BLUE,
            LogLevel.WARNING: Fore.YELLOW,
            LogLevel.ERROR: Fore.RED,
            LogLevel.CRITICAL: Fore.WHITE + Back.RED
        }
        
        icons = {
            LogLevel.DEBUG: '🐞',
            LogLevel.INFO: 'ℹ',
            LogLevel.WARNING: '⚠',
            LogLevel.ERROR: '❌',
            LogLevel.CRITICAL: '🔥'
        }
        
        self._write_log(message, level, colors[level], icons[level])

    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)

    def info(self, message: str):
        self.log(LogLevel.INFO, message)

    def warning(self, message: str):
        self.log(LogLevel.WARNING, message)

    def error(self, message: str):
        self.log(LogLevel.ERROR, message)

    def critical(self, message: str):
        self.log(LogLevel.CRITICAL, message)

    def log_exception(self, exc: BaseAPIException):
        """Registra exceções de forma estruturada com base em seu tipo"""
        log_level = self.exception_map.get(type(exc), LogLevel.ERROR)
        message = f"{type(exc).__name__}: {exc.internal_message or exc.detail}"
        self.log(log_level, message)

    def alert(self, 
              message: str, 
              alert_type: AlertType = AlertType.CUSTOM,
              border_char: str = '═',
              border_length: int = 30):
                
        title, icon = self._alert_palette.get(alert_type, ("CUSTOM", '◈'))
        color = alert_type.value[1]
        
        message_body = f"{color}{icon} {title.upper()}{Style.RESET_ALL}: {message}"
        
        border_length = len(message_body) - 7
        border = border_char * border_length

        print(f"\n{border}\n{message_body}\n{border}\n")    
        
    def interactive_input(self, 
                          prompt: str, 
                          validation: Optional[Callable[[str], bool]] = None,
                          error_message: str = "Entrada inválida. Tente novamente.") -> str:
        while True:
            self.info(f"{prompt} ➤ ")
            user_input = input().strip()
            
            if not validation or validation(user_input):
                return user_input
            self.error(f"{error_message}")

# Funções de conveniência
logger = AdvancedLogger()

def success(message: str):
    logger.alert(message, AlertType.SUCCESS)

def info_alert(message: str):
    logger.alert(message, AlertType.INFO)

def warning_alert(message: str):
    logger.alert(message, AlertType.WARNING)

def error_alert(message: str):
    logger.alert(message, AlertType.ERROR)

def interactive_input(prompt: str, validation: Optional[Callable[[str], bool]] = None, 
                    error_message: str = "Entrada inválida. Tente novamente.") -> str:
    return logger.interactive_input(prompt, validation, error_message)