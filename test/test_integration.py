import os
import pytest
import requests
from app import app
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'test'
    client = app.test_client()
    with app.app_context():
        pass
    app.app_context().push()
    yield client
#test de nos listes dino dans les pages respectives
def test_dino(client):
    response = client.get('/')
    assert 200 == response.status_code
    
def test_some_dino(client):
    res = client.get("/dinosaur/velociraptor")
    assert res.status_code == 200
    assert b"velociraptor" in res.data
    assert b"https://allosaurus.delahayeyourself.info/static/img/dinosaurs/velociraptor.jpg"in res.data


