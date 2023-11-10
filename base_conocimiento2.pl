producto('Fideos Tirabuzon','Don Vicente','500 grs',739.02).
producto('Fideos Nido fettuccine','Lucchetti','500 grs',547.47).
producto('Fideos Codito','Canale','500 grs',302.68).
producto('Capelettini con carne NI','Giacomo','500 grs', 1114.96).

producto('Aceitunas verdes rellenas premiun','Nucete','220 cc',928.74).

producto('Pure de tomate de 1030 grs','De La Huerta','1030 grs',865.28).
producto('Pulpa de tomate suave','Arcor','520 grs',292.77).
producto('Pure de tomate de 530 grs','De La Huerta','530 grs',480.69).
producto('Pure de tomate de 210 grs','De La Huerta','210 grs',249.93).

producto('Fernet','Capri','700 cc',1151.52).
producto('Fernet Menta Ricetta Italiana','Branca','750 cc',2699.99).
producto('Granadina','Cusenier','750 cc',917.20).

producto('Vino Capitulo Uno Chardonnay','Ruca Malen','750 ml',3906.49).
producto('Vino Capitulo Uno Cabernet Sauvignon','Ruca Malen','750 ml',3906.49).

producto('Jabon Barra Ecolavado Coco X2','Ala','400 grs',560.31).
producto('Apresto C/Aromatizante DoyPack','Ecovita','500 ml',229.99).
producto('Suavizante Concentrado Oleo de Argan','Comfort','450 ml',599.99).
producto('Perfume P/Tela Suavidad de Beb DP','Poett','250 ml',473.58).

producto('Cera p/pisos liquida Roble claro','Suiza','850 cc',2873.42).
producto('Cera p/pisos liquida Roble claro','Suiza','425 cc',1838.19).
producto('Cera p/pisos liquida Roble oscuro','Suiza','425 cc',1838.19).
producto('Cera p/pisos liquida natural','Suiza','425 cc',1949.62).

categoria_producto('Cera p/pisos liquida Roble claro','Limpieza Pisos y Grandes Superficie').
categoria_producto('Cera p/pisos liquida Roble claro chico','Limpieza Pisos y Grandes Superficie').
categoria_producto('Cera p/pisos liquida Roble oscuro','Limpieza Pisos y Grandes Superficie').
categoria_producto('Cera p/pisos liquida natural','Limpieza Pisos y Grandes Superficie').

categoria_producto('Jabon Barra Ecolavado Coco X2','Limpieza de Ropa').
categoria_producto('Apresto C/Aromatizante DoyPack','Limpieza de Ropa').
categoria_producto('Suavizante Concentrado Oleo de Argan','Limpieza de Ropa').
categoria_producto('Perfume P/Tela Suavidad de Beb DP','Limpieza de Ropa').

categoria_producto('Vino Capitulo Uno Chardonnay','Vino').
categoria_producto('Vino Capitulo Uno Cabernet Sauvignon','Vino').

categoria_producto('Fernet','Aperitivo y Coctel').
categoria_producto('Fernet Menta Ricetta Italiana','Aperitivo y Coctel').
categoria_producto('Granadina','Aperitivo y Coctel').

categoria_producto('Pure de tomate de 1030 grs','Conservas').
categoria_producto('Pulpa de tomate suave','Conservas').
categoria_producto('Pure de tomate de 530 grs','Conservas').
categoria_producto('Pure de tomate de 210 grs','Conservas').

categoria_producto('Aceitunas verdes rellenas premiun','Encurtidos').

categoria_producto('Fideos Tirabuzon', 'Pastas Secas').
categoria_producto('Fideos Nido fettuccine', 'Pastas Secas').
categoria_producto('Fideos Codito', 'Pastas Secas').
categoria_producto('Capelettini con carne NI', 'Pastas Secas').

descuento('Fideos Tirabuzon', 10).
descuento('Fideos Nido fettuccine', 5).
descuento('Fideos Codito', 8).
descuento('Capelettini con carne NI', 15).

descuento('Aceitunas verdes rellenas premiun', 12).

descuento('Pure de tomate de 1030 grs', 7).
descuento('Pulpa de tomate suave', 3).
descuento('Pure de tomate de 530 grs', 5).

descuento('Fernet', 10).
descuento('Fernet Menta Ricetta Italiana', 15).
descuento('Granadina', 8).

descuento('Vino Capitulo Uno Chardonnay', 5).
descuento('Vino Capitulo Uno Cabernet Sauvignon', 5).

descuento('Jabon Barra Ecolavado Coco X2', 10).
descuento('Apresto C/Aromatizante DoyPack', 5).
descuento('Suavizante Concentrado Oleo de Argan', 7).
descuento('Perfume P/Tela Suavidad de Beb DP', 3).

descuento('Cera p/pisos liquida Roble claro', 10).
descuento('Cera p/pisos liquida Roble oscuro', 10).
descuento('Cera p/pisos liquida natural', 10).


descuento_categoria('Pastas Secas', 5).
descuento_categoria('Encurtidos', 10).
descuento_categoria('Conservas', 9).
descuento_categoria('Aperitivo y Coctel', 8).
descuento_categoria('Vino', 6).
descuento_categoria('Limpieza de Ropa', 12).
descuento_categoria('Limpieza Pisos y Grandes Superficie', 15).

calcular_descuento_categoria(Categoria, Descuento) :-
    descuento_categoria(Categoria, Porcentaje),
    Descuento is (Porcentaje / 100).
consulta_categoria_con_descuento(Categoria, Producto, PrecioConDescuento, DescuentoPorcentaje, Marca, Peso) :-
    categoria_producto(Producto, Categoria), % Verifica que el producto pertenezca a la categoría especificada
    producto(Producto, Marca, Peso, PrecioOriginal),
    calcular_descuento_categoria(Categoria, DescuentoPorcentaje),
    PrecioConDescuento is PrecioOriginal - (PrecioOriginal * DescuentoPorcentaje).


