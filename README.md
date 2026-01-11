# Secure Enterprise Authentication System

A secure, enterprise-style authentication and user management system built in Python.

This project models **internal enterprise systems** where user accounts are
**provisioned by administrators**, not created via public signup.

There is intentionally **no free registration**.

---

## Project Intent

This system is designed to simulate how real organizations manage access:

- Employees are onboarded by IT / Admins
- Roles are assigned deliberately
- Accounts can be locked, suspended, or deleted
- Authentication enforces security invariants
- All critical actions are auditable

This is **not** a public consumer application.

---

## Key Features

- Role-based access control (Admin, Aux Admin, User)
- Secure password hashing (PBKDF2-HMAC-SHA256 with salt)
- Account lockout after repeated failed login attempts
- Session expiration and refresh tokens
- Audit logging for security-relevant events
- Clean separation of concerns
- CLI interface designed to be replaceable (web / GUI ready)
- Fully tested service layer using `pytest`

---

## Architecture Overview

The system follows a **layered architecture** with strict boundaries:

- **Domain layer**  
  Contains pure business objects and rules.  
  No persistence, no I/O, no framework code.

- **Service layer**  
  Implements business use cases and enforces invariants  
  (authentication, authorization, account lifecycle).

- **Repository layer**  
  Abstracts persistence behind interfaces.  
  Current implementation uses JSON storage.

- **Interface layer**  
  Provides a CLI for user interaction.  
  Contains no business logic and can be replaced without affecting the core.

This structure ensures the system is testable, maintainable, and extensible.

---

## Project Structure

