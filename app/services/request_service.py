"""
Serviu00e7o para gerenciamento de requisiu00e7u00f5es de anonimizau00e7u00e3o.

Este mu00f3dulo contu00e9m a classe RequestService que u00e9 responsu00e1vel por gerenciar
operau00e7u00f5es relacionadas u00e0s requisiu00e7u00f5es de anonimizau00e7u00e3o no sistema.
Implementa operau00e7u00f5es CRUD e consua para requisiu00e7u00f5es, incluindo a criação
de novas requisições e consulta de requisições existentes.

Classe:
    RequestService: Gerencia operau00e7u00f5es relacionadas u00e0s requisiu00e7u00f5es de anonimizau00e7u00e3o.

Funu00e7u00f5es:
    create_request: Cria uma nova solicitau00e7u00e3o de anonimizau00e7u00e3o.
    get_request_by_id: Obtu00e9m uma requisiu00e7u00e3o pelo ID.
    update_request: Atualiza uma requisiu00e7u00e3o existente.
    get_pending_requests: Obtu00e9m requisiu00e7u00f5es pendentes.
"""

from sqlalchemy.orm import Session
from app.models.models import Request
from app.models.schemas import RequestCreate
from datetime import datetime
from typing import Optional, List


class RequestService:
    """Serviu00e7o para gerenciamento de requisiu00e7u00f5es de anonimizau00e7u00e3o."""
    
    def __init__(self, db: Session):
        """Inicializa o serviu00e7o de requisiu00e7u00f5es.
        
        Args:
            db: Sessu00e3o do banco de dados
        """
        self.db = db
    
    def create_request(self, request_data: RequestCreate) -> Request:
        """Cria uma nova requisiu00e7u00e3o de anonimizau00e7u00e3o.
        
        Args:
            request_data: Dados da requisiu00e7u00e3o a ser criada
            
        Returns:
            Request: A requisiu00e7u00e3o criada
        """
        # Criar a solicitau00e7u00e3o no banco de dados
        new_request = Request(
            nm_system=request_data.nm_system,
            ct_payload={
                "id_person": request_data.id_person,
                "tp_document": request_data.tp_document
            },
            dt_register=datetime.now()
        )
        self.db.add(new_request)
        self.db.commit()
        self.db.refresh(new_request)
        return new_request
    
    def get_request_by_id(self, request_id: int) -> Optional[Request]:
        """Obtu00e9m uma requisiu00e7u00e3o pelo ID.
        
        Args:
            request_id: ID da requisiu00e7u00e3o a ser obtida
            
        Returns:
            Optional[Request]: A requisiu00e7u00e3o, se encontrada, ou None
        """
        return self.db.query(Request).filter(Request.id_request == request_id).first()
    
    def update_request(self, request: Request) -> Request:
        """Atualiza uma requisiu00e7u00e3o existente.
        
        Args:
            request: Objeto Request com os dados atualizados
            
        Returns:
            Request: A requisiu00e7u00e3o atualizada
        """
        self.db.commit()
        self.db.refresh(request)
        return request
    
    def get_pending_requests(self) -> List[Request]:
        """Obtu00e9m requisiu00e7u00f5es pendentes.
        
        Returns:
            List[Request]: Lista de requisiu00e7u00f5es pendentes
        """
        return self.db.query(Request).filter(Request.st_request == 0).all()