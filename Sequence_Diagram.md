# Diagramas de Sequu00eancia do Request Manager

Este documento apresenta os diagramas de sequu00eancia que ilustram o funcionamento das principais APIs do sistema Request Manager. Os diagramas mostram as interau00e7u00f5es entre os clientes, endpoints da API, serviu00e7os, e o banco de dados.

## u00cdndice

1. [Criau00e7u00e3o de Requisiu00e7u00e3o](#1-criau00e7u00e3o-de-requisiu00e7u00e3o)
2. [Verificau00e7u00e3o de Identidade](#2-verificau00e7u00e3o-de-identidade)
3. [Atualizau00e7u00e3o de Status de Processamento](#3-atualizau00e7u00e3o-de-status-de-processamento)
4. [Consulta de Status](#4-consulta-de-status)

## 1. Criau00e7u00e3o de Requisiu00e7u00e3o

```mermaid
sequenceDiagram
    participant C as Cliente
    participant AR as API (request_router)
    participant RS as RequestService
    participant SS as SystemService
    participant PS as ProcessService
    participant DB as Banco de Dados

    C->>AR: POST /api/request (RequestCreate)
    Note over C,AR: Payload: nm_system, id_person, tp_document
    
    AR->>SS: get_system_by_name(nm_system)
    SS->>DB: Query tb_dom_system
    DB-->>SS: Dados do sistema
    SS-->>AR: DomSystem
    
    AR->>RS: create_request(request_data)
    RS->>DB: Insert em tb_request
    DB-->>RS: id_request
    RS-->>AR: Request
    
    AR->>SS: get_processing_systems()
    SS->>DB: Query tb_dom_system (type=process)
    DB-->>SS: Lista de sistemas de processamento
    SS-->>AR: List[DomSystem]
    
    loop Para cada sistema de processamento
        AR->>PS: create_process_entry(id_request, id_system, id_person, tp_document)
        PS->>DB: Insert em tb_process
        DB-->>PS: OK
        PS-->>AR: Process
    end
    
    AR-->>C: Response (201 Created)
    Note over AR,C: id_request
```

## 2. Verificau00e7u00e3o de Identidade

```mermaid
sequenceDiagram
    participant C as Cliente
    participant AV as API (verify_router)
    participant PS as ProcessService
    participant NS as NotificationService
    participant DB as Banco de Dados

    C->>AV: POST /api/verify (VerificationRequest)
    Note over C,AV: Payload: id_request, id_system_process, st_system_verify, ds_reason_verify_refuse
    
    AV->>PS: get_process(id_request, id_system_process)
    PS->>DB: Query tb_process
    DB-->>PS: Process
    PS-->>AV: Process
    
    AV->>PS: update_verification_status(id_request, id_system_process, st_system_verify, ds_reason_verify_refuse)
    PS->>DB: Update tb_process
    DB-->>PS: OK
    PS-->>AV: True
    
    alt Se verificau00e7u00e3o aprovada
        AV->>NS: notify_verification_approved(id_request, id_system_process)
        NS-->>AV: OK
    else Se verificau00e7u00e3o rejeitada
        AV->>NS: notify_verification_rejected(id_request, id_system_process, reason)
        NS-->>AV: OK
    end
    
    AV-->>C: Response (200 OK)
```

## 3. Atualizau00e7u00e3o de Status de Processamento

```mermaid
sequenceDiagram
    participant C as Cliente
    participant AR as API (request_router)
    participant PS as ProcessService
    participant NS as NotificationService
    participant DB as Banco de Dados

    C->>AR: POST /api/request/status (RequestStatusUpdate)
    Note over C,AR: Payload: id_request, id_system_process, st_system_request
    
    AR->>PS: get_process(id_request, id_system_process)
    PS->>DB: Query tb_process
    DB-->>PS: Process
    PS-->>AR: Process
    
    AR->>PS: update_processing_status(id_request, id_system_process, st_system_request)
    PS->>DB: Update tb_process
    DB-->>PS: OK
    PS-->>AR: True
    
    alt Se processamento concluu00eddo
        AR->>NS: notify_processing_completed(id_request, id_system_process)
        NS-->>AR: OK
    else Se processamento com erro
        AR->>NS: notify_processing_error(id_request, id_system_process)
        NS-->>AR: OK
    end
    
    AR-->>C: Response (200 OK)
```

## 4. Consulta de Status

```mermaid
sequenceDiagram
    participant C as Cliente
    participant AS as API (status_router)
    participant SS as StatusService
    participant PS as ProcessService
    participant DB as Banco de Dados

    C->>AS: GET /api/request/{id_request}/status
    
    AS->>SS: get_request_status(id_request)
    
    SS->>DB: Query tb_request
    DB-->>SS: Request
    
    SS->>PS: get_processes_for_request(id_request)
    PS->>DB: Query tb_process
    DB-->>PS: List[Process]
    PS-->>SS: List[Process]
    
    loop Para cada processo
        SS->>PS: get_latest_progress(id_request, id_system_process)
        PS->>DB: Query tb_process_progress
        DB-->>PS: ProcessProgress
        PS-->>SS: ProcessProgress
    end
    
    SS-->>AS: StatusResponse
    
    AS-->>C: Response (200 OK)
    Note over AS,C: Dados consolidados do status
```

## Notas Adicionais

1. Os diagramas assumem que todas as validau00e7u00f5es necessu00e1rias su00e3o realizadas em cada etapa, e apenas os fluxos de sucesso su00e3o representados em detalhes.

2. Tratamento de erros:
   - Solicitau00e7u00f5es invu00e1lidas retornam cu00f3digo HTTP 400 (Bad Request)
   - Recursos nu00e3o encontrados retornam cu00f3digo HTTP 404 (Not Found)
   - Erros internos retornam cu00f3digo HTTP 500 (Internal Server Error)

3. Autenticau00e7u00e3o nu00e3o estu00e1 representada nos diagramas, mas assume-se que todas as requisiu00e7u00f5es su00e3o validadas pelo middleware de autenticau00e7u00e3o antes de alcanu00e7arem os endpoints.