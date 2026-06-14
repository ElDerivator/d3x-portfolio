# D3X Portfolio

Portafolio estatico para `d3x.biz`, creado con contenido base del CV de Luis Rivero y 11 credenciales documentadas.

## Archivos

- `index.html`: estructura del portafolio.
- `styles.css`: diseno responsive.
- `script.js`: navegacion suave y pequenos comportamientos.
- `assets/delitruck-01.jpeg` a `assets/delitruck-03.jpeg`: fotos usadas por la galeria Delitruck.

## Accesibilidad y rendimiento

La pagina incluye enlace para saltar al contenido, menu movil con estados `aria`, navegacion activa por seccion e imagenes de galeria con dimensiones estables, carga diferida y decodificacion asincrona.

## Minijuego

La seccion `#game` contiene `D3X Signal Run`, un minijuego de clasificacion operativa. El visitante recibe senales y debe decidir si corresponden a `Automate`, `Validate`, `Escalate` o `Dashboard`. La logica vive en `script.js` y la interfaz en `#game-root`.

## Galeria y experiencia de campo

La seccion de experiencia profesional incluye una galeria Delitruck con tres imagenes `.jpeg`, thumbnails visuales, controles anterior/siguiente y una descripcion lateral de aprendizaje operativo: eventos, servicio al cliente, inventario, precios, promociones y ejecucion en punto de venta.

El timeline tambien incluye Delitruck como experiencia formal y resume la evolucion profesional desde servicio al cliente hacia datos, operaciones y automatizacion.

## Metodo D3X

La pagina incluye una seccion de metodo de trabajo: mapear friccion, validar datos, automatizar con control y medir decisiones.

## Propuesta de valor

La pagina incluye un bloque de capacidades practicas: reducir trabajo manual, ordenar datos operativos y mejorar visibilidad para decisiones.

El hero incluye un resumen rapido del perfil con foco, herramientas y tipo de problemas donde Luis puede aportar.

La seccion de proyectos incluye un bloque de enfoque actual para conectar automatizacion, validacion de archivos operativos y sistemas trazables antes de mostrar los casos.

## Formacion academica

La pagina incluye una seccion de educacion con estudios en Administracion de Empresas y Psicologia, presentada como formacion cursada con enfoque profesional aplicado y cierre administrativo de titulacion pendiente por servicio social.

## Credenciales

La seccion de credenciales incluye un mapa de aprendizaje por categorias: Data, BI/ETL, Product/Agile y Language, seguido por las credenciales individuales.

## Animaciones

El sitio usa animaciones suaves de entrada con `IntersectionObserver`, microinteracciones en tarjetas y botones, contadores animados en el panel D3X, un pipeline operativo con pulso de datos, progreso de lectura, navegacion activa, tilt sutil en tarjetas y una barra de tiempo animada dentro del minijuego. Tambien respeta `prefers-reduced-motion` para reducir movimiento cuando el navegador lo solicite.

## Como verlo localmente

Abre `index.html` en el navegador o usa un servidor estatico desde esta carpeta.

## Publicacion en d3x.biz

Squarespace Domains administra el dominio, pero no reemplaza por si solo a un hosting web. Hay dos rutas:

1. Usar Squarespace Website Builder y recrear esta pagina con secciones, textos y estilos similares.
2. Publicar estos archivos en un hosting estatico como GitHub Pages, Netlify o Vercel, y apuntar `d3x.biz` desde Squarespace Domains con los registros DNS del proveedor.

La ruta mas flexible para este portafolio es hosting estatico + dominio conectado desde Squarespace Domains.

## Acabados

La pagina incluye metadata Open Graph, color de tema, favicon SVG embebido, estados de proyecto, menu responsive accesible y footer con regreso al inicio.
