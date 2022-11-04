# run pytest .\tests\app_tests.py
import requests
from src.config import PROJECT_PATH
from os.path import exists

def test_acc_data():
    file_exists = exists(f'{PROJECT_PATH}/app/acc_data.csv')
    assert file_exists == True # check if file for the acc price for each account exists

def test_online_dashboard_up():
    response = requests.get('https://ramtrading.streamlitapp.com')
    assert response.status_code == 200 # check if dashboard webapp is up on streamlit domain

def test_local_dashboard_up():
    response = requests.get('http://localhost:8501')
    assert response.status_code == 200 # check if dashboard webapp is up locally