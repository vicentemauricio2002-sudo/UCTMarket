# Uso de Inteligencia Artificial en UCTMarket

## 1. IA utilizada

Durante el desarrollo de UCTMarket se utilizó inteligencia artificial como herramienta de apoyo para la planificación, programación, resolución de problemas técnicos, generación de datos de prueba y evaluación de la aplicación.

Las principales herramientas utilizadas fueron:

- **ChatGPT:** utilizado como asistente para comprender conceptos de programación, revisar fragmentos de código, resolver errores de frontend, orientar la organización del proyecto y apoyar la elaboración de escenarios de prueba y métricas de evaluación.
- **Otras herramientas de inteligencia artificial:** se utilizaron como apoyo complementario para contrastar algunas soluciones y obtener distintas perspectivas durante el desarrollo.

La inteligencia artificial no reemplazó el trabajo de programación ni las decisiones del desarrollador. Sus respuestas fueron revisadas y adaptadas a las necesidades del proyecto.

## 2. Prompts

Durante el desarrollo se realizaron consultas relacionadas con distintas áreas del proyecto. A continuación, se describen las principales solicitudes realizadas a la inteligencia artificial.

- **Diseño y desarrollo de la interfaz:** se pidió orientación para mejorar la distribución visual de las pantallas, organizar los componentes de KivyMD y conseguir una apariencia más adecuada para una aplicación de escritorio, utilizando una barra de navegación superior.

- **Resolución de errores de frontend:** se solicitaron explicaciones y alternativas para solucionar problemas relacionados con la estructura de los archivos KV, la navegación entre pantallas, los espacios visuales, el desplazamiento de contenido y la utilización de componentes de KivyMD 2.0.0.

- **Implementación de funcionalidades:** se pidió apoyo para comprender e implementar funcionalidades como la edición y eliminación de publicaciones, la lista de deseos y el contacto con vendedores mediante enlaces de WhatsApp con mensajes predefinidos.

- **Generación de datos ficticios:** se solicitó diseñar un conjunto de usuarios y publicaciones de prueba para representar situaciones de uso del marketplace, manteniendo una estructura compatible con los archivos JSON existentes.

- **Diseño de pruebas y métricas:** se pidió ayuda para definir escenarios de prueba, identificar eventos importantes de interacción y establecer KPI que permitieran evaluar el funcionamiento de UCTMarket.

- **Desarrollo del sistema de analítica:** se solicitó orientación para registrar eventos en JSON, procesarlos mediante Python y generar gráficos estadísticos que facilitaran la interpretación de los resultados.

- **Documentación del proyecto:** se pidió apoyo para estructurar y mejorar el README, describir la arquitectura del proyecto y documentar el uso de inteligencia artificial.

## 3. Respuesta de IA

A partir de las solicitudes anteriores, la inteligencia artificial entregó explicaciones, sugerencias, ejemplos de código y propuestas que fueron utilizadas como referencia durante el desarrollo.

- **Diseño y desarrollo de la interfaz:** la IA propuso distintas alternativas de distribución visual y utilización de componentes de KivyMD. También explicó cómo personalizar colores, botones, iconos, tarjetas y elementos de navegación.

- **Resolución de errores de frontend:** proporcionó explicaciones sobre posibles causas de errores en la estructura KV y en la organización de los componentes. Además, sugirió modificaciones para mejorar el desplazamiento de las pantallas y corregir problemas de presentación.

- **Implementación de funcionalidades:** entregó ejemplos y explicaciones para gestionar publicaciones, actualizar la lista de deseos y abrir enlaces de WhatsApp desde la aplicación.

- **Generación de datos ficticios:** propuso registros sintéticos de usuarios, publicaciones y eventos de interacción. Se consideraron identificadores UUID y números de contacto ficticios para evitar utilizar información personal real.

- **Diseño de pruebas y métricas:** propuso escenarios de evaluación y KPI relacionados con las búsquedas, publicaciones, interés en productos, registros y listas de deseos.

- **Desarrollo del sistema de analítica:** proporcionó orientación para implementar el registro de eventos, almacenar marcas de tiempo, procesar los datos mediante Python y representar los resultados utilizando Matplotlib.

- **Documentación del proyecto:** ayudó a organizar la información técnica y redactar explicaciones sobre las funcionalidades, arquitectura, instalación y tecnologías utilizadas.

## 4. Ajustes realizados

Las respuestas entregadas por la inteligencia artificial no se incorporaron automáticamente. Se revisaron, probaron y modificaron según la estructura, las tecnologías y los objetivos de UCTMarket.

- **Compatibilidad con KivyMD:** algunas sugerencias iniciales utilizaban componentes o propiedades que no correspondían a la versión 2.0.0 utilizada en el proyecto. Se corrigieron las propuestas para trabajar con los componentes actuales, como `MDButton`, `MDButtonText` y `MDTextFieldHintText`.

- **Correcciones de frontend:** las soluciones propuestas para la distribución de componentes, navegación y desplazamiento fueron probadas dentro de la aplicación. Se realizaron ajustes adicionales hasta obtener un comportamiento visual y funcional adecuado.

- **Adaptación de las funcionalidades:** los ejemplos de código se modificaron para respetar la arquitectura existente y los servicios de persistencia JSON del proyecto. En particular, el contacto mediante WhatsApp se planteó como una forma de comunicar al comprador con el vendedor, sin implementar un sistema de pagos o transacciones dentro de la aplicación.

- **Datos sintéticos:** se utilizaron identificadores de productos existentes en `productos.json` para mantener la coherencia entre las publicaciones y los eventos de analítica. Los números de WhatsApp incluidos en los datos ficticios fueron reemplazados por números de prueba.

- **Ajuste de KPI:** se revisaron las fórmulas y cantidades utilizadas en los escenarios sintéticos para asegurar que los resultados fueran coherentes con los eventos que realmente registra la aplicación. También se distinguió entre interacciones e indicadores de ventas, ya que presionar el botón de contacto no significa que se haya concretado una compra.

- **Revisión de la analítica:** se comprobó que los eventos registrados correspondieran a funcionalidades existentes en el código. Se ajustaron los scripts de análisis y generación de gráficos para trabajar con la estructura real de los archivos JSON.

- **Organización y documentación:** se revisaron las descripciones de los archivos, las instrucciones de instalación y las dependencias para que la documentación representara la versión actual del proyecto.

## 5. Reflexión acerca del uso de IA

La utilización de inteligencia artificial fue un apoyo importante durante el desarrollo de UCTMarket, especialmente para comprender conceptos, resolver errores y explorar alternativas de implementación.

Uno de los principales beneficios fue poder recibir explicaciones sobre problemas técnicos que, de otra manera, habrían requerido más tiempo de investigación. También permitió explorar distintas soluciones de diseño y organizar el proceso de evaluación mediante escenarios de prueba y métricas.

Sin embargo, se comprobó que las respuestas de la inteligencia artificial no siempre eran compatibles con la versión de las bibliotecas utilizadas o con la estructura específica del proyecto. Por este motivo, fue necesario revisar las sugerencias, contrastarlas con el código existente y realizar pruebas antes de incorporarlas.

En cuanto a la evaluación, los datos sintéticos permitieron representar distintas situaciones de uso y calcular indicadores de funcionamiento sin presentar resultados ficticios como si fueran mediciones de usuarios reales. Estos datos fueron utilizados como escenario simulado de evaluación, con autorización del docente.

Finalmente, el uso de inteligencia artificial permitió complementar el aprendizaje y facilitar el desarrollo, pero también hizo necesario mantener una actitud crítica frente a sus respuestas. La responsabilidad de comprender, verificar, adaptar y decidir qué soluciones incorporar permaneció en el desarrollador.
