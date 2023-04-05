"""
Пакет avm реализует работу с api antivirus multiscaner.

ivi
# License: BSD
"""

#описание пакета;
#список модулей и пакетов, экспортируемых этим модулем;
#автор;
#контактные данные;
#лицензия.

__author__ = 'ivi'
__all__ = ["client", "resp"]
from .client import AVMScaner
from .resp import AVMSResponce, AVMSSummaryReport, AVMSFullReport, AVMSProcessingError

