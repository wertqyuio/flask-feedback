from app import app
from models import db, User
import unittest

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_test'
db.create_all()


class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and make new cupcake."""

        User.query.delete()

        self.client = app.test_client()

        self.new_user = User.register("un_Test","password","test@test.com","fn_test","ln_user")

        db.session.add(self.new_user)
        db.session.commit()

    def test_public_get_routes(self):
        '''Check to see if we can access all public routes.'''

        response_home = self.client.get('/')
        response_register = self.client.get('/register')
        response_login = self.client.get('/login')
        response_secret = self.client.get('/secret')

        self.assertEqual(response_home.status_code, 302)
        self.assertEqual(response_register.status_code, 200)
        self.assertEqual(response_login.status_code, 200)
        self.assertEqual(response_secret.status_code, 200)

    # def test_add_new_user_by_form(self):
    #     '''Create a new user through a post request to register.'''

    #     response = self.client.post('/register', data={"username":"SecondTest",
    #                                                    "password":"passw0rd",
    #                                                    "email":"email@email.com",
    #                                                    "first_name":"First name",
    #                                                    "last_name":"Last name"})

    #     self.assertEqual(response.status_code, 302)

        

  