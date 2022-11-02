# run pytest .\tests\app_tests.py
import urllib.request
from src.config import PROJECT_PATH
from os.path import exists

def test_acc_data():
    file_exists = exists(f'{PROJECT_PATH}/src/acc_data.csv')
    assert file_exists == True # check if file for the acc price for each account exists

def test_dashboard_up():
    request_code = urllib.request.urlopen("http://localhost:8501").getcode()
    assert request_code == 200 # check if dashboard webapp is up