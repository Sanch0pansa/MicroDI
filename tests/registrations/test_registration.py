from src.micro_di import DIContainer, Injectable
from typing import Annotated


class Dependency:
    pass


class Abstract:
    pass


class Concrete(Abstract):

    dependency: Annotated[Dependency, Injectable]

    pass


def test_concrete_type_registration(di: DIContainer) -> None:
    di.register_instance(Dependency, Dependency())
    di.register(Abstract, Concrete)

    res = di.resolve(Abstract)
    assert isinstance(res, Concrete)
