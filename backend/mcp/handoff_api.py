from fastapi import APIRouter
from pydantic import BaseModel, Field

from mcp.database import get_connection
from scripts.handoff_repository import registrar_handoff

router = APIRouter(prefix="/handoff", tags=["handoff"])

class HandoffRequest(BaseModel):
    """
    Payload de solicitud de derivacion a humano.
    cart_id: representa la conversacion o carrito asociado.
    motivo: razon concreta de la derivacion.
    contexto: resumen util para el humano
    """
    cart_id: str = Field(..., description="ID del carrito/conversacion")
    motivo: str = Field(..., min_length=3, description="Motivo de la derivacion")
    contexto: str | None = Field(default=None, description="Contexto adicional para el agente humano")


@router.post("")
def create_handoff(payload: HandoffRequest) -> dict:
    """
   Crea un registro de derivacion a humano.
   En esta etapa NO se registra con Chatwoot, pero queda listo para el agente.
   - dispare la accion sin errores
   - guarde el contexto
   - obtenga un handoff_id

   Returns:
        dict: confirmacion y handoff_id generado.
    """

    conn = get_connection()
    handoff_id = registrar_handoff(conn, payload.cart_id, payload.motivo, payload.contexto)
    conn.close()

    return {
        "status": "ok",
        "handoff_id": handoff_id
    }

