drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  imdb_id text not null,
  title text not null,
  rating real
);
create table episodes (
  id integer,
  episode text not null,
  title text not null,
  rating text not null
);