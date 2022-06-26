import os
import random
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.wrong_quiz = {
            "quiz_category" : { "id": 10, "type" : "noway"}
        }

        self.category = {4, "History"}
        self.wrong_category = {100, "Math"}
        self.previous_questions = [1, 3]
        self.searchTerm = "Who"
        self.question = {
            "question" : "When did COVID 19 spread to Ghana?",
            "answer" : "2020",
            "category" : 4,
            "difficulty" : 1
        }
        
        self.current_category = { 2: "Entertainment"}

        self.quiz = {
            "quiz_category" : { "id": 4, "type" : "History"},
            "previous_questions" : [10, 5]
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # self.db.session.add(self.category1)
            # self.db.session.commit()
            # self.db.session.add(self.category2)
            # self.db.session.commit()
            # self.db.session.add(self.category3)
            # self.db.session.commit()

            # self.db.session.add(self.question1)
            # self.db.session.commit()
            # self.db.session.add(self.question2)
            # self.db.session.commit()
            # self.db.session.add(self.question3)
            # self.db.session.commit()
            # self.db.session.add(self.question4)
            # self.db.session.commit()
            # self.db.session.add(self.question5)            
            # self.db.session.commit()

            self.db.session.close()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

# GET CATEGORIES

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
        self.assertTrue(data["success"])


# GET QUESTIONS
    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["success"])

    def test_get_questions_with_page(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["success"])
    
    def test_404_invalid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data["message"])
        self.assertTrue(data["error"])
        self.assertFalse(data["success"])

# CREATE QUESTION

    def test_create_question(self):
        res = self.client().post("/questions", json=self.question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["message"], "Question has successfully been created!")
        self.assertTrue(data["success"])

    # def test_405_cannot_create_question(self):
    #     res = self.client().post("/questions/1", json=self.question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["message"], "Question has successfully been created!")
    #     self.assertFalse(data["success"])

# SEARCH QUESTION

    def test_search_question(self):
        res = self.client().post("/questions/search", json={'searchTerm' : self.searchTerm})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["success"])

    def test_empty_searchterm_search_question(self):
        res = self.client().post("/questions/search", json={'searchTerm' : ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["success"])
    
    def test_no_searchterm_search_question(self):
        res = self.client().post("/questions/search")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(data["message"])
        self.assertFalse(data["success"])

# DELETE QUESTION

    def test_delete_question(self):
        res = self.client().delete("/questions/36")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["message"], "Question has been deleted!")
        self.assertTrue(data["success"])

    def test_404_invalid_id_delete_question(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "The question id does not exist.")
        self.assertFalse(data["success"])

    # def test_405_invalid_method_delete_question(self):
    #     res = self.client().delete("/questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertTrue(data["message"])
    #     self.assertFalse(data["success"])

# FILTER BY CATEGORY

    def test_filter_question(self):
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["success"])

    def test_404_invalid_filter_question(self):
        res = self.client().get("/categories/100/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data["message"])
        self.assertFalse(data["success"])


        # QUIZZES

    def test_random_question(self):
        res = self.client().post("/quizzes", json=self.quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])
        self.assertTrue(data["success"])

    def test_no_input_random_question(self):
        res = self.client().post("/quizzes")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data["message"])
        self.assertFalse(data["success"])

    def test_404_input_not_found_random_question(self):
        res = self.client().post("/quizzes", json=self.wrong_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data["message"])
        self.assertFalse(data["success"])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()