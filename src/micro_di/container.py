from collections.abc import Callable
from dataclasses import dataclass
from inspect import isabstract
from typing import Annotated, Any, Generic, get_args, get_origin

from .exceptions import (
    DIResolutionError,
    NoRegisteredImplementationsError,
    UnresolvableDependencyError,
)
from .injectable import Injectable
from .registrations import DIRegistration
from .types import P, T


@dataclass
class DIFactory(Generic[P, T]):
    constructor: Callable[P, T]
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


class DIContainer:
    def __init__(self) -> None:
        self.__registrations: dict[type, DIRegistration] = {}
        self.__factories: dict[type, DIFactory] = {}
        
    def __create_registration(
        self,
        abstract_type: type,
        concrete_type: type[T],
        instance: T | None = None,
    ) -> None:
        self.__registrations[abstract_type] = DIRegistration(concrete_type=concrete_type, instance=instance)

    def register_instance(self, abstract_type: type, instance: T) -> None:
        self.__create_registration(abstract_type, abstract_type, instance)

    def register(self, abstract_type: type, concrete_type: type[T]) -> None:
        self.__create_registration(abstract_type, concrete_type)

    def register_factory(
        self,
        abstract_type: type,
        constructor: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        self.__factories[abstract_type] = DIFactory(constructor=constructor, args=args, kwargs=kwargs)
        self.__create_registration(abstract_type, abstract_type)

    def __get_injectable_attributes(self, cls: type) -> dict[str, Any]:
        attributes: dict[str, Any] = {}
        type_hints = getattr(cls, "__annotations__", {})
        for name, annotation in type_hints.items():
            origin = get_origin(annotation)
            args = get_args(annotation)
            if origin is Annotated and len(args) > 1:
                marker = args[1]
                if marker is Injectable:
                    attributes[name] = args[0]
    
        return attributes

    def __create_instance(self, concrete_type: type[T]) -> T:
        if concrete_type in self.__factories:
            factory = self.__factories[concrete_type]
            return factory.constructor(*factory.args, **factory.kwargs)


        print(concrete_type, isabstract(concrete_type))
        if isabstract(concrete_type):
            raise NoRegisteredImplementationsError(concrete_type)

        try:
            return concrete_type()
        except TypeError as e:
            raise UnresolvableDependencyError(concrete_type) from e
    
    def __define_registration_dependencies(
        self,
        registration: DIRegistration,
    ) -> None:
        injectable_attrs = self.__get_injectable_attributes(registration.concrete_type)
        registration.set_dependencies(injectable_attrs)
    
    def __resolve_dependencies_for_registration(
        self,
        registration: DIRegistration,
        instance: T,
    ) -> None:
        try:
            for attr_name, dep_type in registration.dependencies.items():
                setattr(instance, attr_name, self.resolve(dep_type))
        except DIResolutionError as e:
            raise UnresolvableDependencyError(registration.concrete_type) from e

    def resolve(self, abstract_type: type[T]) -> T:
        if abstract_type not in self.__registrations:
            self.register(abstract_type, abstract_type)

        registration = self.__registrations[abstract_type]
        if registration.instance is not None:
            return registration.instance

        self.__define_registration_dependencies(registration)
        instance = self.__create_instance(registration.concrete_type)
        self.__resolve_dependencies_for_registration(registration, instance)

        registration.set_instance(instance)

        return instance

    @property
    def registrations(self) -> dict[type, DIRegistration]:
        return self.__registrations
