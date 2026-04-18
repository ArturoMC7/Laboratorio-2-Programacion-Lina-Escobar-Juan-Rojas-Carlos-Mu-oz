# 🧪 Laboratorio 2: Sistema de Supervisión de Contratos

## 📌 Información General

- **Curso:** Programación  
- **Periodo:** 2026-I  
- **Universidad:** Universidad del Quindío  
- **Estudiantes:** Juan Sebastian Rojas - Carlos Arturo Muñoz - Lina Marcela Escobar
- **Resultados de Aprendizaje:** RA1, RA2, RA3, RA4  

---

## 🎯 Objetivo del Laboratorio

Desarrollar la lógica del lado del servidor de un sistema de supervisión de contratos, implementando funcionalidades de autenticación, gestión de contratos, seguimiento contractual y generación de estadísticas, utilizando estructuras de datos y persistencia en archivos JSON.

---

## 🧩 Descripción del Sistema

El sistema permite a una organización gestionar contratos y realizar seguimiento estructurado sobre los mismos. Incluye:

- Registro y autenticación de usuarios con roles.
- Gestión de contratos.
- Registro de seguimientos contractuales.
- Cálculo de estadísticas generales.
- Exportación de información a archivos CSV.

La persistencia de datos se realiza mediante archivos JSON, lo que permite almacenar y recuperar información de forma estructurada.

---

## 🏗️ Arquitectura del Sistema

El sistema sigue una arquitectura modular:
server.py # Servidor principal (no modificable)
auth.py # Gestión de usuarios y autenticación
supervision.py # Lógica de contratos, seguimientos y estadísticas
supervision_client.py # Cliente (no modificable)
test_client.py # Pruebas automáticas


### 🔹 Separación de responsabilidades

- `auth.py` → Manejo de usuarios, sesiones y roles  
- `supervision.py` → Lógica del negocio (contratos, seguimientos, estadísticas)  
- `server.py` → Comunicación y exposición de endpoints  

---

## 💾 Persistencia de Datos

### 📁 users.json
Almacena los usuarios del sistema:

```json
{
  "users": [
    {
      "user": "admin1",
      "password": "adm",
      "role": "admin",
      "session": false
    }
  ]
}
📁 db.json

Almacena contratos y seguimientos:

{
  "contracts": [
    {
      "number": "C-1001",
      "contractor": "Ana Torres",
      "trackings": []
    }
  ]
}
