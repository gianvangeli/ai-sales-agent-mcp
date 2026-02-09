from fastapi import APIRouter, HTTPException
from mcp.database import get_connection
from scripts.cart_repository import crear_carrito, agregar_item_al_carrito,obtener_carrito, actualizar_cantidad_item, eliminar_item_del_carrito



router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/{cart_id}")
def create_cart(cart_id: str):
    """
    Crea un carrito si no existe.
    El cart_id representa una conversacion o sesion

    Returns:
        dict: confirmacion de creacion.
    """

    conn = get_connection()
    crear_carrito(conn, cart_id)
    conn.close()

    return {"status": "ok", "cart_id": cart_id}



@router.post("/{cart_id}/items")
def add_item(cart_id: str, product_id: str, cantidad: int):
    """
    Agrega un producto al carrito.
    Si el producto exite, incrementa cantidad

    Returns:
        dict: confirmacion de operacion 
    """

    conn = get_connection()
    agregar_item_al_carrito(conn, cart_id, product_id,cantidad)
    conn.close()

    return {"status": "ok"}



@router.get("/{cart_id}")
def get_cart(cart_id: str):
    """
    Obtiene el estado completo del carrito.
    Returns:
        dict: carrito con items y total.
    """
    conn= get_connection()
    carrito = obtener_carrito(conn, cart_id)
    conn.close()

    return carrito


@router.put("/{cart_id:}/items/{product_id}")
def update_item(cart_id: str, product_id: str, cantidad: int):
    """
    Actualiza la cantidad de un producto en el carrito.
    Args:
        cart_id(str): ID del carrito
        product_id(str): ID del producto
        cantidad(int): Nueva cantidad
    
    Returns:
        dict: Confirmacion de actualizacion y estado actualizado del carrito.
    """

    if cantidad < 0:
        raise HTTPException(status_code=400, detail="La cantidad no puede ser negativa")
    
    conn = get_connection()
    actualizar_cantidad_item(conn, cart_id, product_id, cantidad)
    carrito = obtener_carrito(conn, cart_id)
    conn.close()

    return {"status":"ok", "cart": carrito}

@router.delete("/{cart_id}/items/{product_id}")
def delete_item(cart_id: str, product_id: str):
    """
    Elimina un producto del carrito.

    Args:
        cart_id(str): ID del carrito.
        product_id(str): ID del producto
    Returns:
        dict: Confirmacion de eliminacion y estado actualizado del carrito
    """

    conn = get_connection()
    eliminar_item_del_carrito(conn, cart_id, product_id)
    carrito = obtener_carrito(conn, cart_id)
    conn.close()

    return {"status": "ok", "cart": carrito}