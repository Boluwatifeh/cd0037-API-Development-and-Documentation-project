from crypt import methods
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        formatted_categories = {category.id :category.type for category in categories}
        return jsonify({
                        'success': True,
                        'categories': formatted_categories
                        })

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
    def paginator_helper_function(request, requested_data):
        current_page = request.args.get('page', 1, type=int)
        start = (current_page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_data = [data.format() for data in requested_data]
        current_data = formatted_data[start:end]
        return current_data

    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        paginated_questions = paginator_helper_function(request, questions)
        if len(paginated_questions) == 0:
            abort(404)
        categories = Category.query.all()
        formatted_categories = {category.id :category.type for category in categories}
        current_category = formatted_categories
        return jsonify({
                        'success': True,
                        'questions': paginated_questions, 
                        'total_questions': len(questions),
                        'current_category': current_category, 
                        'categories': formatted_categories
                        })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({'success': True, 'question_id':question.id}, 200)
        except:
            abort(422)

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
    def post_question():
        body = request.get_json()
        if not body:
            abort(400)
        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')
        
        if not question or not answer or not difficulty or not category:
            abort(400)
        try:
            new_question = Question(question=question,  answer=answer, category=category, difficulty=difficulty)
            new_question.insert()
            return jsonify({'success': True, 'question_id': new_question.id}, 201)
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    @app.route('/searchquestions', methods=['POST'])
    def search_question():
        body = request.get_json()
        searched_term = body.get("searchTerm", None)
        print(searched_term)
        questions = Question.query.filter(Question.question.ilike('%' + searched_term + '%')).all()
        if questions:
            formatted_questions = [question.format() for question in questions]
            categories = Category.query.all()
            index = formatted_questions[0]['category']
            formatted_categories = {category.id :category.type for category in categories}
            return (jsonify({
                            'success': True,
                            'questions': formatted_questions, 
                            'totalQuestions': len(questions),
                            'currentCategory': formatted_categories[index]
                             }))
        else:
            return (jsonify({'message' :'No Result for searched question!', 
                            'success':False},
                            404) )
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_question_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        questions = Question.query.filter(Question.category == str(category_id)) \
            .all()
        formatted_questions = paginator_helper_function(request, questions)
        return ( jsonify({'success': True, 
                        'questions': formatted_questions, 
                        'total_questions': len(questions),
                        'current_category': category.type}), 200)

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
    def get_quiz():
        req_body = request.get_json()
        quiz_category = req_body.get('quiz_category',None)
        previous_questions = req_body.get('previous_questions', None)

        try:
            if quiz_category.get('id') == 0: 
                selection = Question.query.all()
            else:
                selection = Question.query.filter(Question.category == quiz_category.get('id')).all()
                    
            if selection is None or len(selection) == 0: 
                return jsonify({
                    'question': None
                })  
            questions= [question.format() for question in selection if question.id not in previous_questions] 
            
            if questions is None or len(questions) == 0: 
                return jsonify({
                    'question': None
                }) 
            else: 
                question = random.choice(questions)
            
            return jsonify({
                'success': True, 
                'question': question
            })
            
        except Exception as e:
            abort(422)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": "Bad request",
            "error": 400,
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "message": "Requested resource not  found",
            "error": 404
        }), 404
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "message": "Method not allowed for requested url",
            "error": 405,
        }), 405
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "message": 'Request can not be processed',
            "error": 422
        }), 422
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "message": "internal server error",
            "error": 500
        }), 500

    return app

