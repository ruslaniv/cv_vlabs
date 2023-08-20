import platform
from functools import lru_cache
from typing import NamedTuple

import torch


class ComputeDevice(NamedTuple):
    device: str
    device_name: str


def get_compute_device() -> ComputeDevice:
    """Получение информации об устройстве для векторизации.

    Returns
    -------
    ComputeDevice: namedtuple
        Информация об устройстве для векторизации.
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"
    device_name = platform.processor()
    if device == "cuda":
        device_name = torch.cuda.get_device_name()
    return ComputeDevice(device=device, device_name=device_name)
