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
        self.database_name = "trivia"
        self.database_path = "postgresql://{}/{}".format('postgres:tobe@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # new question for testing
        self.test_question = {
            "question": "How long?",
            "answer": "Soon",
            "category": "3",
            "difficulty": 2
            }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        """ Test to successfully display all categories using a list"""
        res = self.client().get("/categories")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

    def test_paginated_questions(self):
        """ Test to get paginated questions"""
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
    
    def test_404_page_not_found(self):
        """ 
        Test to return 404 error when requested page > available pages
        """
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)

    def test_delete_question(self):
        """ Test to delete questions successfully"""
        question = Question(
            question=self.test_question["question"],
            answer=self.test_question["answer"],
            difficulty=self.test_question["difficulty"],
            category=self.test_question["category"],
        )
        question.insert()
        question_id = question.id

        res = self.client().delete("/questions/" + str(question_id))
        data = json.loads(res.data)

        question = Question.query.get(question_id)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsNone(question)

    def test_delete_question_error(self):
        """
        Test to throw error when trying to delete
        out of range or not found questions
        """
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)

    def test_add_question(self):
        """Test to add questions successfully"""
        res = self.client().post("/questions", json=self.test_question)
        data = json.loads(res.data)
        question = Question.query.get(data["added"])

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(question)

    def test_add_question_error(self):
        """ Test to return error upon adding invalid question format"""
        res = self.client().post("/questions", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)

    def test_search_questions(self):
        """ Test to search for questions successfully"""
        res = self.client().post("/questions", json={"searchTerm": "movie"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])

    def test_search_questions_no_input(self):
        """
        Test to search for empty search phrase 
        does not result in error
        """
        res = self.client().post("/questions", json={"searchTerm": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])

    def test_search_questions_nonexistent(self):
        """
        Test to ensure questions not found
        does not throw an error
        """
        res = self.client().post("/questions", json={"searchTerm": "abcdxyz"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(len(data["questions"]))
        self.assertFalse(data["totalQuestions"])

    def test_get_questions_by_category(self):
        """ Test to search questions by category """
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])

    def test_play_quiz(self):
        """ Test to get questions to play the quiz """
        res = self.client().post("/quizzes", json={
            "previous_questions": [8, 12],
            "quiz_category": {"type": "Geography", "id": "3"}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])


    def test_quiz_format_error(self):
        """ Test to return error if not quiz"""
        res = self.client().post("/quizzes", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()