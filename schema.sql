-- task tracking / trello

create table boards (
  id serial primary key,
  name text unique not null,
  is_favorite boolean not null default false
);

create unique index one_favorite on boards (is_favorite) where (is_favorite is true);

create table columns (
  id serial primary key,
  name text not null,
  index integer not null,  -- allow overlaps for now
  board_id integer not null references boards (id),
  unique (board_id, name),
  unique (board_id, index)
);

create table cards (
  id serial primary key,
  board_id integer not null references boards (id),
  column_id integer not null references columns (id),
  name text not null,
  body text,
  unique (board_id, name)
);

create table tags (
  id serial primary key,
  name text unique not null
);

create table card_tags (
  id serial primary key,
  card_id integer not null references cards (id),
  tag_id integer not null references tags (id),
  unique (card_id, tag_id)
);


-- SRS / flashcards

create table flashcard_decks (
  id serial primary key,
  name text unique not null,
  is_favorite boolean not null default false
);

create table flashcards (
  id serial primary key,
  deck_id integer not null references flashcard_decks (id),
  front text,
  back text
);

create table flashcard_reviews (
  id serial primary key,
  flashcard_id integer not null references flashcards (id),
  review_time timestamp with time zone not null default now(),
  correct boolean not null default false
);
