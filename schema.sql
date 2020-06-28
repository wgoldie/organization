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
