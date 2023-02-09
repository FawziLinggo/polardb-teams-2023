CREATE TABLE public.stock_price (
	id serial4 NOT null primary key,
	stock_id int4 not null,
	date date null,
	open float8 not null,
	high float8 not null,
	low float8 not null,
	close float8 not null,
	adj_close float8 not null,
	volume float8 not null,
	foreign key (stock_id) references stock (id)
);
