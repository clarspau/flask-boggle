from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        """Setup code to run before each test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test the homepage route."""
        with self.client:
            # Send a GET request to the '/' route
            response = self.client.get('/')

            # Check if 'board' is in the session
            self.assertIn('board', session)

            # Check if 'highscore' and 'nplays' are None in the session
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('numplays'))

            # Check if specific HTML elements are present in the response
            self.assertIn(b'<p>High Score:', res.data)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'Seconds Left:', res.data)

    def test_valid_word(self):
        """Test if a word is valid by modifying the board in the session."""
        with self.client as client:
            with client.session_transaction() as sess:
                # Simulate a game board in the session
                sess['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        # Send a GET request to check if the word 'cat' is valid
        response = self.client.get('/word-check?word=cat')

        # Check if the response indicates that the word is valid
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if a word is not on the board."""
        self.client.get('/')
        # Send a GET request to check if the word 'impossible' is valid
        response = self.client.get('/word-check?word=impossible')

        # Check if the response indicates that the word is not on the board
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if a non-English word is not in the dictionary."""
        self.client.get('/')
        # Send a GET request to check a non-English word
        response = self.client.get(
            '/word-check?word=fsjdakfkldsfjdslkfjdlksf')

        # Check if the response indicates that the word is not in the dictionary
        self.assertEqual(response.json['result'], 'not-word')
