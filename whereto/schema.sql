drop table if exists towns;
create table towns (
  id integer primary key autoincrement,
  commune text not null,
  department text not null,
  region text not null
);
drop table if exists routes;
create table routes (
  origin_id integer not null,
  destination_id integer not null,
  duration integer not null,
  duration_text text not null,
  distance integer not null,
  distance_text text not null
);
