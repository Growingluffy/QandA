CREATE TABLE users (
  id serial primary key,
  name text not null,
  password text not null,
  expert boolean not null,
  admin boolean not null
);

CREATE TABLE question (
  id serial primary key,
  question_text text not null,
  answer_text text not null,
  asked_by_id integer not null,
  expert_id integer not null
);
