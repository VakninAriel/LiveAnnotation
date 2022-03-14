import inspect
from typing import Tuple, Union, List, Callable, Any, TypeVar
from functools import wraps

# Please keep __all__ alphabetized within each category.
__all__ = [
    # decorator
    'check_params',

    # contracts
    'Float',
    'Integer',
    'LegalRange',
    'LegalRangeInteger',
    'LegalRangeFloat',
    'LegalString',
    'Negative',
    'Positive',
    'String',
    'NoneEmpty',


    # core
    'Contract',
    'Typed'

]


# core
class Contract:
    @classmethod
    def check(cls, method: str, name: str,  value: Any) -> None:
        pass


class Typed(Contract):
    type: Any = None

    @classmethod
    def check(cls, method: str, name: str, value: Any) -> None:
        assert isinstance(value, cls.type),\
                f'[{method}]: Expected {name} to be of type { cls.type}. instead got {value}  of type {type(value)}'
        super().check(method, name, value)


# basic types
class Integer(int, Typed ):
    type = int


class Float(float, Typed):
    type = float


class String(str, Typed):
    type = str


class Positive(Contract):
    @classmethod
    def check(cls, method: str, name: str, value: Any) -> None:
        assert value > 0, f'[{method}]: Expected {name} to be Positive. but got {value}'
        super().check(method, name, value)


class Negative(Contract):
    @classmethod
    def check(cls,  method: str, name: str, value: Any) -> None:
        assert value < 0, f'[{method}]: Expected {name} to be Negative. but got {value}'
        super().check(method, name, value)


class NoneEmpty(Contract):
    @classmethod
    def check(cls,  method: str, name: str, value: Any) -> None:
        assert len(value) > 0, f'[{method}]: Expected {name} to be non- empty value'
        super().check(method, name, value)


class LegalString(String):
    _all_slots: List[str] = []
    _string_name: str = 'none'

    def __init__(self, all_slots: List[str]):
        self._all_slots = all_slots
        super().__init__()

    @classmethod
    def check(cls, method: str, name: str, value: Any) -> None:
        assert value in cls._all_slots, f"[{method}]:  '{value}' is not part of legal {cls._string_name}"
        super().check(method, name, value)


class PositiveInteger(Integer, Positive):
    pass


class LegalRange(Contract):
    _range: List[Union[float, int]] = [0, 0]
    _string_name: str = ''

    @classmethod
    def check(cls, method: str, name: str, value: Any) -> None:
        assert cls._range[0] <= value <= cls._range[1], \
            f"[{method}]:  '{value}' is not in  legal {cls._string_name} range of {cls._range}"
        super().check(method, name, value)


class LegalRangeFloat(Float, LegalRange):
    pass


class LegalRangeInteger(Integer, LegalRange):
    pass


TFun = TypeVar('TFun', bound=Callable[..., Any])


# decorator
def check_params(f: TFun) -> Any:
    signature = inspect.signature(f)

    @wraps(f)
    def wrapper(*args, **kwargs) -> Any:
        bound_arguments = signature.bind(*args, **kwargs)
        for name, value in bound_arguments.arguments.items():
            annotation = signature.parameters[name].annotation
            if annotation is inspect.Signature.empty:
                continue
            annotation.check(f.__name__, name, value)
        return f(*args, **kwargs)

    return wrapper


def check_features(feature: str) :
    def decorator(f: TFun):
        def wrapper(*args, **kwargs):
           assert feature in f.__name__.features, f''

        return wrapper
    return decorator
