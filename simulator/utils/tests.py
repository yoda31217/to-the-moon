import pytest


def approximately(number: float):
    return pytest.approx(number)  # pyright: ignore [reportUnknownMemberType]
