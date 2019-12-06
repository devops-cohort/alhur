import unittest

from flask import abort, url_for
from flask_testing import TestCase
from os import getenv
from application import app, db
from application.models import Users


class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://'+str(getenv('MY_SQL_USER'))+':'+str(getenv('MY_SQL_PASSWORD'))+'@'+str(getenv('MY_SQL_URL'))+'/'+str(getenv('MY_SQL_DB'))        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password="admin2016")

        # create test non-admin user
        employee = Users(first_name="test", last_name="user", email="test@user.com", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestApplication(TestBase):
    def test_homepage_view(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)
        
    def test_login_view(self):
        """Tests if login page is available when logged out"""
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_view(self):
        """looks to see users are redirected to dashboard if they are already logged in"""
        target_url = url_for('users', user_id=2)
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_account_view(self):
        """Tests if login page is available when logged out"""
        response = self.client.get(url_for('account'))
        self.assertEqual(response.status_code, 302)


