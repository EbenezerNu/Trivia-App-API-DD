import json
from logging import exception
import os
import sys
from unicodedata import category
from urllib import response
from flask import (
    Flask, 
    request, 
    abort, 
    Response, 
    flash, 
    redirect, 
    url_for, 
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from sqlalchemy import and_, or_

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/*": {"origins": "*"}}, withCredentials=True, supports_credentials=True)


    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """Pagination Function
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    def paginate(data, page):
        start = (int(page) - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        if len(data) < end:
            end = len(data) - 1
            
        if start >= len(data):
            return []
        else:
            return data[start:end]

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    @cross_origin()
    def categoriesFunction():
        data = {}
        data = {c.id : c.type for c in Category.query.all()}
        print(data)
        return jsonify({ "categories" : data,
                "success" : True}), 200


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    @cross_origin()
    def getQuestions():
        try:
            page = request.args.get('page', 1)
            data = []
            {data.append(c.format()) for c in Question.query.all()}
            questions = paginate(data, page)
            if len(questions) == 0:
                return jsonify({"message": "Page limit exceeded", "error": sys.exc_info(), "success": False}), 404

            response = []
            currentCategory_id = questions[len(questions)-1]['category']
            currentCategory = Category.query.get(currentCategory_id)
            categories = {}
            categories = {c.id : c.type for c in Category.query.all()}
            response = {
                "questions" : questions,
                "total_questions": len(questions),
                "current_category": currentCategory.type,  
                "categories": categories,
                "success" : True
                }
            print("Categories : ", categories)
            return jsonify(response), 200
        
        except:
            abort(400)
        finally:
            print("GetQuestion")


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """


    @app.route('/questions', methods=['POST'])
    @cross_origin()
    def createQuestion():
        try:
            data = request.get_json()
            if data.get('question'):
                print("Data : ", data , "\n")
                if(data):
                    category_ = Category.query.get_or_404(data.get('category'))
                    if category_:
                        question = Question(
                            question = data.get('question'),
                            answer = data.get('answer'),
                            category = data.get('category'),
                            difficulty = int(data.get('difficulty')))
                        question.insert()
                        return jsonify({"message": "Question has successfully been created!",
                "success" : True}), 200
                    else:
                        return jsonify({"message": "Category id does not exist!",
                "success" : False}), 404
            else:
                abort(422)
        except:
            return jsonify({"message": "Could not complete your insertion. Check your request data well",
                "success" : False}), 400
        finally:
            db.session.close

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """


    @app.route('/questions/search', methods=['POST'])
    @cross_origin()
    def searchQuestions():
        try:
            data = request.get_json()
            # THE SEARCH METHOD 
            if data.get('searchTerm') is not None:
                term = request.get_json(silent=True).get('searchTerm')
                keyword = "%{}%".format(term)
                questions = []
                data = Question.query.filter(Question.question.ilike(keyword)).all()
                if len(data) == 0:
                    return jsonify({
                        "questions": data,
                        "total_questions": len(data),
                        "current_category": {},
                        "success" : False
            }), 200
            elif data.get('searchTerm') is None:
                data = Question.query.all()

            idx = data[len(data)-1].category
            print("idx : ", idx, "\nQuestions : ", questions)
            current_category = Category.query.get(idx)
            {questions.append(q.format()) for q in data}
            return jsonify({
                "questions": questions,
                "total_questions": len(questions),
                "current_category": current_category.type,
                "success" : True
            }), 200

        except:
            return jsonify({"message": "Could not complete your search. Check your request data well",
                "success" : False}), 400
        finally:
            print("search complete")

    """Endpoint to get a single Question
    
    Keyword arguments: Uses question id as path variable
    argument -- description
    Return: question and a success = True if successful
    """

    @app.route('/questions/<int:id>', methods=['GET'])
    @cross_origin()
    def getQuestion(id):
        try:
            print("ID : ", id, "Data : ")
            data = Question.query.get(id)
            response = data.format()
            return jsonify({"question" : response,
                "success" : True}), 200
        except:
            return jsonify({"message": "The question id does not exist.",
                "success" : False}), 404
        finally:
            print("get question")


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:id>', methods=['DELETE'])
    @cross_origin()
    def deleteQuestion(id):
        try:
            question = Question.query.get_or_404(id)
            question.delete()
            return jsonify({"message": "Question has been deleted!",
                "success" : True}), 200
        except:
            return jsonify({"message": "The question id does not exist.",
                "success" : False}), 404
        finally:
            print("Delete question")


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    @cross_origin()
    def filter_by_category(id):
        try:
            response = []
            category = Category.query.filter(Category.id == id).first()
            print('Category : ', category)
            if category is not None:
                data = Question.query.filter(Question.category == id).all()
                questions = []
                size_ = 0
                print("Data: ", data)
                if len(data) != 0:
                    {questions.append(q.format()) for q in data}
                    size_ = len(questions)

                response = { 
                    "questions": questions, 
                    "total_questions": size_, 
                    "current_category": category.type, 
                    "success" : True
                    }
                print("Response : ", response)
                return jsonify(response), 200
            else:
                return jsonify({"message": "Category cannot be found",
                "success" : False}), 404
        except:
            return jsonify({"message": "No category was selected",
                "success" : False}), 400
        finally:
            print ("End Filter")

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    @cross_origin()
    def random_question():
        try:
            questions = []
            previous = []
            request_ = request.get_json()
            print("Request : ", request_)
            if request_.get('previous_questions'):
                previous = request_.get('previous_questions')
            category = {}
            data = []
            if request_.get('quiz_category'):
                category = request_.get('quiz_category')
            if (category.get('id') == 0) and (len(previous) == 0):
                data = Question.query.all()
            elif (category.get('id') == 0) and (len(previous) != 0):
                data = Question.query.filter(Question.id not in previous).all()
            elif (category.get('id') != 0) and (len(previous) == 0):
                data = Question.query.filter(Question.category == category.get('id')).all()
            elif (category.get('id') != 0) and (len(previous) != 0):
                data = Question.query.filter(and_(Question.category == category.get('id'), Question.id not in previous)).all()
            else:
                abort(404)

            print("Data : ", data)
            { questions.append(q.format()) for q in data}
            idx = random.randint(0, len(questions)-1)

            return jsonify({
                "question": questions[idx],
            "success" : True
                }), 200
        except:
            return jsonify({"message": "Could  not filter questions",
            "success" : False}), 404
        finally:
            print ("End Random")



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"message": "Data is not found", "error" : sys.exc_info(),
                "success" : False}), 404


    @app.errorhandler(422)
    def server_error(error):
        return jsonify({"message": "Unable to process user instructions.\nPleease modify your request before sending another one", "error" : sys.exc_info(),
                "success" : False}), 422
    
    @app.errorhandler(405)
    def invalid_method_error(error):
        return jsonify({"message": "Method is not allowed", "error" : sys.exc_info(),
                "success" : False}), 405


    if __name__ == "__main__":
        app.run(debug=True)

    return app


