from src.micro_di import DIContainer


class Abstract:
    pass


class Concrete(Abstract):
    pass


def test_instance_registration(di: DIContainer) -> None:
    instance = Concrete()
    di.register_instance(Abstract, instance)

    res = di.resolve(Abstract)
    assert res is instance
