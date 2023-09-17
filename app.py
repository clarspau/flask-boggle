from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# Subclass TestCase to create a test class


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()  # Create a test client
        app.config['TESTING'] = True  # Set the app to testing mode

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        # Use the test client to send a GET request to the home page
        with self.client:
            response = self.client.get('/')

            # Assert that the 'board' key exists in the session
            self.assertIn('board', session)

            # Assert that 'highscore' and 'nplays' are not in the session
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

            # Assert that specific HTML elements are present in the response
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        # Create a test client and modify the session to contain a specific board
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]

        # Use the test client to send a GET request to check a word
        response = self.client.get('/check-word?word=cat')

        # Assert the result of the word check
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        # Send a GET request to the home page
        self.client.get('/')

        # Use the test client to send a GET request to check an invalid word
        response = self.client.get('/check-word?word=impossible')

        # Assert the result of the word check
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        # Send a GET request to the home page
        self.client.get('/')

        # Use the test client to send a GET request to check a non-English word
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')

        # Assert the result of the word check
        self.assertEqual(response.json['result'], 'not-word')
