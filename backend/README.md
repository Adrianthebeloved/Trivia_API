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

### Documentation

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
`GET '/questions'`

- Fetches a dictionary containing all categories, a paginated set of questions in same category in which the keys are the ids and the value is the corresponding string of the category and key value pairs for the questions dictionaries.
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample: curl `http://127.0.0.1:5000/questions`

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
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }]
}
```

`GET '/categories/<int:category_id>/questions'`

- Fetches a dictionary of questions in a given category with the category id requested
- Request Arguments: None
- Returns: An question objects in key: value pairs.
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`

```json
{
  "Category": 2,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist with initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }]
}
```

`POST '/questions/'`

- Sends a post request to add a new question
- Request Arguments: None
- Returns: Returns a success value and the posted question's id.
- Sample: `curl -i -X POST -H "Content-Type: application/json" -d '{"question": "In what year was the last World Cup?", "answer": "2018", "difficulty": 3, "category":6}'`

```json
{
  "added": 45,
  "success": true
}
```

`DELETE '/questions/<int:question_id>'`

- Deletes the question with the given id
- Request Arguments: question_id
- Returns: The deleted question's id
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/70`

```json
{
  "deleted":70,
  "success": true
}

```

`POST '/questions'`

- Searches for a question based on a search term
- Request Arguments: None
- Returns: The total number of questions and the questions related to thre search term
- Sample: `curl -i -X POST -H "Content-Type: application/json" -d '{"searchTerm":"World Cup"}' http://127.0.0.1:5000/questions`

```json
{
  "currentCategory": null, 
  "questions": [
    {
      "answer": "2018", 
      "category": 6, 
      "difficulty": 3, 
      "id": 75, 
      "question": "In what year was the last World Cup?"
    }
  ], 
  "success": true, 
  "totalQuestions": 1
}
```

`POST '/quizzes'`

- Request Argument: None
- Returns a random quize question to play the game

```json
{
  "question": {
    "answer": "Uruguay", 
    "category": "6", 
    "difficulty": 4, 
    "id": 11, 
    "question": "Which country won the first ever soccer World Cup in 1930?"
  }, 
  "success": true
}
```

## Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "success": false,
    "error": 404,
    "message": "resource not found"
}
```
The API will return three error types when requests fail:

- `400: Bad Request`
- `404: Resource Not Found`
- `422: Not Processable`
- `500: Internal server error`

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
