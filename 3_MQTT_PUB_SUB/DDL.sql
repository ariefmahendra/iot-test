create database monitoring;

create table weather (
    id int primary key auto_increment,
    topic varchar(100),
    humidity varchar(100),
    temperature varchar(100)
);

select * from weather;

