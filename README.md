# 🔐 Auth Microservice (Django + gRPC)

A **production-ready Authentication Microservice** built with **Django + gRPC**, designed for **microservice architectures**.  
This service is the **single source of truth for authentication and authorization** and integrates cleanly with other services using **gRPC**, **JWT**, and **event-driven patterns**.

---

## 📌 Responsibilities

✅ User authentication (login / signup)  
✅ Google OAuth login  
✅ JWT access & refresh token issuing  
✅ Token validation for other services  
✅ Authorization (roles / permissions)  
✅ Auth-related events publishing (Kafka-ready)  

> ❌ This service does **not** contain business logic of other services

---

## 🏗️ Architecture Overview

```text
Frontend
  ↓ (credentials / Google ID token)
Auth Microservice (Django + gRPC)
  ├─ Verifies identity
  ├─ Issues JWT
  └─ Publishes auth events
        ↓
Other Microservices (Task, User, etc.)
  └─ Validate JWT via interceptor
