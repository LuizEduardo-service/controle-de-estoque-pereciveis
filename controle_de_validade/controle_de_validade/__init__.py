__version__ = '0.1.0'

import datetime as dt
import locale
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR')
except:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')

data = dt.datetime.now().date()
mes = dt.datetime.strftime(data,'%B')
print(mes.upper())