# Bertocoin - Your own 3D Bitcoin coin
Make your own Bitcoin coin using a domestic 3D printer.
<p align="left">
  <img src="./imagenes/albercoin_01.png">
</p>

## Introduction
This repository contains instructions, software and CAD models to allow regular users make their own physical Bitcoin coins.

## Definition
A Bitcoin coin is a tangible artifact, shaped as a coin, that allows its owner to store in it an arbitrary amount of bitcoin.

## History
The first physical coins were created by Mike Caldwell, under the commerecial name of ["Casacius coins"](https://en.bitcoin.it/wiki/Casascius_physical_bitcoins). After a moderate initial success, they were discontinued in 2013, after receiving legal threats due to the fact that, according to the Department of the Treasure of the U.S., those coins constitute a mode of "transmission of money" which requires, in accordance with the U.S. law, obtaining specific licenses. As a result, the creator decided to retire them from the market, considering that obtaining those licenses was not worthwhile.

Later on, there have been some alternate commercial products, most of them have vanished from the market for different reasons.

Due to that, currently is not easy to acquire a Bitcoin coin from a commercial provider. This project is born to empower the end users to create such coins.

## Requisites
To make your own coin, you will need:

### Software
1. A Python 2.7 interpreter. 
   - Dependencies: 

     - **ecdsa** (Used for crytographical computations)
     - **pyqrcode** (Used to generate the QR codes of the coin)
     - **pypng** (Used by pyqrcode to generate png files)


2. ```bertocoin.py``` (in this repository). A script that generates the private/public keys of the coin, as well as their corresponding QR codes.

### Hardware
1. A filament based, 3D printer. 
Used to print the coin.

We used an Anet AB printer, but any Prusa or similar is perfectly valid.

    Notes: 
   - Due to the need to place some inserts during the printing process, resin printers CAN NOT be used.
   - The recommended material is PLA plastic.
   - The design is optimized for an extruder head of 0.4 mm.

2. A Laser/Inkjet printer.
Any domestic-grade printer can be used. However, it is highly recommended to use original ink/toner as well as looking up the durability of the printed material in the documentation of the manufacturer. 

3. DIN A4 paper.
We recommend using white or yellow office paper with a grammage of de 90 gr/m2 or superior.

4. Washer.
The design prescribes the insertion of a metallic washer to confer total opacity to the secret key stored inside of the coin.
The recommended washer has a thickness of 2 mm and an external diameter of 30 mm.

5. Transparent metacrilate laminate of 1 mm of thickness.

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
       
       
5. Una vez lanzado el programa, se generará un sub-directorio llamado **delete-me**, donde aparecerá un fichero denominado **print-me.svg**.
Este es un fichero, en formato Scalable Vector Graphics, que contiene una hoja con las instrucciones y la carátula que debemos imprimir y colocar dentro de la moneda 3D.


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

<p align="left">
  <img src="./imagenes/modelo.gif">
</p>
El modelo imprimible de la moneda se encuetra disponible en este repositorio.

El fichero _print-me.svg_ contiene una carátula recortable que se ha de insertar dentro de la moneda 3D .
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

<p align="left">
  <img src="./imagenes/explotado3.png">
</p>

Una vez colocados los tres insertos, se continuará con la impresión de la moneda 3D.

Para mayor información, descargue y lea atentamente este fichero PDF: "Bertocoin - Manual de Impresión de la Moneda 3D".

## Uso de la moneda

Las instrucciones sobre cómo utilizar la moneda, se encuentran en el siguiente fichero PDF: "Bertocoin - Manual del Usuario".


