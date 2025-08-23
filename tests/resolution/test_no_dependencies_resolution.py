from src.micro_di import DIContainer, Injectable, NoInjectableDependenciesError, UnresolvableDependencyError, DIResolutionError
from typing import Annotated
import pytest


class Dependency:
    pass


class ClassWithDependencies:
    dependency: Annotated[Dependency, Injectable]


class ClassWithoutDependencies:
    pass


def test_resolving_class_without_dependencies(di: DIContainer) -> None:
    with pytest.raises(NoInjectableDependenciesError):
        di.resolve(ClassWithoutDependencies)


def test_resolving_chain_with_class_without_dependencies(di: DIContainer) -> None:
    try:
        di.resolve(ClassWithDependencies)
    except DIResolutionError as e:
        assert e.__class__ is UnresolvableDependencyError
        assert e.__cause__.__class__ is NoInjectableDependenciesError