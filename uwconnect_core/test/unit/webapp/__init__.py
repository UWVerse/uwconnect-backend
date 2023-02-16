from uwconnect_core.main import create_app
import pytest

"""Initialize the testing environment

Creates an app for testing that has the configuration flag ``TESTING`` set to``True``.

"""

# The @pytest.fixture annotation tells pytest that the following function creates (using the yield command) an app for testing.
@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """
    app = create_app()
    #app.config['TESTING'] = True
    client = app.test_client()

    yield client