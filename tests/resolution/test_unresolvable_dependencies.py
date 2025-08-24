from src.micro_di import DIContainer, Injectable, UnresolvableDependencyError, DIResolutionError
from typing import Annotated
import pytest


class Dependency:
    pass


class UnresolvableDependency:
    def __init__(self, a: int):
        pass


class UnresolvableClass:
    dependency: Annotated[Dependency, Injectable]
    
    def __init__(self, a: int):
        pass


def test_resolving_class_with_resolvable_dependency(di: DIContainer) -> None:
    with pytest.raises(UnresolvableDependencyError):
        di.resolve(UnresolvableDependency)


def test_resolving_class_with_unresolvable_dependency(di: DIContainer) -> None:
    try:
        di.resolve(UnresolvableClass)
    except DIResolutionError as e:
        assert e.__class__ is UnresolvableDependencyError
        assert e.__cause__.__class__ is TypeError