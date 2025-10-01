# IndicaVende - Lead Management System

## Overview
IndicaVende is a lead management application that facilitates collaboration between lead providers (indicadores), salespeople (vendedores), and managers (gestores).

## Architecture
- **Backend**: FastAPI (Python) running on port 8000
- **Frontend**: Streamlit running on port 5000
- **Database**: SQLite (indicavende.db)

## User Roles

### Indicador (Lead Provider)
- Create new leads
- Assign leads to vendedores
- View their submitted leads

### Vendedor (Salesperson)
- View assigned leads
- Update lead status (novo → em_contato → em_negociacao → fechado/perdido)
- Add observations to leads

### Gestor (Manager)
- View all leads
- View all users
- Access analytics and reports

## Test Users
The database has been seeded with the following test accounts:

| Email | Password | Role |
|-------|----------|------|
| admin@indicavende.me | admin123 | gestor |
| juliano@indicavende.me | seller123 | vendedor |
| daniela@indicavende.me | seller123 | vendedor |
| pedro@indicavende.me | indicator123 | indicador |

## Current State
- ✅ Backend API running successfully
- ✅ Frontend application running successfully
- ✅ Database seeded with test users
- ✅ Authentication flow working
- ✅ Role-based access control implemented
- ✅ All workflows configured and running

## Recent Changes
- 2025-10-01: Initial setup with FastAPI backend and Streamlit frontend
- 2025-10-01: Fixed access control issue - added /vendedores/ endpoint for indicadores to list available salespeople

## Known Limitations
- Authentication uses simple header-based authentication (X-User-Email). For production use, implement JWT tokens or session-based authentication.
