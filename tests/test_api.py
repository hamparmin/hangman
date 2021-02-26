from server import app
from unittest import TestCase, TestSuite
import json
import sys
import hangman
import random
import string

# Monkey patch the create game function so we can have a deterministic word to test with. This should
# probably read the words from some config and not rely on hardcoded vars but this is simpler.
original_hangman_create = hangman.create_hangman_game


def create_game_with_override_words(words=None, guess_limit=5):
    return original_hangman_create(words=["abac"], guess_limit=5)


hangman.create_hangman_game = create_game_with_override_words


def parse_response(response):
    return json.loads(response.get_data().decode(sys.getdefaultencoding()))


#create a TestCase obj for each test / for more tests I'd modularize tests and use TestSuite runner
class TestApiIntegration(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def get_game(self, game_id):
        return self.app.get(f"/api/hangman/{game_id}")

    def test_get_hangman_missing(self):
        invalid_game_id = 9999
        response = self.get_game(invalid_game_id)
        self.assertEqual(response.status_code, 404)

class TestNewEndpoint(TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_guess_endpoint(self): #test if new route for guessing is working
        create_response=self.app.post(f"/api/hangman") #create game
        game_id=create_response.get_json()["gameId"]
        self.assertEqual(create_response.status_code,200)

        #get game by id
        get_game_response=self.app.get(f"/api/hangman/{game_id}")
        self.assertEqual(get_game_response.status_code,200)

        #post guess request
        valid_char="a" #alphanumeric valid char
        post_data=json.dumps({"letter": valid_char})
        guess_response=self.app.post(f"/api/hangman/{game_id}/guess",data=post_data, content_type="application/json")
        self.assertEqual(guess_response.status_code,200)

class TestWin(TestCase): #test specific guess functionality
    def setUp(self):
        self.app = app.test_client()
    
    def test_post_gamewon(self):
        create_response=self.app.post(f"/api/hangman") #create game
        game_id=create_response.get_json()["gameId"]
    
        self.app.get(f"/api/hangman/{game_id}") #get game by id

        for char in "abac": #use monkeypatched testcase / submit letter by letter until game over
            post_data=json.dumps({"letter": char})
            response=self.app.post(f"/api/hangman/{game_id}/guess",data=post_data, content_type="application/json")
            if char!='c':#check response for in progress state
                self.assertEqual(response.get_json()['state'],"IN_PROGRESS")
        
        #check response after game over => should be "WON"
        post_game_response=self.app.post(f"/api/hangman/{game_id}/guess",data=post_data, content_type="application/json")
        self.assertEqual(post_game_response.get_json()['state'],"WON")
    
class TestLose(TestCase): #test specific guess functionality
    def setUp(self):
        self.app = app.test_client()
        
    def test_post_gamelost(self):
        create_response=self.app.post(f"/api/hangman") #create game
        game_id=create_response.get_json()["gameId"]

        self.app.get(f"/api/hangman/{game_id}") #get game by id

        for char in "qwert": #use incorrect input of len>5 of different chars
            post_data=json.dumps({"letter": char})
            response=self.app.post(f"/api/hangman/{game_id}/guess",data=post_data, content_type="application/json")
            if char!="t": #check response for in progress state
                self.assertEqual(response.get_json()['state'],"IN_PROGRESS")

        #check response after game over => should be "LOST"
        self.assertEqual(response.get_json()['state'],"LOST")

class TestInvalidInput(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_invalid_input(self):
        #one could theoretically input infinite invalid inputs and it should not effect game_state
        create_response=self.app.post(f"/api/hangman") #create game
        game_id=create_response.get_json()["gameId"]
        
        self.app.get(f"/api/hangman/{game_id}") #get game by id
        invalid_inputs=string.punctuation #'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        for char in invalid_inputs:
            post_data=json.dumps({"letter": char})
            response=self.app.post(f"/api/hangman/{game_id}/guess",data=post_data, content_type="application/json")
        self.assertEqual(response.get_json()['state'],"IN_PROGRESS")
        
    
