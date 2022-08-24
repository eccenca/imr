"""Testing utilities."""
import os
from typing import Optional

import pytest
import requests


# check for cmem environment and skip if not present
from cmem.cmempy.api import get_token

from cmem_plugin_base.dataintegration.context import (
    PluginContext,
    UserContext,
    TaskContext,
    ExecutionContext,
    ReportContext
)

needs_cmem = pytest.mark.skipif(
    len(os.environ.get('CMEM_BASE_URI', '')) == 0, reason="Needs CMEM configuration"
)


class TestUserContext(UserContext):
    """dummy user context that can be used in tests"""

    __test__ = False

    def __init__(self):
        # get access token from default service account
        try:
            access_token: str = get_token()["access_token"]
        except requests.exceptions.RequestException:
            access_token: str = ''
        self.token = lambda: access_token


class TestPluginContext(PluginContext):
    """dummy plugin context that can be used in tests"""

    __test__ = False

    def __init__(self, project_id: str = "dummyProject",
                 user: Optional[UserContext] = TestUserContext()):
        self.project_id = project_id
        self.user = user

class TestTaskContext(TaskContext):
    """dummy Task context that can be used in tests"""

    __test__ = False

    def __init__(self, project_id: str = 'dummyProject'):
        self.project_id = lambda: project_id


class TestExecutionContext(ExecutionContext):
    """dummy execution context that can be used in tests"""

    __test__ = False

    def __init__(self, project_id: str = "dummyProject",
                 user: Optional[UserContext] = TestUserContext()):
        self.report = ReportContext()
        self.task = TestTaskContext(project_id=project_id)
        self.user = user
