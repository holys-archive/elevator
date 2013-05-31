--drop table if exists movie;
create table movie_new(
    id integer primary key autoincrement not null,
    title text not null,
    download_url text not null,
    movie_url text not null,
    douban_url text,
    douban_title text,
    lpic_url text,
    douban_id integer,
    sended integer default 0,
    download_url_md5 text,
    upload_date text
);
