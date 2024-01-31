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