create table boards (
  id serial primary key,
  name text unique
);

create table columns (
  id serial primary key,
  name text,
  index integer,
  board_id integer references boards (id),
  unique (board_id, name),
  unique (board_id, index)
);

create table cards (
  id serial primary key,
  board_id integer references boards (id),
  column_id integer references columns (id),
  name text,
  body text,
  unique (board_id, name)
);

create table tags (
  id serial primary key,
  name text unique
);

create table card_tags (
  id serial primary key,
  card_id integer references cards (id),
  tag_id integer references tags (id),
  unique (card_id, tag_id)
);
