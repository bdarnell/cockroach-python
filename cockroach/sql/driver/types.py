import datetime
import time

try:
    import enum
except ImportError:
    import enum34 as enum


from .wire_pb2 import Datum


class Binary(object):
    def __init__(self, v):
        self.v = v


def Date(y, m, d):
    return datetime.date(y, m, d)


def Time(h, m, s):
    return datetime.time(h, m, s)


def Timestamp(y, mo, d, h, mi, s):
    return datetime.datetime(y, mo, d, h, mi, s)


# Implementations of the FromTicks methods are copied from PEP 249.
def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])


class TypeCode(enum.Enum):
    STRING = 1
    BINARY = 2
    NUMBER = 3
    DATETIME = 4
    ROWID = 5

for k, v in TypeCode.__members__.items():
    globals()[k] = v


def _python_to_datum(val):
    if val is None:
        return Datum()
    elif isinstance(val, str):
        return Datum(string_val=val)
    elif isinstance(val, bool):
        # Note that bool is a subtype of int, so order matters.
        return Datum(bool_val=val)
    elif isinstance(val, int):
        return Datum(int_val=val)
    elif isinstance(val, float):
        return Datum(float_val=val)
    elif isinstance(val, datetime.datetime):
        ts = val.timestamp()
        return Datum(time_val=Datum.Timestamp(
            sec=int(ts),
            nsec=int((ts % 1) * 1e9),
        ))
    else:
        raise TypeError("unsupported type %s" % type(val))


def _datum_to_python(datum):
    which = datum.WhichOneof("payload")
    if which is None:
        return None
    elif which == "string_val":
        return datum.string_val
    elif which == "int_val":
        return datum.int_val
    elif which == "float_val":
        return datum.float_val
    elif which == "bool_val":
        return datum.bool_val
    elif which == "time_val":
        return datetime.datetime.fromtimestamp(
            datum.time_val.sec + datum.time_val.nsec / 1e9)
    else:
        raise TypeError("unsupported type %s" % which)

__all__ = ['Binary', 'Date', 'Time', 'Timestamp', 'DateFromTicks', 'TimeFromTicks',
           'TimestampFromTicks', 'STRING', 'BINARY', 'NUMBER', 'DATETIME', 'ROWID']
