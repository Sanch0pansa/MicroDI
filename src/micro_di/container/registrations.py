from typing import Generic
from .types import T


class DIRegistration(Generic[T]):
    __concrete_type: type[T]
    __dependencies: dict[str, type]
    __instance: T | None

    def __init__(self, concrete_type: type[T], instance: T | None = None) -> None:
        self.__concrete_type = concrete_type
        self.__instance = instance
        self.__dependencies = {}

    @property
    def is_resolved(self) -> bool:
        return self.__instance is not None

    @property
    def instance(self) -> T | None:
        return self.__instance

    @property
    def concrete_type(self) -> type[T]:
        return self.__concrete_type

    @property
    def dependencies(self) -> dict[str, type]:
        return self.__dependencies

    def set_instance(self, instance: T) -> None:
        self.__instance = instance

    def set_dependencies(self, dependencies: dict[str, Any]) -> None:
        self.__dependencies = dependencies