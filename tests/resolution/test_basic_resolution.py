from src.micro_di import DIContainer, Injectable, UnresolvableDependencyError
from typing import Annotated
import pytest


class IRepo:
    pass


class Repo(IRepo):
    def __init__(self, database_url: str):
        super().__init__()
        self.database_url = database_url
    

class Service:
    repo: Annotated[IRepo, Injectable]


class IController:
    pass


class EventConsumer:
    def __init__(self, queue: str):
        self.queue = queue


class APIRouter:
    def __init__(self, base_url: str):
        self.base_url = base_url


class MQController(IController):
    service: Annotated[Service, Injectable]
    event_consumer: Annotated[EventConsumer, Injectable]


class RESTController(IController):
    service: Annotated[Service, Injectable]
    api_router: Annotated[APIRouter, Injectable]


class App:
    controller: Annotated[IController, Injectable]



def test_unresolvable_app(di: DIContainer) -> None:
    with pytest.raises(UnresolvableDependencyError):
        di.resolve(App)


def test_resolvable_app(di: DIContainer) -> None:
    repo = Repo("database")
    event_consumer = EventConsumer("queue")
    di.register_instance(IRepo, repo)
    di.register_instance(EventConsumer, event_consumer)
    di.register(IController, MQController)

    app = di.resolve(App)
    assert isinstance(app.controller, MQController)
    assert app.controller.event_consumer is event_consumer
    assert app.controller.service.repo is repo
