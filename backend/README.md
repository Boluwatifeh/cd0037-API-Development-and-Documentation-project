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

First activate your virtual environment and make sure the you are in the parent directory of your venv
```bash
source ./venv/bin/activate
```

Navigate to the backend directory and run the following commands

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


### API Documentation 

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with two keys, `categories`, that contains an object of `id: category_string` key: value pairs and `success` which is a boolean value.

Example response

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
- Fetches a dictionary of an arry of questions, categories, current_category.
- Request arguements: None
- Returns: An object of 5 keys {
  "categories",
  "current_category",
  "questions",
  "success",
  "total_questions
}

Example response

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
    "current_category": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        ...
        ],
    "success": true,
    "total_questions": 21
}
```

`DELETE '/questions/<question_id>'`

- Delete question using a question id 
- Request arguements: None
- Returns: An object with 2 keys {
  "question_id",
  "success"
}

Example response


```json
[
    {
        "question_id": 13,
        "success": true
    },
    200
]
```

`POST '/questions'`

- This creates a new question in the database
- Arguement: Request data {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
}

Example response

```json
[
    {
        "question_id": 19,
        "success": true
    },
    201
]
```
`POST '/searchquestions'`

- Fetches a question with the given search term from the list of quies
- Request arguement: {
    "searchTerm" : "actor"
}

Example response

```json
{
    "current_category": 5,
    "question": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }
    ],
    "success": true,
    "total_question": 1
}
```
`GET '/categories/<category_id>/questions'`

- Fetch a list of questions in the specified category 
- Returns: An object with 4 keys {
  "current_category", 
  "questions",
  "success",
  "total_questions"
}


Example response

```json
[
    {
        "current_category": 2,
        "questions": [
            {
                "answer": "Escher",
                "category": 2,
                "difficulty": 1,
                "id": 16,
                "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
            },
            {
                "answer": "Mona Lisa",
                "category": 2,
                "difficulty": 3,
                "id": 17,
                "question": "La Giaconda is better known as what?"
            },
            {
                "answer": "One",
                "category": 2,
                "difficulty": 4,
                "id": 18,
                "question": "How many paintings did Van Gogh sell in his lifetime?"
            },
            {
                "answer": "Jackson Pollock",
                "category": 2,
                "difficulty": 2,
                "id": 19,
                "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
            }
        ],
        "success": true,
        "total_questions": 4
    },
    200
  ```

`POST '/quizzes'`
- Randomly fetch a quiz question that is not in the list of previous questions specified in the request body
- Request arguements: {
  "previous questions" : [2, 1, 3],
    "quiz_category"   : {"type" : "Science", "id" : "1"}
}

Example response

```json
{
    "question": {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    "success": true
}
```


## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```
