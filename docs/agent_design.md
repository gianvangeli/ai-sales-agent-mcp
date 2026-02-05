# 1. Objetivo del Agente

El objetivo del agente de IA es asistir a un usuario en un proceso de compra, manteniendo una conversación natural y coherente, y delegando el acceso a datos y acciones de negocio a través de un Model Context Protocol (MCP).

## Rol dEl agente:

- Interpreta lenguaje natural

- Mantiene el contexto conversacional

- Decide dinámicamente cuándo consumir capacidades externas

- No contiene lógica de negocio hardcodeada

Este enfoque permite desacoplar la inteligencia conversacional del acceso a datos y facilita la escalabilidad del sistema.

# 2. Arquitectura General

El sistema está compuesto por los siguientes componentes:

Usuario (WhatsApp)
        ↓
Chatwoot (CRM)
        ↓
Agente de IA (Laburen)
        ↓
MCP (HTTP API)
        ↓
Base de Datos

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

| Método	| Endpoint	       | Descripción                                |

| GET	    | /products/search | Buscar productos por nombre o descripción  |
| GET	    | /products/{id}   | Obtener el detalle de un producto          |
| POST	    | /cart	           | Crear un carrito                           |
| GET	    | /cart/{id}	   | Obtener el contenido del carrito           |
| POST	    | /cart/items	   | Agregar un producto al carrito             |
| PUT	    | /cart/items/{id} | Actualizar cantidad o eliminar un ítem     |
| POST	    | /handoff	       | Derivar la conversación a un agente humano |

Cada endpoint representa una capacidad explícita del agente, siguiendo el principio de responsabilidad única.

# 5. Flujo de Interacción del Agente

## Exploración de Productos

Usuario expresa una necesidad
        ↓
Agente interpreta la intención
        ↓
Agente decide consultar datos externos
        ↓
Agente invoca MCP → /products/search
        ↓
API consulta la base de datos
        ↓
Agente presenta resultados y guía al usuario

## Mostrar Detalle de Producto

Usuario solicita más información
        ↓
Agente identifica el producto
        ↓
Agente invoca MCP → /products/{id}
        ↓
Agente presenta información detallada

## Creacion de carrito de Compras

Usuario expresa intención de compra
        ↓
Agente verifica si existe un carrito
        ↓
Agente crea el carrito si es necesario
        ↓
Agente agrega ítems → /cart/items
        ↓
Agente confirma el contenido del carrito

El agente agrega etiquetas en el CRM para reflejar los productos seleccionados por el usuario.

## Edición de Carrito

Usuario solicita modificar el carrito
        ↓
Agente interpreta la acción (editar o eliminar)
        ↓
Agente invoca MCP → /cart/items/{id}
        ↓
Agente confirma el nuevo estado del carrito


# 6. Derivación a Humano

Usuario solicita atención humana
        ↓
Agente invoca MCP → /handoff
        ↓
Se crea conversación en Chatwoot
        ↓
Se agregan etiquetas de contexto

Esta capacidad permite una transición controlada desde el agente automático a un operador humano.

# 7. Consideraciones de Diseño

- El agente no expone flujos rígidos ni menús

- Las decisiones se toman en tiempo real según la conversación

- El MCP actúa como contrato explícito entre el agente y el backend

- El diseño prioriza claridad, mantenibilidad y extensibilidad