from src.micro_di import DIContainer


class Abstract:
    pass


class Concrete(Abstract):
    def __init__(self, a: str):
        super().__init__()
        self.a = a


def test_factory_registration(di: DIContainer) -> None:
    di.register_factory(Abstract, Concrete, a="hello")

    res = di.resolve(Abstract)
    assert isinstance(res, Concrete)
    assert res.a == "hello"
