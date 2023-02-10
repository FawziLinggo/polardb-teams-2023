CREATE TABLE public."user" (
	id serial4 NOT null primary key,
	email varchar NOT null unique,
	"password" varchar(255) NOT NULL,
	username varchar NOT null unique
);