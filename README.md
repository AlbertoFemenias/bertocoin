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
Las primeras monedas físicas fueron creadas por Mike Caldwell, bajo el nombre comercial de ["Casacius coins"](https://en.bitcoin.it/wiki/Casascius_physical_bitcoins). Tras un moderado éxito inicial, dejaron de fabricarse en 2013, después de recibir amenazas legales dado que, según el Departamento del Tesoro de EEUU dichas monedas constituyen un modo de "transmisión de dinero" lo que requiere, según la ley estadounidense, la obtención de licencias específicas. Por este motivo, el creador decidió retirarlas del mercado al considerar que no era rentable la obtención de dichas licencias.

Posteriormente han aparecido otras ofertas comerciales, la mayoría de las cuales han ido desapareciendo por diversos motivos.

En consecuencia, en la actualidad no es fácil adquirir una moneda Bitcoin de un proveedor comercial, por lo que surge este proyecto para facilitar la producción de tales monedas al usuario final.

## Requisitos
Para fabricar tu moneda necesitarás:

### Software
1. Intérprete Python 2.7 superior. 
   - Dependencias: 

     **ecdsa** (Utilizado para los cálculos criptográficos)
     **pyqrcode** (Utilizado para la generación de los códigos QR de la moneda)


2. MonedaBitcon.py (en este repositorio). Un script que permite la generación de las claves privada/pública de la moneda, así como los códigos QR correspondientes.
3. Entropy.txt. Un fichero de texto plano que contiene una cadena SECRETA de texto que se utilizará para generar las claves privadas y públicas de las moneda.


> :warning: **ATENCIÓN**
>
> Es vital que el usuario final cambie el texto contenido en Entropy.txt por su propio texto secreto.
> De no hacerlo así, es PRÁCTICAMENTE SEGURO que pierda sus fondos Bitcoin.

4. Un programa de diseño gráfico, tal como Adobe Photoshop, Adobe Illustrator, Google Docs, GIMP, etc.

Este programa se usará para componer el documento que contiene las claves y códigos QR.

### Hardware
1. Impresora 3D de filamento. 
Se utiliza para imprimir la carcasa de la moneda. 
Para este proyecto de utilizó una Anet A8, pero cualquier impresora Prusa o similar es perfectamente válida.
Notas: 
   - Debido al proceso de colocación de insertos dentro de la moneda, NO se pueden utilizar impresoras de resina.
   - Se recomienda utilizar plástico PLA.
   - El diseño está optimizado para un cabezal extrusor de 0.4 mm.

2. Impresora Láser/Inyección de tinta.
Se puede utilizar cualquier impresora láser de calidad doméstica. Respecto a las impresoras de inyección de tinta se recomienda utilizar tinta original y consultar la duración de la impresión en las características técnicas de durabilidad del fabricante.
3. Papel A4
Se recomienda utilizar papel blanco o amarillo de oficina con un gramaje de 100 gr/m2.
4. Arandela
El diseño prevé la inserción de una arandela metálica para darle total opacidad a la clave secreta guardada en el interior.
La arandela recomendada tiene un diámetro exterior de 30 mm y un grosor de 2 mm.

5.- Lámina de metacritalo transparente de 1 mm de espesor.

## Uso del software

1. En caso de que el ordenador no cuente con un intérprete de Python 2.7, es preciso comenzar por instalarlo.
Para ello, siga las instrucciones del fabricante de su sistema operativo.

    Enlaces de descarga: 
    
    - [Python 2.70](https://www.python.org/downloads/release/python-270/)
    - [Otras versiones](https://www.python.org/downloads/)

2. Si no están instalados previamente, se requiere instalar los paquetes de Python **ecdsa**, **pypng** y **pyqrcode**. 

Para ello, pueden utilizarse los siguientes comandos:

     pip2.7 install ecdsa
     pip2.7 install.pypng
     pip2.7 install pyqrcode

3. Descargar el script de este repositorio denominado 'bertocoin.py' y el fichero de entropia 'entropia.txt' y colocar ambos en un mismo directorio.


5. Editar el fichero 'entropia.txt' con un editor de texto plano, tal como Notepad en Windows o TextEdit en OS X y reemplazar el contenido por una cadena SECRETA de caracteres.
Es recomendable que la cadena contenga suficiente entropía como para que sea difícil de adivinar.
Siga las recomendaciones habituales que se recommiendan para generar claves secretas, tales como:
   - Tamaño: 20 posiciones o más
   - Caracteres: Utilice una mezcla de mayúsculas, minúsculas y símbolos especiales
   
5. Desde ese directorio lanzar el siguiente comando:

     ```python2.7 bertocoin.py```
     
       
6. Una vez lanzado el programa, si la ejecución fue correcta, se generará un sub-directorio, llamado **delete-me** donde aparecerán un fichero denominado **print-me.eps**.
Este es un fichero, en formato PostScript Encapsulado que contiene una hoja con las instrucciones y la imagen que debemos imprimir y colocar dentro de la moneda 3D.


> :warning: **ATENCIÓN**
>
> El usuario dispone de 3 minutos para imprimir este fichero.
> Después, el directorio **delete-me** y todo su contenido se borrará automáticamente, ya que contiene
> la clave privada con la que se podría acceder a los fondos de la moneda.
> Si por alguna razón, el borrado automático no funcionase, es **imperativo borrar manualmente** el 
> directorio **delete-me** y todo su contenido.
> De no hacerlo así es PRÁCTICAMENTE SEGURO que pierda sus fondos Bitcoin si algún actor malicisioso
> accediese a la información contenida en este directorio.
> Este ejemplo solamente se ofrece para que el usuario verifique el funcionamiento del software.
>
> En **NINGÚN CASO** se deben generar las monedas reales utilizando este valor de ejemplo.
   
## Impresión y colocación de la carátula impresa

El fichero _print-me.eps_ contiene una carátula recortable que se ha de insertar dentro de la moneda 3D .
En la siguiente imagen, podemos ver una imagen de un fichero de ejemplo:

<p align="left">
  <img src="./imagenes/bertocoin_print-me_ejemplo.png">
</p>

Es importante imprimir esta hoja y recortarlo siguiendo las instrucciones que aparecen en la misma **antes** de iniciar el proceso de impresión 3D de la moneda.

Una vez impresa y recortada la carátula, se deberá utilizar la lámina transparente de metacrilato y recortar una pieza en forma de hexágono de las mismas dimensiones que la carátula que acabamos de imprimir.

El impresor deberá pausar la impresión de la moneda 3D aproximadamente a la mitad del proceso.
Entonces, se introducirán, en este orden:

1.- La pieza hexagonal de metacrilato.
2.- La carátula plegada, siguiendo las instrucciones de la hoja impresa, y dejando visible la cara identificada como "COIN_XXXX_PUBLIC".
3.- La arandela metálica, que proporciona opacidad a la clave privada, inserta en la moneda, y fija la carátula para asegurar que se mantiene en su sitio al continuar con el proceso de impresión 3D.

Una vez colocados los tres insertos, se continuará con la impresión de la moneda 3D.




