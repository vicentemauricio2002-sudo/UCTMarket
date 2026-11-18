# Fundamentación UX/UI — Marketplace UCT

## 1. Descripción del proyecto

**Marketplace UCT** es una aplicación orientada a la comunidad universitaria, cuyo objetivo es facilitar la publicación, búsqueda, compra, venta e intercambio de productos entre sus integrantes.

La propuesta busca centralizar este tipo de actividades en una plataforma enfocada en estudiantes y miembros de la comunidad universitaria, permitiendo visualizar publicaciones, buscar productos, guardar artículos de interés y acceder a la información de los usuarios que publican.

La interfaz fue desarrollada utilizando **Python, Kivy y KivyMD**, separando la lógica de programación de la interfaz mediante archivos `.py` y `.kv`.

## 2. Metodología UX/UI

Para el diseño de la aplicación se consideraron principios básicos de UX/UI y los resultados obtenidos durante el proceso de investigación realizado mediante una encuesta en Google Forms.

El proceso se organizó en las siguientes etapas:

1. Identificación del problema.
2. Identificación del usuario objetivo.
3. Recopilación de información mediante una encuesta.
4. Análisis de las respuestas obtenidas.
5. Identificación de necesidades y hallazgos.
6. Definición de decisiones de diseño.
7. Elaboración de la interfaz.
8. Implementación del prototipo utilizando Kivy y KivyMD.
9. Revisión de la navegación y experiencia de usuario.

El objetivo fue diseñar una interfaz sencilla y fácil de comprender, reduciendo la cantidad de pasos necesarios para acceder a las funciones principales de la aplicación.

## 3. Usuario objetivo

El usuario principal de Marketplace UCT corresponde a integrantes de la comunidad universitaria, principalmente estudiantes interesados en encontrar, publicar, comprar, vender o intercambiar productos.

Se consideraron características como:

- Uso frecuente de dispositivos móviles y plataformas digitales.
- Necesidad de acceder rápidamente a publicaciones.
- Interés por encontrar productos dentro de la comunidad universitaria.
- Necesidad de identificar al usuario que realiza una publicación.
- Preferencia por una navegación sencilla y directa.
- Posibilidad de aprovechar productos que otros integrantes de la comunidad ya no utilizan.

## 4. Investigación y resultados de la encuesta

Para complementar la identificación de necesidades se realizó una encuesta mediante Google Forms, orientada a conocer los hábitos, experiencias e interés de los posibles usuarios respecto a la búsqueda, compra, venta e intercambio de productos.

La encuesta obtuvo **3 respuestas**. Se utilizó una escala de valoración de 1 a 5, donde 1 representa un nivel muy bajo, nunca o nada de interés, mientras que 5 representa un nivel muy alto, siempre o mucho interés.

### 4.1 Resultados principales

Los siguientes resultados corresponden a los promedios de las respuestas recibidas. En las preguntas con respuestas incompletas se indica la cantidad de participantes que contestaron.

| Aspecto evaluado | Promedio | Respuestas | Interpretación |
|---|---:|---:|---|
| Necesidad de conseguir productos o recursos | 3,50 | 2 | Se observa una necesidad de nivel moderado a alto. |
| Dificultad para encontrar productos o recursos | 2,50 | 2 | La dificultad percibida fue relativamente baja. |
| Dificultad económica por el precio de los productos | 3,50 | 2 | El precio representa una dificultad moderada a alta. |
| Frecuencia con que se necesitan recursos universitarios | 2,50 | 2 | La frecuencia declarada fue relativamente baja. |
| Uso de redes sociales o plataformas de compra y venta | 3,33 | 3 | Existe familiaridad moderada con estas plataformas. |
| Experiencia comprando productos usados | 3,67 | 3 | Se observa experiencia previa en la compra de artículos usados. |
| Experiencia vendiendo productos | 4,00 | 3 | Se observa una experiencia relativamente alta en ventas. |
| Experiencia intercambiando productos | 4,67 | 3 | El intercambio obtuvo una valoración alta. |
| Posibilidad de tener artículos que ya no se utilizan | 3,67 | 3 | Existe una tendencia favorable, aunque las respuestas fueron variadas. |
| Interés en comprar, vender o intercambiar dentro de la comunidad | 4,33 | 3 | Se observa un interés alto en realizar estas actividades. |
| Disposición a pagar por la aplicación | 2,00 | 3 | La disposición a pagar fue baja. |
| Interés en encontrar u ofrecer productos en una plataforma universitaria | 3,67 | 3 | Se observa un interés moderado a alto. |
| Frecuencia estimada de uso de una plataforma de este tipo | 2,67 | 3 | La frecuencia esperada de uso fue moderada-baja. |
| Viabilidad de aceptar distintos medios de pago | 4,33 | 3 | Las respuestas muestran una valoración favorable. |

*Nota: La pregunta sobre disposición a pagar aparecía duplicada en el formulario. Para evitar contar dos veces la misma información, se consideró una sola vez.*

### 4.2 Interpretación de los hallazgos

A partir de los resultados se identificaron los siguientes aspectos:

1. **Interés en el intercambio universitario:** la pregunta sobre el interés en comprar, vender o intercambiar productos dentro de la comunidad obtuvo un promedio de 4,33. Esto entrega una señal favorable respecto a la propuesta de conectar a integrantes de la universidad mediante una plataforma común.

2. **Experiencia previa de los usuarios:** las respuestas muestran experiencia en la compra, venta e intercambio de artículos, especialmente en esta última actividad, que obtuvo un promedio de 4,67. Esto sugiere que las funciones principales de la aplicación pueden basarse en actividades que los participantes ya conocen.

3. **Importancia del precio:** la dificultad económica asociada al precio de los productos obtuvo un promedio de 3,50. Este resultado permite considerar el acceso a artículos a precios convenientes y la reutilización de productos como aspectos relevantes de la propuesta.

4. **Interés en una plataforma universitaria:** el interés por encontrar u ofrecer productos dentro de una plataforma enfocada en la comunidad universitaria obtuvo un promedio de 3,67. Esto respalda la pertinencia de explorar una solución de este tipo.

5. **Acceso gratuito:** la disposición a pagar por la aplicación obtuvo un promedio de 2,00. Esto indica una baja disposición a pagar y respalda la decisión de plantear Marketplace UCT como una plataforma gratuita.

6. **Frecuencia de uso esperada:** la frecuencia estimada de utilización obtuvo un promedio de 2,67. Aunque existe interés en la propuesta, no se puede afirmar que los participantes utilizarían la aplicación de manera frecuente. Por ello, resulta importante facilitar el acceso a las publicaciones y mantener una experiencia de navegación sencilla.

7. **Medios de pago:** la aceptación de distintos medios de pago obtuvo un promedio de 4,33. Esto refleja una valoración favorable hacia la flexibilidad en los pagos. Sin embargo, esta preferencia no significa que la aplicación ya implemente o procese pagos directamente.

### 4.3 Limitaciones de la investigación

Los resultados deben interpretarse considerando que la encuesta obtuvo solamente tres respuestas. Además, una de las respuestas dejó incompletas las primeras cuatro preguntas, por lo que estas cuentan con dos observaciones.

Por esta razón, los resultados representan una aproximación exploratoria a las preferencias y experiencias de los participantes, pero no permiten generalizar conclusiones a toda la comunidad universitaria.

La encuesta se utilizó como un antecedente para orientar las decisiones de diseño, no como una validación estadística definitiva de la necesidad o aceptación de la aplicación.

## 5. Decisiones de diseño

Las decisiones de diseño se relacionaron con las necesidades identificadas durante la investigación y con los principios de simplicidad, claridad y facilidad de navegación.

### 5.1 Pantalla de acceso

La primera pantalla corresponde al acceso a la aplicación.

Se incorporaron:

- Nombre de la aplicación.
- Campo para ingresar el nombre de usuario.
- Campo para ingresar la contraseña.
- Botón para iniciar sesión.
- Acceso a la pantalla de registro.

El objetivo es presentar de manera inmediata la función principal de la pantalla y evitar elementos innecesarios.

La distribución vertical permite que los elementos sean identificables fácilmente y mantiene una jerarquía visual clara.

### 5.2 Pantalla de registro

La pantalla de registro permite que nuevos usuarios creen una cuenta para acceder a la aplicación.

Se incorporaron:

- Título que identifica la creación de una cuenta.
- Campo para ingresar el nombre de usuario.
- Campo para ingresar la contraseña.
- Mensaje para informar errores o resultados del registro.
- Botón para registrar la cuenta.
- Acceso para regresar al inicio de sesión.

La estructura mantiene una distribución similar a la pantalla de acceso, favoreciendo la consistencia visual y facilitando la comprensión del proceso.

### 5.3 Pantalla principal

La pantalla principal funciona como un espacio de bienvenida y acceso a información personal del usuario.

Se incorporaron:

- Mensaje de bienvenida personalizado.
- Descripción breve de la plataforma.
- Sección de lista de deseos.
- Tarjetas para mostrar los productos guardados.

La lista de deseos permite que los usuarios mantengan organizados los productos que les interesan y puedan acceder a ellos desde la pantalla principal.

### 5.4 Pantalla del Marketplace

La pantalla del Marketplace permite explorar las publicaciones disponibles dentro de la aplicación.

Se incorporaron:

- Campo de búsqueda con icono de lupa.
- Sección de publicaciones recientes.
- Tarjetas para representar los productos disponibles.

Las publicaciones se presentan mediante tarjetas independientes para separar visualmente cada producto y facilitar su lectura.

Cada tarjeta permite mostrar información relevante, como:

- Nombre del producto.
- Precio.
- Imagen del producto.
- Información del vendedor.

Esta estructura permite que el usuario pueda revisar rápidamente diferentes publicaciones sin tener que entrar individualmente a cada una.

La incorporación de un buscador responde a la necesidad de facilitar el acceso a los productos publicados. Además, la presentación mediante tarjetas busca aprovechar la familiaridad que los participantes manifestaron tener con plataformas de compra y venta.

### 5.5 Pantalla de detalle del producto

La pantalla de detalle permite visualizar información más completa de una publicación seleccionada.

Se incorporaron:

- Nombre del producto.
- Imagen del producto.
- Precio.
- Descripción.
- Información del vendedor.
- Botón para contactar al vendedor mediante WhatsApp.
- Opción para agregar o quitar el producto de la lista de deseos.
- Opción para editar la publicación cuando pertenece al usuario.
- Botón para regresar a la pantalla anterior.

La organización de la información permite que el usuario conozca las características del producto antes de decidir si desea contactar al vendedor.

El contacto mediante WhatsApp facilita la comunicación entre los interesados sin necesidad de implementar un sistema de pagos dentro de la aplicación.

### 5.6 Pantalla de perfil

La pantalla de perfil permite representar la información básica del usuario y administrar sus publicaciones.

Se incorporaron:

- Imagen de perfil.
- Nombre del usuario.
- Sección de publicaciones propias.
- Acceso para iniciar la creación de una publicación.
- Acceso visual a opciones de configuración.

La separación entre el Marketplace y el perfil permite mantener una estructura de navegación sencilla y evita mezclar información personal con las publicaciones.

## 6. Estructura y navegación

La aplicación utiliza `ScreenManager` de Kivy para administrar las diferentes pantallas y permitir la navegación entre las secciones principales.

La estructura está compuesta por seis pantallas:

- **LoginScreen:** permite iniciar sesión.
- **RegistroScreen:** permite crear una cuenta.
- **PrincipalScreen:** presenta la pantalla principal y la lista de deseos.
- **MarketScreen:** permite explorar y buscar publicaciones.
- **ProductoScreen:** muestra el detalle de una publicación, incluyendo su imagen, precio, descripción y vendedor. También permite contactar al vendedor y administrar la lista de deseos.
- **PerfilScreen:** presenta la información del usuario y sus publicaciones, además de permitir iniciar el proceso de creación de una nueva publicación.

La navegación se complementa con una barra superior (`MDTopAppBar`), que proporciona acceso directo a la pantalla principal, al Marketplace y al perfil del usuario. También incorpora la opción de cerrar sesión.

El acceso a las pantallas de inicio de sesión y registro se realiza mediante sus respectivos botones. Desde el Marketplace se puede acceder al detalle de un producto y regresar a las publicaciones. Desde el perfil se puede iniciar la creación de nuevas publicaciones.

Esta organización busca mantener una navegación centralizada, facilitar el acceso a las funciones principales y evitar que el usuario tenga que recorrer múltiples pantallas para realizar acciones habituales.

## 7. Conclusión de la fundamentación UX/UI

El diseño de Marketplace UCT se orientó a ofrecer una experiencia sencilla, organizada y accesible para los integrantes de la comunidad universitaria.

Los resultados de la encuesta entregaron antecedentes favorables respecto al interés en comprar, vender e intercambiar productos dentro de un entorno universitario. También permitieron identificar aspectos relevantes, como la importancia del precio, la preferencia por una solución gratuita y la necesidad de facilitar la búsqueda y visualización de publicaciones.

A partir de estos antecedentes se definieron decisiones de diseño centradas en una navegación directa, una presentación clara de los productos y el acceso sencillo a las funciones principales.

Finalmente, debido al número reducido de respuestas, las decisiones se consideran fundamentadas en una investigación exploratoria. La experiencia de uso y la aceptación de la propuesta deberán seguir evaluándose mediante pruebas con una mayor cantidad de integrantes de la comunidad universitaria.
