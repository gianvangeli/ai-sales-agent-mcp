# AI Sales Agent – MCP Backend

Este repositorio implementa el **Model Context Protocol (MCP)** para un agente de IA capaz de asistir a usuarios en un proceso de compra mediante una conversación natural.

El proyecto forma parte del **Desafío Técnico – AI Engineer para Laburen.com** y cubre tanto la **fase conceptual** como la **fase práctica (backend)**.

---

## Objetivo

Diseñar e implementar un backend que permita a un **agente de IA**:

- Explorar productos
- Mostrar detalles de productos
- Crear y gestionar un carrito de compras
- Editar el carrito (extra)
- Derivar la conversación a un agente humano

El agente **no contiene lógica de negocio**, sino que consume capacidades explícitas a través de un MCP HTTP.

---

## Arquitectura General
Usuario (WhatsApp)
↓
Chatwoot (CRM)
↓
Agente de IA (Laburen)
↓
MCP (FastAPI - HTTP API)
↓
Base de Datos (SQLite)

- El **agente de IA** interpreta la intención del usuario.
- El **MCP** actúa como contrato explícito entre el agente y el backend.
- La **base de datos** almacena productos y carritos.

---

## Estructura del Proyecto
ai-sales-agent-mcp/
│
├── backend/
│ ├── mcp/ # API MCP (FastAPI)
│ │ ├── main.py
│ │ ├── products_api.py
│ │ └── cart_api.py
│ │
│ ├── scripts/ # Lógica de negocio y persistencia
│ │ ├── product_repository.py
│ │ ├── cart_repository.py
│ │ ├── excel_loader.py
│ │ ├── product_mapper.py
│ │ └── import_products.py
│ │
│ ├── database/
│ │ └── database.sqlite
│ │
│ └── products.xlsx
│
├── docs/
│ ├── agent_design.md
│ └── diagrama_flujo_agente.puml
│
└── README.md

## Modelo de Datos

### products
- id (PK)
- nombre
- descripcion
- categoria
- color
- talle
- precio
- stock
- disponible

### carts
- id (PK)
- created_at
- updated_at

### cart_items
- id (PK)
- cart_id (FK)
- product_id (FK)
- qty

---

## Endpoints MCP

### Productos
- `GET /products/search`  
  Busca productos con filtros dinámicos (nombre, color, talle, categoría).

- `GET /products/{id}`  
  Devuelve el detalle de un producto específico.

### Carrito
- `POST /cart/{cart_id}`  
  Crea un carrito (un carrito por conversación).

- `GET /cart/{cart_id}`  
  Obtiene el estado actual del carrito.

- `POST /cart/{cart_id}/items`  
  Agrega productos al carrito.

- `PUT /cart/{cart_id}/items/{product_id}`  
  Actualiza cantidad o elimina un ítem.





## Cómo ejecutar el proyecto localmente

### 1. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate