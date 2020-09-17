
use agenda;
create table usuarios
(id_usuario int primary key auto_increment not null,
 nombres char(20),
 apellidos char(20),
 usuario char(40),
 password varchar(255) not null
);
create table eventos 
(id int primary key auto_increment not null,
 titulo char(70),
 hora time,
 dia date,
 descripcion varchar(250)
);