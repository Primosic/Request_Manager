#!/usr/bin/env python
"""
Inicializa o banco de dados com dados de teste para os testes funcionais.

Este script cria registros de teste no banco de dados para permitir a execuu00e7u00e3o
dos testes funcionais. Cria um sistema de teste, uma solicitau00e7u00e3o e os processos associados.
"""

from sqlalchemy.orm import Session
from app.db.database import get_db, engine, Base
from app.models.models import Request, DomSystem, Process
from app.services.system_service import SystemService
from app.services.request_service import RequestService
from app.services.process_service import ProcessService
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_test_data():
    """Inicializa o banco de dados com dados de teste."""
    # Garantir que as tabelas existem
    Base.metadata.create_all(bind=engine)
    
    db = next(get_db())
    
    try:
        # Verificar se existem sistemas de teste no banco
        system_service = SystemService(db)
        
        # Verificar sistema lab_a
        requester_system = system_service.get_system_by_name("lab_a")
        if not requester_system:
            # Verificar se existe algum sistema com id_dom_system = 1
            system_id_1 = db.query(DomSystem).filter(DomSystem.id_dom_system == 1).first()
            if system_id_1:
                logger.info(f"Ju00e1 existe um sistema com ID=1: {system_id_1.nm_system}")
                requester_system = system_id_1
            else:
                logger.info("Criando sistema de teste 'lab_a'...")
                requester_system = DomSystem(
                    nm_system="lab_a",
                    system_type="requester",
                    api_verify_address="http://localhost:8080/api/verify",
                    api_request_address="http://localhost:8080/api/request",
                    api_status_address="http://localhost:8080/api/status",
                    id_dom_system=1
                )
                db.add(requester_system)
                db.commit()
                db.refresh(requester_system)
        else:
            logger.info(f"Sistema 'lab_a' ju00e1 existe com ID: {requester_system.id_dom_system}")
        
        # Verificar sistema de processamento system_a
        process_system = system_service.get_system_by_name("system_a")
        if not process_system:
            # Verificar se existe algum sistema com id_dom_system = 2
            system_id_2 = db.query(DomSystem).filter(DomSystem.id_dom_system == 2).first()
            if system_id_2:
                logger.info(f"Ju00e1 existe um sistema com ID=2: {system_id_2.nm_system}")
                process_system = system_id_2
            else:
                logger.info("Criando sistema de processamento 'system_a'...")
                process_system = DomSystem(
                    nm_system="system_a",
                    system_type="process",
                    api_verify_address="http://localhost:8080/api/verify",
                    api_request_address="http://localhost:8080/api/request",
                    api_status_address="http://localhost:8080/api/status",
                    id_dom_system=2
                )
                db.add(process_system)
                db.commit()
                db.refresh(process_system)
        else:
            logger.info(f"Sistema 'system_a' ju00e1 existe com ID: {process_system.id_dom_system}")
        
        # Criar uma solicitau00e7u00e3o de teste (ID seru00e1 gerado automaticamente)
        request_service = RequestService(db)
        logger.info("Criando solicitau00e7u00e3o de teste com ID gerado automaticamente...")
        
        # Usar o serviu00e7o de requisiu00e7u00e3o para criar com valores corretos
        from app.models.schemas import RequestCreate
        request_data = RequestCreate(
            nm_system="lab_a",
            id_person="123456",
            tp_document="CC"
        )
        
        new_request = request_service.create_request(request_data)
        logger.info(f"Solicitau00e7u00e3o criada com ID: {new_request.id_request}")
        
        # Agora criar um processo para a solicitau00e7u00e3o que acabamos de criar
        logger.info(f"Criando processo para a solicitau00e7u00e3o {new_request.id_request} e sistema {process_system.id_dom_system}...")
        process_service = ProcessService(db)
        process = Process(
            id_request=new_request.id_request,
            id_system_process=process_system.id_dom_system,
            id_system_requester=requester_system.id_dom_system,
            dt_system_verify=datetime.now(),
            dt_system_verify_response=datetime.now(),
            id_person="123456",
            tp_document="CC",
            st_system_verify=1,  # Aprovado
            st_system_request=1  # Concluiu00edo
        )
        db.add(process)
        db.commit()
        db.refresh(process)
        
        # Salvar o ID da requisiu00e7u00e3o em um arquivo para uso nos testes funcionais
        with open("request_id.txt", "w") as f:
            f.write(str(new_request.id_request))
        
        logger.info("Dados de teste inicializados com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inicializar dados de teste: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_test_data()