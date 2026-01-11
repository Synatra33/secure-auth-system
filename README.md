# Secure Enterprise Authentication System

A secure, enterprise-grade authentication and user management system built in Python.

This system is designed for **internal enterprise use**, where user accounts are
**provisioned by administrators**, not self-registered by the public.

## Features

- Role-based access control (Admin, Aux Admin, User)
- Secure password hashing (PBKDF2-HMAC-SHA256)
- Account lockout after repeated failed logins
- Session expiration with refresh tokens
- Audit logging for security events
- Clean separation of domain, services, repositories, and interfaces
- Fully tested service layer (pytest)

## Architecture Overview

- **Domain**: Core entities (User, Role, Identity, AuditEvent)
- **Repositories**: Persistence abstractions and JSON implementation
- **Services**: Authentication and user management logic
- **Interfaces**: CLI interface (thin, replaceable)
- **Tests**: Service-level tests with fake repositories

## Usage (Development)

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install pytest
