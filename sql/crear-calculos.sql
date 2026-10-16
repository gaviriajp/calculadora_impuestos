create table if not exists calculos (
  id_calculo varchar(40) primary key not null,
  precio_base decimal not null,
  nombre_impuesto varchar(50) not null,
  valor_impuesto decimal not null,
  cantidad_bolsas int not null,
  valor_bolsas decimal not null,
  total decimal not null
);
