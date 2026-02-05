from abc import abstractmethod, ABC
from typing import Optional


class ExceptionProtocol(Exception, ABC):
    base_msg: str

    def __init__(self, msg: Optional[str] = None, *args):
        self.msg = self.base_msg.format(e=msg or "")
        super().__init__(*args)

    def __str__(self):
        return self.msg

    @property
    @abstractmethod
    def base_msg(self) -> str:
        return self.base_msg
