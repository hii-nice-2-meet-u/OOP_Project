from datetime import datetime
from enum import Enum

class LogType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    TRANSACTION = "TRANSACTION"

class Log:
    """Base class for all logs."""
    def __init__(self, log_id: str, level: LogType, message: str):
        self.__log_id = log_id
        self.__timestamp = datetime.now()
        self.__level = level
        self.__message = message

    def get_log_entry(self) -> str:
        return f"[{self.__timestamp}] [{self.__level.value}] ID:{self.__log_id} - {self.__message}"

class SystemLog(Log):
    """Logs for system events (e.g., server start, errors)."""
    def __init__(self, log_id: str, level: LogType, message: str, module_name: str):
        super().__init__(log_id, level, message)
        self.__module_name = module_name

    def get_log_entry(self) -> str:
        # Override to include module name
        return f"{super().get_log_entry()} [Module: {self.__module_name}]"

class FinancialLog(Log):
    """Logs for monetary transactions."""
    def __init__(self, log_id: str, amount: float, transaction_type: str, performed_by: str):
        message = f"Transaction: {transaction_type} Amount: {amount} by {performed_by}"
        super().__init__(log_id, LogType.TRANSACTION, message)
        self.__amount = amount
        self.__performed_by = performed_by

class AuditLog(Log):
    """Logs for user actions (e.g., Staff modifying an order)."""
    def __init__(self, log_id: str, action: str, user_id: str, target_id: str):
        message = f"User {user_id} performed {action} on {target_id}"
        super().__init__(log_id, LogType.INFO, message)
        self.__user_id = user_id
        self.__action = action

class LogManager:
    """Singleton-like manager to store logs in memory (or db)."""
    def __init__(self):
        self.__logs = []

    def add_log(self, log: Log):
        self.__logs.append(log)
        # In a real system, this would write to a file or database
        print(f"LOG RECORDED: {log.get_log_entry()}")