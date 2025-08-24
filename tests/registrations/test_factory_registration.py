from src.micro_di import DIContainer, Injectable
from typing import Annotated


class Abstract:
    pass


class Dependency:
    pass

class Concrete(Abstract):
    dependency: Annotated[Dependency, Injectable]

    def __init__(self, a: str):
        super().__init__()
        self.a = a


def test_factory_registration(di: DIContainer) -> None:
    di.register_factory(Abstract, Concrete, a="hello")

    res = di.resolve(Abstract)
    assert isinstance(res, Concrete)
    assert res.a == "hello"
    assert isinstance(res.dependency, Dependency)
