create table boards (
  id serial primary key,
  name text
);

create table columns (
  id serial primary key,
  name text,
  index integer,
  board_id integer references boards (id)
);

create table cards (
  id serial primary key,
  board_id integer references boards (id),
  column_id integer references columns (id),
  name text,
  body text
);

create table tags (
  id serial primary key,
  name text
);

create table card_tags (
  id serial primary key,
  card_id integer references cards (id)
);
