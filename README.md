# 3D-Bitcoin coin
Fabrica tu propia moneda Bitcoin con una impresora 3D doméstica.
<p align="center">
  <img src="./imagenes/albertocoin_photo_01.png">
</p>

## Introducción
Este repositorio contiene instrucciones, software y modelos CAD diseñados para permitir a un usuario crear sus propias monedas físicas Bitcoin.

## Definición
Una moneda Bitcoin es un dispositivo tangible, con aspecto de moneda, que permite a su poseedor almacenar una cantidad determinada de bitcoins.

## Historia
Las primeras monedas físicas fueron creadas por Mike Caldwell, bajo el nombre comercial de "Casacius coins". Tras un moderado éxito inicial, dejaron de fabricarse en 2013, después de recibir amenazas legales dado que, según el Departamento del Tesoro de EEUU dichas monedas constituyen un modo de "transmisión de dinero" lo que requiere, según la ley estadounidense, la obtención de licencias específicas. Por este motivo, el creador decidió retirarlas del mercado al considerar que no era rentable la obtención de dichas licencias.

Posteriormente han aparecido otras ofertas comerciales, la mayoría de las cuales han ido desapareciendo por diversos motivos.

En consecuencia, en la actualidad no es fácil adquirir una moneda Bitcoin de un proveedor comercial, por lo que surge este proyecto para facilitar la producción de tales monedas al usuario final.

## Requisitos
Para fabricar tu moneda necesitarás:

### Software
1. Intérprete Python 3.6 o superior
2. MonedaBitcon.py (en este repositorio). Un script que permite la generación de las claves privada/pública de la moneda, así como los códigos QR correspondientes.
3. Entropy.txt. Un fichero de texto plano que contiene una cadena SECRETA de texto que se utilizará para generar las claves privadas y públicas de las moneda.

> ATENCIÓN
> Es vital que el usuario final cambie el texto contenido en Entropy.txt por su propio texto secreto.
> De no hacderlo así es PRÁCTICAMENTE SEGURO que pierda sus fondos Bitcoin.
4. Un programa de diseño gráfico, tal como Adobe Photoshop, Adobe Illustrator, Google Docs, GIMP, etc.
Este programa se usará para componer el documento que contiene las claves y códigos QR.


