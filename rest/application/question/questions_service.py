import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.engine.result import Result
from config import Config

from application.question.model.dto.question import Question
from application.question.model.mapper.question_mapper import QuestionMapper
from application.models import Page

class QuestionFilters:
    def __init__(self, author_id):
        self.author_id = author_id

class QuestionsService:
    def __init__(self):
        self.questions_mapper = QuestionMapper()
        self.db_engine = create_engine(Config.POSTGRES_DB_URL)

    def _execute_query(self, query, args_dict) -> Result:
        try:
            with self.db_engine.connect() as connection:
                result = connection.execute(query, args_dict)
                connection.commit()
                inserted_rows = result.rowcount
                print(f'Query: {query}. Inserted rows: {inserted_rows}')
                return result
        except Exception as e:
            print(f'Error: {e}')
            raise
    
    def _get_question_dict(self, question) -> dict:
        question_dict = {'id': str(question.id),
                        'author_id': str(question.author_id),
                        'body': question.body}
        return question_dict

    def _create_question_db(self, question) -> None:
        query = text('''
        INSERT INTO questions (id, author_id, body)
        VALUES (:id, :author_id, :body);
        ''')
        self._execute_query(query, self._get_question_dict(question))
        return
    
    def _update_question_db(self, question) -> None:
        query = text('''
        UPDATE questions
        SET body = :body
        WHERE id = :id;
        ''')
        self._execute_query(query, self._get_question_dict(question))
        return
    
    def create_question(self, request_data) -> Question:
        question = self.questions_mapper.map_request(request_data)
        self._create_question_db(question)
        return question
    
    def update_question(self, question_id, request_data) -> Question:
        question = self.questions_mapper.map_request(request_data)
        self._update_question_db(question)
        return question
    
    def get_question(self, question_id) -> Question:
        query = text('''
        SELECT id, author_id, body
        FROM questions
        WHERE id = :question_id;
        ''')
        result = self._execute_query(query, {'question_id': str(question_id)}).first()
        if result:
            return self.questions_mapper.map_entity_to_dto(result)
        else:
            print('Failed to retrieve the question.')
    
    def get_questions(self, filters: QuestionFilters, page: int, size: int) -> Page[Question]:
        if filters.author_id is None:
            print('Missing author id')
            return Page(size=size, page=page, total_pages=1, content=[])
        else:
            query = text('''
            SELECT id, author_id, body
            FROM questions
            WHERE author_id = :author_id;
            ''')
            result = self._execute_query(query, {'author_id': str(filters.author_id)}).all()
            if result and len(result)>0:
                questions = [self.questions_mapper.map_entity_to_dto(q) for q in result]
                return Page(size=size, page=page, total_pages=1, content=questions)
            else:
                print(f'Failed to find author with id {filters.author_id}.')
                return Page(size=size, page=page, total_pages=1, content=[])