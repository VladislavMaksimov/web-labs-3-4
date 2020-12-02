create table users
(
	id integer not null
		constraint users_pk
			primary key autoincrement,
	email text not null,
	password text not null
);

create unique index users_email_uindex
	on users (email);

create table tasks
(
	id integer not null
		constraint tasks_pk
			primary key autoincrement,
	title text not null,
	description text,
	user_id integer not null
);