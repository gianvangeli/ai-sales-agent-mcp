> Documento técnico – Fase Conceptual del Agente de IA

# 1. Objetivo del Agente

El objetivo del agente de IA es asistir a un usuario en un proceso de compra, manteniendo una conversación natural y coherente, y delegando el acceso a datos y acciones de negocio a través de un Model Context Protocol (MCP).

## Rol del agente:

- Interpreta lenguaje natural

- Mantiene el contexto conversacional

- Decide dinámicamente cuándo consumir capacidades externas

- No contiene lógica de negocio hardcodeada

Este enfoque permite desacoplar la inteligencia conversacional del acceso a datos y facilita la escalabilidad del sistema.

# 2. Arquitectura General

El sistema está compuesto por los siguientes componentes:

1. Usuario (WhatsApp)
2. Chatwoot (CRM)
3. Agente de IA (Laburen)
4. MCP (HTTP API)
5. Base de Datos

El agente de IA es el único consumidor del MCP.
El usuario final nunca interactúa directamente con la API.

# 3. Modelo de Datos

El modelo de datos implementa el esquema mínimo requerido:

## Tabla products

- id (PK)

- name

- description

- price

- stock

Los productos se importan desde un archivo products.xlsx provisto por la empresa y representan la fuente única de verdad del catálogo.

## Tabla carts

- id (PK)

- created_at

- updated_at

Existe un carrito por conversación, asociado al contexto del agente.

## Tabla cart_items

- id (PK)

- cart_id (FK)

- product_id (FK)

- qty

Permite representar múltiples productos dentro de un mismo carrito.

# 4. Endpoints MCP

El MCP expone un conjunto reducido y explícito de capacidades que el agente puede utilizar.

| Método | Endpoint               | Descripción                                      |
|--------|------------------------|--------------------------------------------------|
| GET    | /products/search       | Buscar productos por nombre o descripción        |
| GET    | /products/{id}         | Obtener el detalle de un producto                |
| POST   | /cart                  | Crear un carrito                                 |
| GET    | /cart/{id}             | Obtener el contenido del carrito                 |
| POST   | /cart/items            | Agregar un producto al carrito                   |
| PUT    | /cart/items/{id}       | Actualizar cantidad o eliminar un ítem           |
| POST   | /handoff               | Derivar la conversación a un agente humano       |


Cada endpoint representa una capacidad explícita del agente, siguiendo el principio de responsabilidad única.

# 5. Flujo de Interacción del Agente

## Exploración de Productos

1. El usuario expresa una necesidad
2. El agente interpreta la intención
3. El agente decide consultar datos externos
4. El agente invoca MCP → /products/search
5. API consulta la base de datos
6. El agente presenta resultados y guía al usuario

## Mostrar Detalle de Producto

1. El usuario solicita más información
2. El agente identifica el producto
3. El agente invoca MCP → /products/{id}
4. El agente presenta información detallada

## Creacion de carrito de Compras

1. El usuario expresa intención de compra
2. El agente verifica si existe un carrito
3. El agente crea el carrito si es necesario
4. El agente agrega ítems → /cart/items
5. El agente confirma el contenido del carrito

El agente agrega etiquetas en el CRM para reflejar los productos seleccionados por el usuario.

## Edición de Carrito

1. El usuario solicita modificar el carrito 
2. El agente interpreta la acción (editar o eliminar)
3. El agente invoca MCP → /cart/items/{id}
4. El agente confirma el nuevo estado del carrito


# 6. Derivación a Humano

1. El usuario solicita atención humana
2. El agente invoca MCP → /handoff
3. Se crea conversación en Chatwoot
4. Se agregan etiquetas de contexto

Esta capacidad permite una transición controlada desde el agente automático a un operador humano.

# 7. Consideraciones de Diseño

- El agente no expone flujos rígidos ni menús

- Las decisiones se toman en tiempo real según la conversación

- El MCP actúa como contrato explícito entre el agente y el backend

- El diseño prioriza claridad, mantenibilidad y extensibilidad

## Diagrama de flujo de interacción del agente

El siguiente diagrama de secuencia ilustra cómo el agente de IA interactúa con el usuario,
el CRM, el MCP y la base de datos durante el proceso de exploración de productos,
creación de carrito y edición del carrito.

Ver archivo: `diagrama_flujo_agente.puml`
