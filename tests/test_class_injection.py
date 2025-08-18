import pytest
from typing import Annotated


class A:
    attribute_1: str
    attribute_2: str


class B:
    attribute_1: A
    attribute_2: str