import pytest
import tempfile

@pytest.fixture(autouse=True)
def temp_media(settings):
    with tempfile.TemporaryDirectory() as tmp:
        settings.MEDIA_ROOT = tmp
        yield