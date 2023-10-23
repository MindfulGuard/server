from mindfulguard.core.response_status_codes import OK
from mindfulguard.database.postgresql.settings import Settings

import pytest

@pytest.mark.asyncio
async def test_get_settings():
    settings = await Settings().get()
    settings_OK = settings[1]
    
    assert settings_OK == OK