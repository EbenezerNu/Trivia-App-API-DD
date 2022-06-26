# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

`GET '/questions'`

- Fetches a dictionary of questions, total_questions, current_category, categories in which the keys.
- Request Arguments: Page number is an integer as request parameter to access the paginated questions.
- Returns: An object with `questions`, `total_questions`, `current_category`, `categories` and `success`.
  - The `questions` key contains an array of paginated question objects.
  - The `total_questions` key contains the number of items in the array of questions.
  - The `current_category` key contains the type attribute of the category of the last question object in the questions object
  - The `categories` key contains an object of `id: category_string` key: value pairs.
  - The `success` key contains a boolean true.

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "category": "2",
      "difficulty": 3
    }
  ],
  "total_questions": 1,
  "current_category": "Art",
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

`POST '/questions'`

- Sends a request with a question object to be saved into the database.
- Request Arguments: a `question` object.
- Returns: An object with `message` and `success`.
  - The `message` key contains a string
  - The `success` key contains a boolean true.

```json
{
  "message": "Question has been saved",
  "success": true
}
```

`POST '/questions/search'`

- Fetches a dictionary of questions, total_questions, current_category, categories in which the keys.
- Request Arguments: An object with `searchTerm` as key and a string value.
- Returns: An object with `questions`, `total_questions`, `current_category`, `categories` and `success`.
  - The `questions` key contains an array of question objects which has its question key containing `searchTerm`.
  - The `total_questions` key contains the number of items in the array of questions.
  - The `current_category` key contains the type attribute of the category of the last question object in the questions object
  - The `categories` key contains an object of `id: category_string` key: value pairs.
  - The `success` key contains a boolean true.

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "category": "2",
      "difficulty": 3
    }
  ],
  "total_questions": 1,
  "current_category": "Art",
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

`DELETE '/questions/<int:id>'`

- Sends a request with a question object's id to be deleted from the database.
- Request Arguments: a category `id` as integer.
- Returns: An object with `message` and `success`.
  - The `message` key contains a string
  - The `success` key contains a boolean true.

```json
{
  "message": "Question has been deleted",
  "success": true
}
```

`GET '/categories/<int:id>/questions'`

- Fetches a dictionary of questions, total_questions, current_category, categories in which the keys.
- Request Arguments: An integer path variable as `id`.
- Returns: An object with `questions`, `total_questions`, `current_category`, `categories` and `success`.

  - The `questions` key contains an array of question objects which are of the category `id`.
  - The `total_questions` key contains the number of items in the array of questions.
  - The `current_category` key contains the type attribute of the category of the last question object in the questions object.
  - The `success` key contains a boolean true.

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "category": "2",
      "difficulty": 3
    }
  ],
  "total_questions": 1,
  "current_category": "Art",
  "success": true
}
```

`POST '/quizzes'`

- Fetches an oject of keys `question` and `success`, where `question` is a random question based on input arguments.
- Request Arguments: An object of containing a keys `quiz_category` and `previous_questions`, and values category object and an array of questions' ids respectively.
- Returns: An object with `question` and `success`.
  - The `question` key contains a random quesiton object of category `quiz_category` and is not in the array `previous_questions`.
  - The `success` key contains a boolean true.

```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "category": "2",
    "difficulty": 3
  },
  "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
