import os
import pytest
import requests
from app import app
from flask import url_for


@pytest.fixture
def client():
    app.config['TESTING'] = True 
    app.config['SERVER_NAME'] = 'TEST'
    client = app.test_client()
    with app.app_context():
        pass 
    app.app_context().push()
    yield client

def test_Login(client):
    response = client.get('/login')
    assert 200 == response.status_code
    assert b'Sign in' in response.data
   
def test_AddFeed(client):
    response = client.get('/add_feed')
    assert 200 == response.status_code
    assert b'Impossible' in response.data

def test_AllFeed(client):
    response = client.get('/feed/all_feed')
    assert 200 == response.status_code
    assert b'Impossible' in response.data

def test_Home(client):
    response = client.get('/signup')
    assert 200 == response.status_code
    assert b'login' in response.data

def test_logOut(client):
    response = client.get('/logout')
    assert 200 == response.status_code
    assert b'Home' in response.data