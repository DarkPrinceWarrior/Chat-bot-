use Chat_bot_DB;

create table Music(

    id int primary key auto_increment,
    song_name varchar(100) not null unique

);

INSERT into  Music(song_name) values('Nickelback - When we stand together');
INSERT into  Music(song_name) values('The Weekend - starboy');
INSERT into  Music(song_name) values('Linkin Park - Numb');
INSERT into  Music(song_name) values('Arash - Boro boro');

