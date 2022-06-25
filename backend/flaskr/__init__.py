from logging import exception
import os
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
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, withCredentials=True, supports_credentials=True)


    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/categories')
    @cross_origin()
    def categoriesFunction():
        data = []
        {data.append(c.format()) for c in Category.query.all()}
        print(data)
        return jsonify(data), 200


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

    @app.route('/api/questions', methods=['GET', 'POST'])
    @cross_origin()
    def questionsFunction():
        if request.method == 'GET':
            
            page = request.args.get('page', 1)
            data = []
            {data.append(c.format()) for c in Question.query.all()}
            start = (int(page) - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
        
            if start > len(data):
                return jsonify({"Message": "Page Number Exceeded!"}), 404
            else:
                response = data[start:end]
                currentCategory_id = response[len(response)-1]['category']
                currentCategory = Category.query.get(currentCategory_id)
                response.append({
                    "Total Number of Questions": len(response),
                    "Current Category": currentCategory.type
                    })
                return jsonify(response), 200

        elif request.method == 'POST':
            try:
                data = request.get_json()
                print("Data : {\nQuestion : ", data['question'], "\nAnswer : ", data['answer'])
                if(data is not None):
                    question = Question(
                        question = data['question'],
                        answer = data['answer'],
                        category = data['category'],
                        difficulty = data['difficulty']
                    )
                    question.insert()
                    return jsonify({"Message": "Question has successfully been created!"}), 200
                else:
                    raise exception
            except:
                return jsonify({"Message": "Could not complete your insertion. Check your request data well"}), 400
            finally:
                db.session.close

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/api/questions/<int:id>', methods=['GET', 'DELETE'])
    @cross_origin()
    def questionFunction(id):
        
        if request.method == 'DELETE':
            try:
                Question.query.get_or_404(id).delete()
                return jsonify({"Message": "Question has been deleted!"}), 200
            except:
                return jsonify({"Message": "The question id does not exist."}), 404
            finally:
                db.session.close()


        elif request.method == 'GET':
            try:
                response = []
                print("ID : ", id, "Data : ")
                data = Question.query.get(id)
                response.append(data.format()) 
                return jsonify(response), 200
            except:
                return jsonify({"Message": "The question id does not exist."}), 404
            finally:
                db.session.close()


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """



    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/api/questions/search', methods=['POST'])
    @cross_origin()
    def search_questions():
        if request.method == 'POST':
            try:
                response = []
                term = request.get_json(silent=True)['term']
                keyword = "%{}%".format(term)
                data = Question.query.filter(Question.question.ilike(keyword)).all()
                {response.append(q.format()) for q in data}
                return jsonify(response), 200
            except:
                return jsonify({"Message": "Could not search for questions"}), 404
            finally:
                print ("End Search")


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/api/questions/filter', methods=['GET'])
    @cross_origin()
    def filter_by_category():
        if request.method == 'GET':
            try:
                response = []
                request_ = request.get_json(silent=True)
                if request_['term'] is not None:
                    filter = "%{}%".format(request_['term'])
                    category_ = Category.query.filter(Category.type.ilike(filter)).first()
                    data = Question.query.filter(Question.category == category_.id).all()
                    {response.append(q.format()) for q in data}
                return jsonify(response), 200
            except:
                return jsonify({"Message": "Could not filter questions"}), 404
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

    @app.route('/api/questions/game', methods=['POST'])
    @cross_origin()
    def random_question():
        if request.method == 'POST':
            try:
                response = []
                request_ = request.get_json(silent=True, force=True)
                previous = -1
                category = "All"
                if request_.get('previous'):
                    previous = request_.get('previous')

                if request_.get('category'):
                    category = request_.get('category')

                if (category.lower() == "all") and previous:
                    data = Question.query.filter(Question.id != previous).all()
                elif (category.lower() == "all"):
                    data = Question.query.get().all()
                else:
                    filter = "%{}%".format(category)
                    category_ = Category.query.filter(Category.type.ilike(filter)).first()
                    if previous:
                        data = Question.query.filter(and_(Question.category == category_.id, Question.id != previous)).all()
                    else:
                            data = Question.query.filter(Question.category == category_.id).all()

                { response.append(q.format()) for q in data}
                idx = random.randint(0, len(response)-1)

                return jsonify(response[idx]), 200
            except:
                return jsonify({"Message": "Could not filter questions"}), 404
            finally:
                print ("End Random")



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    if __name__ == "__main__":
        app.run(debug=True)

    return app


