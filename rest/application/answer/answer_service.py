import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.engine.result import Result

from config import Config
from application.answer.model.dto.answer import Answer
from application.answer.model.mapper.answer_mapper import AnswerMapper
from application.models import Page

class AnswerFilters:
    def __init__(self, author_id, question_id):
        self.author_id = author_id
        self.question_id = question_id

class AnswerService:
    def __init__(self):
        self.answer_mapper = AnswerMapper()
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

    def _get_answer_dict(self, answer) -> dict:
        answer_dict = {'id': str(answer.id),
                       'author_id': str(answer.author_id),
                       'question_id': str(answer.question_id),
                       'score': answer.score,
                       'body': answer.body}
        return answer_dict
    
    def _create_answer_db(self, answer) -> None:
        query = text('''
        INSERT INTO answers (id, author_id, question_id, score, body)
        VALUES (:id, :author_id, :question_id, :score, :body);
        ''')
        self._execute_query(query, self._get_answer_dict(answer))
        return
    
    def _update_answer_db(self, answer) -> None:
        query = text('''
        UPDATE answers
        SET body = :body
        WHERE id = :id;
        ''')
        self._execute_query(query, self._get_answer_dict(answer))
        return
    
    def create_answer(self, request_data) -> Answer:
        answer = self.answer_mapper.map_request(request_data)
        self._create_answer_db(answer)
        return answer
    
    def update_answer(self, answer_id, request_data) -> Answer:
        answer = self.answer_mapper.map_request(request_data)
        answer.id = answer_id
        self._update_answer_db(answer)
        return answer
    
    def get_answer(self, answer_id) -> Answer:
        query = text('''
        SELECT id, author_id, question_id, score, body
        FROM answers
        WHERE id = :answer_id;
        ''')
        result = self._execute_query(query, {'answer_id': str(answer_id)}).first()
        if result:
            return self.answer_mapper.map_entity_to_dto(result)
        else:
            print('Failed to retrieve the answer.')
    
    def get_answers(self, filters: AnswerFilters, page: int, size: int) -> Page[Answer]:   
        if filters.author_id is None or filters.question_id is None:
            print('Missing author id or question id')
            return Page(size=size, page=page, total_pages=1, content=[])
        else:
            query = text('''
            SELECT id, author_id, question_id, score, body
            FROM answers
            WHERE author_id = :author_id AND question_id = :question_id;
            ''')
            result = self._execute_query(query, {'author_id': str(filters.author_id),
                                                 'question_id': str(filters.question_id)}).all()
            if result and len(result)>0:
                answers = [self.answer_mapper.map_entity_to_dto(a) for a in result]
                return Page(size=size, page=page, total_pages=1, content=answers)
            else:
                print(f'Failed to find question {filters.question_id} with author {filters.author_id}.')
                return Page(size=size, page=page, total_pages=1, content=[])
            

    
