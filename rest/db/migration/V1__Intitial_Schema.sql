CREATE TABLE questions(
    id UUID PRIMARY KEY,
    author_id UUID NOT NULL,
    body TEXT NOT NULL
);

CREATE TABLE answers(
    id UUID PRIMARY KEY,
    author_id UUID NOT NULL,
    question_id UUID NOT NULL,
    score INT NOT NULL,
    body TEXT NOT NULL
);

ALTER TABLE answers
ADD CONSTRAINT fk_question_id
FOREIGN KEY (question_id) REFERENCES questions(id);

CREATE INDEX idx_author_id_questions ON questions(author_id);
CREATE INDEX idx_author_id_answers ON answers(author_id);
