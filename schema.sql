drop table if exists movie;
create table movie(
    id integer primary key autoincrement not null,
    title text not null,
    download_url text not null,
    movie_url text not null,
    douban_url text,
    douban_title text,
    lpic_url text,
    sended integer default 0
);
