from json import JSONEncoder
from typing import Any


class DefaultEncoder(JSONEncoder):
    def default(self, obj) -> Any:
        if hasattr(obj, '__dict__'):
            return obj.__dict__()
        return super().default(obj)