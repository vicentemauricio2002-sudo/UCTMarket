# Fundamentación UX/UI — Marketplace UCT

## 1. Descripción del proyecto

**Marketplace UCT** es una aplicación orientada a la comunidad universitaria, cuyo objetivo es facilitar la compra, venta, intercambio y publicación de productos y servicios entre sus integrantes.

La propuesta busca centralizar este tipo de actividades en una plataforma enfocada en estudiantes y miembros de la comunidad universitaria, permitiendo visualizar publicaciones, buscar productos y acceder al perfil de los usuarios.

La interfaz fue desarrollada utilizando **Python, Kivy y KivyMD**, separando la lógica de programación de la interfaz mediante archivos `.py` y `.kv`.

## 2. Metodología UX/UI

Para el diseño de la aplicación se consideraron principios básicos de UX/UI y los resultados obtenidos durante el proceso de investigación realizado por el equipo.

El proceso se organizó en las siguientes etapas:

1. Identificación del problema.
2. Identificación del usuario objetivo.
3. Recopilación de información mediante investigación con usuarios.
4. Identificación de necesidades y hallazgos.
5. Definición de decisiones de diseño.
6. Elaboración de la interfaz.
7. Implementación del prototipo utilizando Kivy y KivyMD.
8. Revisión de la navegación y experiencia de usuario.

El objetivo fue diseñar una interfaz sencilla y fácil de comprender, reduciendo la cantidad de pasos necesarios para acceder a las funciones principales de la aplicación.

## 3. Usuario objetivo

El usuario principal de Marketplace UCT corresponde a integrantes de la comunidad universitaria, principalmente estudiantes interesados en comprar, vender, intercambiar u ofrecer productos y servicios.

Se consideraron características como:

- Uso frecuente de dispositivos móviles.
- Necesidad de acceder rápidamente a publicaciones.
- Interés por encontrar productos dentro de la comunidad universitaria.
- Necesidad de identificar al usuario que realiza una publicación.
- Preferencia por una navegación sencilla y directa.

## 4. Hallazgos de la investigación

A partir de la investigación realizada por el equipo se identificaron necesidades relacionadas con la compra, venta e intercambio de productos y servicios dentro de la comunidad universitaria.

Los principales hallazgos utilizados para orientar el diseño fueron:

| Hallazgo | Necesidad identificada | Decisión de diseño |
|---|---|---|
1. Cuando se le pregunto a los usuarios si estarían dispuestos a pagar por la app ninguno estuvo de acuerdo lo que significa que debe ser gratuita.
2. La mayoría de los usuarios ya tienen experiencia en usar apps de este tipo por lo  tanto no es necesario dar una explicación extensa de como funciona la app.
3. La mayoría esta de acuerdo en que se acepten todos los medios de pago existentes.
4. Los usuarios confirmaron que utilizarían esta app de manera regular, debemos encontrar una manera de hacer la app más llamativa para su uso.

## 5. Decisiones de diseño

La primera pantalla corresponde al acceso a la aplicación.

Se incorporaron:

- Nombre de la aplicación.
- Descripción breve.
- Campo para ingresar el nombre del usuario.
- Botón de ingreso.

El objetivo es presentar de manera inmediata la función principal de la pantalla y evitar elementos innecesarios.

La distribución vertical permite que los elementos sean identificables fácilmente y mantiene una jerarquía visual clara.

La pantalla principal representa el centro de la aplicación.

Se incorporaron los siguientes elementos:

- Barra superior con el nombre de Marketplace UCT.
- Campo de búsqueda.
- Sección de publicaciones recientes.
- Tarjetas para representar productos.
- Acceso al perfil del usuario.

Las publicaciones se presentan mediante tarjetas independientes para separar visualmente cada producto y facilitar su lectura.

Cada tarjeta muestra información básica como:

- Nombre del producto.
- Precio.
- Información del vendedor.

Esta estructura permite que el usuario pueda revisar rápidamente diferentes publicaciones sin tener que entrar individualmente a cada una.

La pantalla de perfil permite representar la información básica del usuario.

Se incorporaron:

- Identificación del usuario.
- Nombre.
- Sección de publicaciones.
- Botón para regresar al Marketplace.

La separación entre el Marketplace y el perfil permite mantener una estructura de navegación sencilla y evita mezclar información personal con las publicaciones.

## 6. Estructura y navegación

La aplicación utiliza `ScreenManager` de Kivy para administrar las diferentes pantallas.

La estructura propuesta es:

```text
LoginScreen
     │
     ▼
PrincipalScreen
     │
     ▼
PerfilScreen
     │
     └──────────► PrincipalScreen

```
