from unittest.mock import MagicMock

from lightning_data.processing import utilities as utilities_module
from lightning_data.processing.utilities import optimize_dns_context


def test_optimize_dns_context(monkeypatch):
    popen_mock = MagicMock()

    monkeypatch.setattr(utilities_module, "_IS_IN_STUDIO", True)
    monkeypatch.setattr(utilities_module, "Popen", popen_mock)

    class FakeFile:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args, **kwargs):
            return self

        def readlines(self):
            return ["127.0.0.53"]

    monkeypatch.setitem(__builtins__, "open", MagicMock(return_value=FakeFile()))

    with optimize_dns_context(True):
        pass

    cmd = popen_mock._mock_call_args_list[0].args[0]
    expected_cmd = (
        "sudo /home/zeus/miniconda3/envs/cloudspace/bin/python"
        " -c 'from lightning_data.processing.utilities import _optimize_dns; _optimize_dns(True)'"
    )
    assert cmd == expected_cmd
