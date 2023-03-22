"""
To use the client fixture we created in webapp __init__.py, 
we need to import it. PyCharm will claim that the import is unused, but pytest actually needs it. 
"""
from uwconnect_core.test.unit.webapp import client
# https://codethechange.stanford.edu/guides/guide_flask_unit_testing.html
# https://flask.palletsprojects.com/en/2.2.x/testing/

# Need not to run `server.py`
# Directly run `python -m pytest`
# Directly run `python -m pytest -v -s --disable-warnings`

"""
def test_demo(client):
    #=======================
    # Some usage
    #=======================
    #landing = client.get("/")
    #html = landing.data.decode()
    #print(html)
    # Check that links to `about` and `login` pages exist
    #assert "<a href=\"/about/\">About</a>" in html
    #assert " <a href=\"/home/\">Login</a>" in html

    # Spot check important text
    #assert "At CultureMesh, we're building networks to match these " \
    #       "real-world dynamics and knit the diverse fabrics of our world " \
    #       "together." in html
    #assert "1. Join a network you belong to." in html

    # check that the request was successful (indicated by a response code of 200)
    # assert landing.status_code == 200
    pass
"""