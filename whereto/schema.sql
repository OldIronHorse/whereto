drop table if exists towns;
create table towns (
  id integer primary key autoincrement,
  commune text not null,
  department text not null,
  region text not null
);
