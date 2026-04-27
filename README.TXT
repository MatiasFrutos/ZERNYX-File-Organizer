============================================================
ZERNYX FILE ORGANIZER
============================================================

Creado por:
Matias Frutos · ZERNYX

------------------------------------------------------------
DESCRIPCION
------------------------------------------------------------

ZERNYX File Organizer es una herramienta de escritorio creada
en Python para ordenar archivos de una carpeta por tipo.

Pensada para escritorios, carpetas de descargas, carpetas de
clientes, archivos administrativos, documentos tecnicos y entornos
PYME donde suele acumularse informacion mezclada.

------------------------------------------------------------
FUNCIONES
------------------------------------------------------------

- Seleccionar carpeta.
- Analizar archivos antes de mover.
- Vista previa de destino.
- Organizar por categorias.
- Incluir o no subcarpetas.
- Crear carpeta organizada con fecha.
- Evitar sobrescritura de archivos.
- Deshacer ultimo movimiento.
- Ver historial.
- Abrir carpeta desde la aplicacion.

------------------------------------------------------------
CATEGORIAS
------------------------------------------------------------

Imagenes:
.jpg, .jpeg, .png, .gif, .webp, .bmp, .svg

Documentos:
.pdf, .doc, .docx, .txt, .rtf, .odt

Planillas:
.xls, .xlsx, .csv, .ods

Presentaciones:
.ppt, .pptx, .odp

Comprimidos:
.zip, .rar, .7z, .tar, .gz

Videos:
.mp4, .mov, .avi, .mkv, .wmv

Audio:
.mp3, .wav, .ogg, .flac, .m4a

Codigo:
.py, .js, .html, .css, .php, .java, .json, .xml, .sql, .bat

Instaladores:
.exe, .msi

Otros:
todo archivo no reconocido

------------------------------------------------------------
COMO EJECUTAR
------------------------------------------------------------

Doble click en:

ejecutar.bat

O desde CMD:

python zernyx_file_organizer.py

------------------------------------------------------------
ESTRUCTURA
------------------------------------------------------------

ZERNYX-File-Organizer/
|
|-- zernyx_file_organizer.py
|-- ejecutar.bat
|-- README.txt
|-- organizer_historial.txt          Se genera automaticamente
|-- organizer_ultimo_movimiento.txt  Se genera automaticamente

------------------------------------------------------------
NOTAS
------------------------------------------------------------

- La aplicacion mueve archivos, no los copia.
- Antes de mover muestra una vista previa.
- El ultimo movimiento puede deshacerse.
- Si un archivo ya existe, se crea una copia con numeracion.
- No elimina informacion.
- El historial queda registrado en TXT.

------------------------------------------------------------
CREDITOS
------------------------------------------------------------

Desarrollo realizado por Matias Frutos · ZERNYX
============================================================