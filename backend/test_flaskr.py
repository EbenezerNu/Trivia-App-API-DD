import os
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
            "quiz_category" : { 10 : "noway"}
        }

        self.category = {1, "History"}
        self.category1 = {"History"}
        self.category2 = {"Entertainment"}
        self.category3 = {"Football"}
        self.wrong_category = {100, "History"}
        self.previous_questions = [1, 3]
        self.question = {
            "question" : "When did COVID 19 spread to Ghana?",
            "answer" : "2020",
            "category" : "1",
            "difficulty" : 1
        }
        self.question1 = Question(
            question="When did COVID 19 spread to Togo?",
            answer="2020",
            category = 2,
            difficulty = 2
        )
        self.question2 = Question(
            question="When did COVID 19 spread to Ghana?",
            answer="2020",
            category = 1,
            difficulty = 3
        )
        self.question3 = Question(
            question="When did COVID 19 spread to Congo?",
            answer="2020",
            category = 2,
            difficulty = 4
        )
        self.question4 = Question(
            question="When did COVID 19 spread to China?",
            answer="2019",
            category = 3,
            difficulty = 2
        )
        self.question5 = Question(
            question="When did COVID 19 spread to Nigeria?",
            answer="2020",
            category = 1,
            difficulty = 1
        )
        self.current_category = { 2: "Entertainment"}

        self.quiz = {
            "quiz_category" : { 1 : "History"},
            "previous_questions" : self.previous_questions
        }

        self.wrong_quiz = {
            "quiz_category" : self.wrong_category,
            "previous_questions" : self.previous_questions
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.db.session.add(self.category1, self.category2, self.category3)
            self.db.session.commit()
            self.db.session.add(self.question1, self.question2, self.question3, self.question4, self.question5)
            self.db.session.commit()
            self.db.session.close()

    def tearDown(self):
        """Executed after reach test"""
        self.db.drop_all()
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

    def test_405_cannot_create_question(self):
        res = self.client().post("/questions/1", json=self.question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["message"], "Question has successfully been created!")
        self.assertFalse(data["success"])

# SEARCH QUESTION

    def test_search_question(self):
        res = self.client().post("/questions/search", json={'searchTerm' : "Ghana"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["success"])

    def test_400_no_searchterm_search_question(self):
        res = self.client().post("/questions/search")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(data["message"])
        self.assertFalse(data["success"])

# DELETE QUESTION

    def test_delete_question(self):
        res = self.client().delete("/questions/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["message"], "Question has been deleted!")
        self.assertTrue(data["success"])

    def test_404_invalid_id_delete_question(self):
        res = self.client().delete("/questions/10000000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "The question id does not exist.")
        self.assertFalse(data["success"])

    def test_405_invalid_method_delete_question(self):
        res = self.client().delete("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertTrue(data["message"])
        self.assertFalse(data["success"])

# FILTER BY CATEGORY

    def test_filter_question(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["success"])

    def test_404_invalid_filter_question(self):
        res = self.client().post("/categories/100/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data["message"])
        self.assertFalse(data["success"])
    
    # def test_400_no_filter_question(self):
    #     res = self.client().post("/categories//questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)
    #     self.assertTrue(data["message"])
    #     self.assertFalse(data["success"])

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

        self.assertEqual(res.status_code, 400)
        self.assertTrue(data["question"])
        self.assertTrue(data["success"])

    def test_404_input_not_found_random_question(self):
        res = self.client().post("/quizzes", json=self.wrong_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["question"])
        self.assertFalse(data["success"])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()