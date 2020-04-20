# Bertocoin - Tu propia moneda Bitcoin 3D
Fabrica tu propia moneda Bitcoin con una impresora 3D doméstica.
<p align="left">
  <img src="./imagenes/albercoin_01.png">
</p>

## Introducción
Este repositorio contiene instrucciones, software y modelos CAD diseñados para permitir a un usuario crear sus propias monedas físicas Bitcoin.

## Definición
Una moneda Bitcoin es un dispositivo tangible, con aspecto de moneda, que permite a su poseedor almacenar una cantidad determinada de bitcoins.

## Historia
Las primeras monedas físicas fueron creadas por Mike Caldwell, bajo el nombre comercial de ["Casacius coins"](https://en.bitcoin.it/wiki/Casascius_physical_bitcoins). Tras un moderado éxito inicial, dejaron de fabricarse en 2013, después de recibir amenazas legales dado que, según el Departamento del Tesoro de EEUU, dichas monedas constituyen un modo de "transmisión de dinero" lo que requiere, según la ley estadounidense, la obtención de licencias específicas. Por este motivo, el creador decidió retirarlas del mercado al considerar que no era rentable la obtención de dichas licencias.

Posteriormente han aparecido otras ofertas comerciales, la mayoría de las cuales han ido desapareciendo por diversos motivos.

En consecuencia, en la actualidad no es fácil adquirir una moneda Bitcoin de un proveedor comercial, por lo que surge este proyecto para facilitar la producción de tales monedas al usuario final.

## Requisitos
Para fabricar tu moneda necesitarás:

### Software
1. Intérprete Python 2.7. 
   - Dependencias: 

     - **ecdsa** (Utilizado para los cálculos criptográficos)
     - **pyqrcode** (Utilizado para la generación de los códigos QR de la moneda)
     - **pypng** (Utilizado por pyqrcode para generar el fichero png)


2. ```bertocoin.py``` (en este repositorio). Un script que permite la generación de las claves privada/pública de la moneda, así como los códigos QR correspondientes.


### Hardware
1. Impresora 3D de filamento. 
Se utiliza para imprimir la carcasa de la moneda. 
Para este proyecto de utilizó una Anet A8, pero cualquier impresora Prusa o similar es perfectamente válida.

    Notas: 
   - Debido al proceso de colocación de insertos dentro de la moneda, NO se pueden utilizar impresoras de resina.
   - Se recomienda utilizar plástico PLA.
   - El diseño está optimizado para un cabezal extrusor de 0.4 mm.

2. Impresora Láser/Inyección de tinta.
Se puede utilizar cualquier impresora láser de calidad doméstica. Se recomienda utilizar tinta/tóner original y consultar la duración de la impresión en las características técnicas de durabilidad del fabricante.

3. Papel A4.
Se recomienda utilizar papel blanco o amarillo de oficina con un gramaje de 90 gr/m2 ó superior.

4. Arandela.
El diseño prevé la inserción de una arandela metálica para darle total opacidad a la clave secreta guardada en el interior.
La arandela recomendada tiene un diámetro exterior de 30 mm y un grosor de 2 mm.

5. Lámina de metacritalo transparente de 1 mm de espesor.

## Uso del software

1. En caso de que el ordenador no cuente con un intérprete de Python 2.7, es preciso comenzar por instalarlo.
Para ello, siga las instrucciones del fabricante de su sistema operativo.

    Enlaces de descarga: 
    
    - [Python 2.70](https://www.python.org/downloads/release/python-270/)
    - [Otras versiones](https://www.python.org/downloads/)

2. Si no están instalados previamente, se requiere instalar los paquetes de Python **ecdsa**, **pypng** y **pyqrcode**. 

Para ello, pueden utilizarse los siguientes comandos:

     pip2.7 install ecdsa
     pip2.7 install pypng
     pip2.7 install pyqrcode

3. Descargar el script de este repositorio denominado 'bertocoin.py' en un directorio donde el usuario cuente con permisos de escritura.
   
4. Desde ese directorio lanzar el siguiente comando:

   ```python2.7 bertocoin.py```


>           Es posible especificar varias opciones para conseguir un mayor 
>           control sobre la generación de los datos de la moneda. 
>           Para conocer las opciones disponibles, puede ejecutar el siguiente comando:
>
>           python2.7 bertocoin.py -h
       
       
5. Una vez lanzado el programa, se generará un sub-directorio llamado **delete-me**, donde aparecerá un fichero denominado **print-me.eps**.
Este es un fichero, en formato PostScript Encapsulado, que contiene una hoja con las instrucciones y la carátula que debemos imprimir y colocar dentro de la moneda 3D.


> :warning: **ATENCIÓN**
>
> El usuario dispone de 3 minutos para imprimir este fichero.
> Después, el directorio **delete-me** y todo su contenido se borrará automáticamente, ya que contiene
> la clave privada con la que se podría acceder a los fondos de la moneda.
> Si por alguna razón, el borrado automático no funcionase, es **imperativo borrar manualmente** el 
> directorio **delete-me** y todo su contenido.
> De no hacerlo así es PRÁCTICAMENTE SEGURO que pierda sus fondos Bitcoin si algún actor malicisioso
> accede a la información contenida en este directorio.
>
> La clave privada se generará a partir de una semilla de texto generada aleatoriamente por el programa.
> Si desea facilitar su propia semilla, puede utilizar la opción correspondiente.
> Para conocer todas las opciones disponibles, lance el script con la opción -h.
   
## Impresión y colocación de la carátula impresa

El fichero _print-me.eps_ contiene una carátula recortable que se ha de insertar dentro de la moneda 3D .
Aquí podemos ver una imagen de un fichero de ejemplo:

<p align="left">
  <img src="./imagenes/bertocoin_print-me_ejemplo.png">
</p>

La carátula tiene la siguiente forma:

<p align="left">
  <img src="./imagenes/bertocoin_caratula_ejemplo.png">
</p>

Es preciso imprimir esta hoja y recortar la carátula **antes** de iniciar el proceso de impresión 3D de la moneda.

Una vez impresa y recortada la carátula, se deberá utilizar la lámina transparente de metacrilato y recortar una pieza en forma de hexágono de las mismas dimensiones que la carátula que acabamos de imprimir.

Se deberá pausar la impresión de la moneda 3D aproximadamente a la mitad del proceso.
Entonces, se introducirán, en este orden:

1. La pieza hexagonal de metacrilato.
2. La carátula plegada, siguiendo las instrucciones de la hoja impresa, y dejando visible la cara identificada como "COIN_XXXX_PUBLIC".
3. La arandela metálica, que proporciona opacidad a la clave privada, inserta en la moneda, y fija la carátula para asegurar que se mantiene en su sitio al continuar con el proceso de impresión 3D.

Una vez colocados los tres insertos, se continuará con la impresión de la moneda 3D.

Para mayor información, descargue y lea atentamente este fichero PDF: "Bertocoin - Manual de Impresión de la Moneda 3D".

## Uso de la moneda

Las instrucciones sobre cómo utilizar la moneda, se encuentran en el siguiente fichero PDF: "Bertocoin - Manual del Usuario".


