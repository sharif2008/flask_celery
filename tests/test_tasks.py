import json
from unittest.mock import patch, call

from galileo_task import long_task


def test_task():
    assert long_task.run()
    assert long_task.run()
