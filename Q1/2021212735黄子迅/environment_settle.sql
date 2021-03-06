create database if not exists guest;
create database if not exists root;
create database if not exists super_root;
use super_root;
create table if not exists translate(id int not null primary key auto_increment,user_name varchar(20) not null);
create table if not exists history(id int not null primary key auto_increment,user_id int not null,time varchar(30) not null,content varchar(60) not null);
create table if not exists info(id int not null primary key auto_increment,password varchar(20) not null);
create table if not exists server_list(id int not null primary key auto_increment,server_name varchar(20) not null,server_location varchar(30) not null);
use root;
create table if not exists ssh_server(id int not null primary key auto_increment,user_id int not null,server_name varchar(20) not null,server_target varchar(20) not null);
create table if not exists translate(id int not null primary key auto_increment,user_name varchar(20) not null);
create table if not exists history(id int not null primary key auto_increment,user_id int not null,time varchar(30) not null,content varchar(60) not null);
create table if not exists command(id int not null primary key auto_increment,user_id int not null,command_start varchar(16) not null,command_last varchar(100) not null);
create table if not exists info(id int not null primary key auto_increment,password varchar(20) not null);
create table if not exists server_list(id int not null primary key auto_increment,server_name varchar(20) not null,server_location varchar(30) not null);
use guest;
create table if not exists ssh_server(id int not null primary key auto_increment,user_id int not null,server_name varchar(20) not null,server_target varchar(20) not null);
create table if not exists translate(id int not null primary key auto_increment,user_name varchar(20) not null);
create table if not exists history(id int not null primary key auto_increment,user_id int not null,time varchar(30) not null,content varchar(60) not null);
create table if not exists command(id int not null primary key auto_increment,user_id int not null,command_start varchar(16) not null,command_last varchar(100) not null);
create table if not exists info(id int not null primary key auto_increment,password varchar(20) not null);
create table if not exists server_list(id int not null primary key auto_increment,server_name varchar(20) not null,server_location varchar(30) not null);
