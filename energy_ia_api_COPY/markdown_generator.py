#!/usr/bin/env python3
"""
📝 GENERADOR DE DOCUMENTACIÓN MARKDOWN SMARWATT
===============================================

Genera documentación en formato Markdown automáticamente.
SIN TOCAR código fuente, perfecto para README y wikis.

CARACTERÍSTICAS:
- Documentación Markdown completa
- Lista todos los endpoints organizados
- Incluye ejemplos de uso
- Compatible con GitHub/GitLab wikis

USO:
python markdown_generator.py

VERSIÓN: 1.0.0
"""

import os
import re
from typing import Dict, List
from auto_doc_generator import SmarWattDocGenerator


class MarkdownDocGenerator(SmarWattDocGenerator):
    """Generador de documentación Markdown"""

    def generate_markdown_docs(self, energy_api_path: str, expert_api_path: str) -> str:
        """Genera documentación completa en Markdown"""

        # Analizar microservicios
        energy_routes = self.analyze_microservice(energy_api_path, "Energy IA API")
        expert_routes = self.analyze_microservice(expert_api_path, "Expert Bot API")

        # Generar Markdown
        markdown = self._generate_header()
        markdown += self._generate_overview(energy_routes, expert_routes)
        markdown += self._generate_energy_api_docs(energy_routes)
        markdown += self._generate_expert_api_docs(expert_routes)
        markdown += self._generate_authentication()
        markdown += self._generate_examples()

        return markdown

    def _generate_header(self) -> str:
        """Genera encabezado del documento"""
        return """# 🚀 SmarWatt Microservices API Documentation

## 📋 Tabla de Contenidos

- [📖 Resumen General](#resumen-general)
- [🔋 Energy IA API](#energy-ia-api)
- [🤖 Expert Bot API](#expert-bot-api)
- [🔐 Autenticación](#autenticación)
- [💡 Ejemplos de Uso](#ejemplos-de-uso)

---

"""

    def _generate_overview(self, energy_routes: List, expert_routes: List) -> str:
        """Genera resumen general"""
        return f"""## 📖 Resumen General

SmarWatt cuenta con **2 microservicios** independientes que trabajan en conjunto:

| Microservicio | Endpoints | Descripción |
|---------------|-----------|-------------|
| **Energy IA API** | {len(energy_routes)} | Chatbot inteligente y análisis energético |
| **Expert Bot API** | {len(expert_routes)} | Recomendaciones avanzadas y datos empresariales |
| **TOTAL** | **{len(energy_routes) + len(expert_routes)}** | Conjunto completo de APIs |

### 🏗️ Arquitectura

```
┌─────────────────┐    HTTP    ┌──────────────────┐
│  Energy IA API  │ ◄────────► │ Expert Bot API   │
│  (Puerto 5000)  │            │  (Puerto 5001)   │
└─────────────────┘            └──────────────────┘
         │                               │
         ▼                               ▼
    ┌─────────┐                  ┌─────────────┐
    │ Gemini  │                  │  BigQuery   │
    │   AI    │                  │ Analytics   │
    └─────────┘                  └─────────────┘
```

---

"""

    def _generate_energy_api_docs(self, routes: List) -> str:
        """Genera documentación del Energy IA API"""
        markdown = """## 🔋 Energy IA API

**Descripción**: Servicio principal de chatbot inteligente con IA avanzada.  
**Puerto**: 5000  
**Base URL**: `http://localhost:5000`

### 📌 Endpoints Disponibles

"""

        # Agrupar por categorías
        categories = self._categorize_routes(routes)

        for category, category_routes in categories.items():
            markdown += f"#### {category}\n\n"

            for route in category_routes:
                methods_str = " | ".join(route["methods"])
                markdown += f"- **`{methods_str} {route['path']}`**\n"
                markdown += f"  - {route['description'][:100]}...\n"
                markdown += f"  - Función: `{route['function']}`\n\n"

        return markdown + "\n---\n\n"

    def _generate_expert_api_docs(self, routes: List) -> str:
        """Genera documentación del Expert Bot API"""
        markdown = """## 🤖 Expert Bot API

**Descripción**: Servicio especializado en análisis avanzado y recomendaciones.  
**Puerto**: 5001  
**Base URL**: `http://localhost:5001`

### 📌 Endpoints Disponibles

"""

        # Agrupar por categorías
        categories = self._categorize_routes(routes)

        for category, category_routes in categories.items():
            markdown += f"#### {category}\n\n"

            for route in category_routes:
                methods_str = " | ".join(route["methods"])
                markdown += f"- **`{methods_str} {route['path']}`**\n"
                markdown += f"  - {route['description'][:100]}...\n"
                markdown += f"  - Función: `{route['function']}`\n\n"

        return markdown + "\n---\n\n"

    def _categorize_routes(self, routes: List) -> Dict[str, List]:
        """Categoriza rutas por función"""
        categories = {
            "🤖 Chatbot": [],
            "👤 Usuarios": [],
            "📊 Análisis": [],
            "🔗 Enlaces": [],
            "⚡ Energía": [],
            "🔧 Administración": [],
            "📈 Métricas": [],
            "🔄 Otros": [],
        }

        for route in routes:
            path_lower = route["path"].lower()
            func_lower = route["function"].lower()

            if any(word in path_lower for word in ["chat", "message", "conversation"]):
                categories["🤖 Chatbot"].append(route)
            elif any(word in path_lower for word in ["user", "profile"]):
                categories["👤 Usuarios"].append(route)
            elif any(
                word in path_lower for word in ["analysis", "sentiment", "recommend"]
            ):
                categories["📊 Análisis"].append(route)
            elif any(word in path_lower for word in ["link", "url"]):
                categories["� Enlaces"].append(route)
            elif any(
                word in path_lower for word in ["energy", "tariff", "consumption"]
            ):
                categories["⚡ Energía"].append(route)
            elif any(word in path_lower for word in ["admin", "manage"]):
                categories["� Administración"].append(route)
            elif any(word in path_lower for word in ["metric", "health", "status"]):
                categories["📈 Métricas"].append(route)
            else:
                categories["� Otros"].append(route)

        # Filtrar categorías vacías
        return {k: v for k, v in categories.items() if v}

    def _generate_authentication(self) -> str:
        """Genera sección de autenticación"""
        return """## 🔐 Autenticación

Todos los endpoints (excepto health checks) requieren autenticación JWT de Firebase.

### Formato del Token

```http
Authorization: Bearer <firebase-jwt-token>
```

### Ejemplo

```bash
curl -X GET "http://localhost:5000/api/v1/users/profile" \\
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

"""

    def _generate_examples(self) -> str:
        """Genera ejemplos de uso"""
        return """## 💡 Ejemplos de Uso

### 1. Iniciar Conversación con Chatbot

```bash
# Iniciar sesión
curl -X POST "http://localhost:5001/api/v1/session/start" \\
  -H "Authorization: Bearer <token>" \\
  -H "Content-Type: application/json"

# Enviar mensaje
curl -X POST "http://localhost:5001/api/v1/message" \\
  -H "Authorization: Bearer <token>" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Hola, ¿cómo puedo ahorrar energía?"}'
```

### 2. Obtener Perfil de Usuario

```bash
curl -X GET "http://localhost:5000/api/v1/users/profile" \\
  -H "Authorization: Bearer <token>"
```

### 3. Análisis de Sentimientos

```bash
curl -X POST "http://localhost:5001/api/v1/analysis/sentiment" \\
  -H "Authorization: Bearer <token>" \\
  -H "Content-Type: application/json" \\
  -d '{"message_text": "Estoy muy contento con el servicio"}'
```

### 4. Recomendaciones de Tarifas

```bash
curl -X GET "http://localhost:5001/api/v1/energy/tariffs/recommendations" \\
  -H "Authorization: Bearer <token>"
```

---

## 📞 Soporte

Para soporte técnico o preguntas sobre la API:
- **Email**: dev@smarwatt.com
- **Documentación Interactiva**: [Swagger UI](./index.html)

---

*Documentación generada automáticamente el {datetime.now().strftime("%d/%m/%Y %H:%M")}*
"""


def main():
    """Función principal"""
    print("📝 GENERADOR DE DOCUMENTACIÓN MARKDOWN")
    print("=" * 42)

    # Detectar rutas
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    energy_api_path = current_dir
    expert_api_path = os.path.join(parent_dir, "expert_bot_api_COPY")
    output_file = os.path.join(parent_dir, "docs", "API_DOCUMENTATION.md")

    generator = MarkdownDocGenerator()

    if os.path.exists(energy_api_path) and os.path.exists(expert_api_path):
        print(f"📂 Energy IA API: {energy_api_path}")
        print(f"📂 Expert Bot API: {expert_api_path}")
        print(f"📄 Salida: {output_file}")

        # Generar Markdown
        markdown_content = generator.generate_markdown_docs(
            energy_api_path, expert_api_path
        )

        # Crear directorio si no existe
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Guardar archivo
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print("✅ Documentación Markdown generada exitosamente")
        print(f"👉 Archivo: {output_file}")

    else:
        print("❌ ERROR: No se encontraron los microservicios")


if __name__ == "__main__":
    import datetime

    main()
