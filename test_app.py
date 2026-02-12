import pytest
from dash.testing.application_runners import import_app
import time

def test_header_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1", timeout=10)
    assert "Pink Morsels Sales Dashboard" in dash_duo.find_element("h1").text

def test_graph_exists(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    assert dash_duo.find_element("#sales-line-chart") is not None

def test_region_radio_exists(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-radio", timeout=10)
    radios = dash_duo.find_elements("#region-radio input[type='radio']")
    assert len(radios) == 5

def test_region_selection_updates_chart(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    
    # Trigger update
    dash_duo.find_element("input[value='north']").click()
    time.sleep(1) 
    
    # Confirm graph remains valid after callback
    assert dash_duo.find_element("#sales-line-chart") is not None