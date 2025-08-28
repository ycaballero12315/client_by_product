# 🧠 Proyecto Backend FastAPI + JWT + MongoDB + Docker + AWS

---

## 📋 Introducción

Este proyecto representa una **arquitectura backend moderna, segura y escalable**, desarrollada con **FastAPI**, **MongoDB Atlas**, **JWT para autenticación**, y desplegada en **Docker sobre EC2**. El objetivo fue construir una **API RESTful robusta, documentada, protegida y lista para producción**.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
| --- | --- |
| **Backend** | FastAPI + Pydantic |
| **Base de datos** | MongoDB Atlas |
| **Autenticación** | JWT (OAuth2 PasswordBearer) |
| **Contenedores** | Docker + docker-compose |
| **Cloud** | AWS EC2 |
| **Proxy inverso** | Nginx |
| **Documentación** | Swagger UI (eliminado en producción) |
| **Frontend** | Página personalizada para pruebas |

---

## 🔗 Arquitectura de Endpoints

### 🔐 **Autenticación** (`/loginJWT`)

| Método | Ruta | Descripción |
| --- | --- | --- |
| `POST` | `/loginJWT/` | Login y obtención de token JWT |
| `GET` | `/loginJWT/users/me` | Usuario autenticado actual |

### 👤 **Gestión de Usuarios** (`/user`)

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/user/` | Listar usuarios |
| `GET` | `/user/users/{id}` | Obtener usuario por ID |
| `PUT` | `/user/users/{id}` | Actualizar usuario |
| `DELETE` | `/user/users/{id}` | Eliminar usuario |

### 📦 **Gestión de Productos** (`/product`)

| Método | Ruta | Descripción |
| --- | --- | --- |
| `GET` | `/product/` | Listar productos |
| `GET` | `/product/{id}` | Obtener producto por ID |
| `GET` | `/product/products/` | Obtener todos los productos |
| `POST` | `/product/` | Crear nuevo producto |

---

## 🔒 Seguridad y Blindaje Implementado

- ✅ **Autenticación JWT** con expiración y validación robusta
- ✅ **Protección de rutas** con `Depends(get_current_user)`
- ✅ **Eliminación de Swagger UI** en producción por seguridad
- ✅ **Configuración de .gitignore** para archivos sensibles
- ✅ **Health checks** en Docker para alta disponibilidad
- ✅ **Nginx como proxy inverso** con redirección optimizada

---

## 🎨 Interfaz de Pruebas Personalizada

Se desarrolló una **página web personalizada** para reemplazar Swagger UI en producción, que permite:

- 🔑 **Autenticación** y obtención de tokens JWT
- 📊 **CRUD completo** de productos y usuarios
- 📱 **Visualización en tiempo real** de respuestas y errores
- 🎯 **Interfaz intuitiva** y profesional

---

## ☁️ Despliegue en AWS EC2

### Arquitectura de Despliegue

- 🐳 **Contenedores Docker** orquestados con `docker-compose`
- 🌐 **MongoDB Atlas** como base de datos en la nube
- 🔄 **Nginx** sirviendo frontend y proxy al backend
- 📊 **Logs centralizados** para monitoreo y troubleshooting
- 💾 **Volúmenes persistentes** y rutas optimizadas

### Configuración Docker

```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - mongo
      
  mongo:
    image: mongo
    volumes:
      - mongo_data:/data/db
      
volumes:
  mongo_data:
```

<style>
pre {
  background-color: #1a1a1a !important;
  color: #f8f8f2 !important;
  border: 1px solid #333 !important;
  border-radius: 6px !important;
  padding: 16px !important;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
}

code {
  background-color: #1a1a1a !important;
  color: #f8f8f2 !important;
  padding: 2px 4px !important;
  border-radius: 3px !important;
}
</style>

---

## 🚀 Roadmap - Próximos Pasos

### 🔒 **Integración SSL/HTTPS**
- Certificado gratuito con **Let's Encrypt**
- Configuración Nginx para **HTTPS**
- Redirección automática HTTP → HTTPS

### 🎨 **Desarrollo Frontend en Python**

| Framework | Características | Ventajas |
| --- | --- | --- |
| **Anvil** | Fullstack visual | Integración directa con backend |
| **NiceGUI** | Declarativo sobre FastAPI | Ideal para dashboards |
| **Streamlit** | Apps interactivas | Prototipado rápido |
| **PyScript** | Python en navegador | Sin dependencia de backend |

---

## 📚 Lecciones Aprendidas

- 📖 **Documentación automática** útil en desarrollo, no profesional en producción
- 🛡️ **Blindaje desde el inicio** previene errores futuros
- 📊 **Trazabilidad y código limpio** son clave para escalabilidad
- ⚙️ **Automatización de despliegues** reduce riesgo operativo
- 🔧 **Integración Nginx-FastAPI** requiere atención especial en routing

---

## 🏆 Conclusión

Este proyecto consolida **buenas prácticas backend profesionales**: seguridad robusta, trazabilidad completa, despliegue eficiente y documentación clara. 

**Aspectos destacados:**
- ✨ Migración de Swagger a interfaz propia
- 🔐 Implementación completa de JWT
- ☁️ Preparación para HTTPS y producción
- 🎯 Enfoque profesional y orientado a escalabilidad

---

## 📂 Repositorio del Proyecto

🔗 **GitHub:** [https://github.com/ycaballero12315/client_by_product.git](https://github.com/ycaballero12315/client_by_product.git)

### 📁 **Incluye:**
- 🏗️ Estructura modular del backend
- 🚀 Scripts de despliegue y configuración
- 📖 Documentación técnica completa
- 🧪 Ejemplos de uso y pruebas locales

---

*Proyecto desarrollado con pasión con arquitectura de software moderna y las mejores prácticas de desarrollo.*
