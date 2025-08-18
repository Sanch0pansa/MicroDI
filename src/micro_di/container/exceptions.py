class DIError(Exception):
    pass


class DIResolutionError(DIError):
    pass


class UnresolvableDependencyError(DIResolutionError):
    def __init__(self, target_type: type):
        self.__target_type = target_type
        super().__init__(f"Cannot resolve dependencies for: {self.__target_type.__name__}")


class NoInjectableDependenciesError(DIResolutionError):
    def __init__(self, target_type: type):
        self.__target_type = target_type
        super().__init__(
            f"No injectable dependencies found for: {self.__target_type.__name__}. "
            f"If the class has no dependencies, provide an instance explicitly."
        )
