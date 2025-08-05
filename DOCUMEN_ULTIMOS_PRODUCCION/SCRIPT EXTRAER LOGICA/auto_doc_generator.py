#!/usr/bin/env python3
"""
🚀 GENERADOR AUTOMÁTICO DE DOCUMENTACIÓN SMARWATT
=================================================

Genera documentación OpenAPI/Swagger automáticamente SIN TOCAR CÓDIGO FUENTE.
Analiza los archivos Flask existentes y crea documentación completa.

CARACTERÍSTICAS:
- NO modifica código fuente existente
- Genera OpenAPI 3.0 compatible
- Extrae endpoints automáticamente
- Documenta parámetros y respuestas
- Genera HTML interactivo

USO:
python auto_doc_generator.py

VERSIÓN: 1.0.0
FECHA: 2025-08-03
"""

import os
import re
import json
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path


class SmarWattDocGenerator:
    """Generador automático de documentación para microservicios SmarWatt"""

    def __init__(self):
        self.endpoints = []
        self.base_info = {
            "openapi": "3.0.3",
            "info": {
                "title": "SmarWatt Microservices API",
                "description": "API completa para análisis energético y chatbot inteligente",
                "version": "2.0.0",
                "contact": {"name": "SmarWatt Team", "email": "dev@smarwatt.com"},
            },
            "servers": [
                {
                    "url": "http://localhost:5000",
                    "description": "Energy IA API Development",
                },
                {
                    "url": "http://localhost:5001",
                    "description": "Expert Bot API Development",
                },
            ],
        }

    def analyze_flask_routes(self, file_path: str, service_name: str) -> List[Dict]:
        """Analiza un archivo Flask para extraer rutas automáticamente"""
        routes = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Patrones para buscar rutas Flask
            route_patterns = [
                r'@\w+\.route\(["\']([^"\']+)["\'](?:,\s*methods\s*=\s*\[([^\]]+)\])?\)',
                r'@app\.route\(["\']([^"\']+)["\'](?:,\s*methods\s*=\s*\[([^\]]+)\])?\)',
            ]

            function_pattern = r"def\s+(\w+)\s*\([^)]*\)(?:\s*->\s*[^:]+)?:"

            for route_pattern in route_patterns:
                route_matches = list(re.finditer(route_pattern, content))

                for match in route_matches:
                    route_path = match.group(1)
                    methods_str = match.group(2) if match.group(2) else '"GET"'
                    methods = [m.strip().strip("\"'") for m in methods_str.split(",")]

                    # Buscar la función correspondiente
                    func_start = match.end()
                    func_match = re.search(
                        function_pattern, content[func_start : func_start + 500]
                    )

                    if func_match:
                        func_name = func_match.group(1)

                        # Extraer docstring
                        docstring = self._extract_docstring(
                            content, func_start + func_match.end()
                        )

                        routes.append(
                            {
                                "path": route_path,
                                "methods": methods,
                                "function": func_name,
                                "description": docstring
                                or f"Endpoint {func_name} del servicio {service_name}",
                                "service": service_name,
                            }
                        )

        except Exception as e:
            print(f"⚠️ Error analizando {file_path}: {e}")

        return routes

    def _extract_docstring(self, content: str, start_pos: int) -> Optional[str]:
        """Extrae docstring de una función"""
        try:
            # Buscar docstring triple quote
            patterns = [r'"""\s*(.*?)\s*"""', r"'''\s*(.*?)\s*'''"]

            for pattern in patterns:
                docstring_match = re.search(
                    pattern, content[start_pos : start_pos + 1000], re.DOTALL
                )
                if docstring_match:
                    return docstring_match.group(1).strip()
        except:
            pass
        return None

    def analyze_microservice(self, service_path: str, service_name: str) -> List[Dict]:
        """Analiza un microservicio completo"""
        all_routes = []

        # Archivos de rutas a buscar
        route_files = [
            "app/routes.py",
            "app/chatbot_routes.py",
            "app/energy_routes.py",
            "app/analysis_routes.py",
            "app/async_routes.py",
            "app/cross_service_routes.py",
            "app/links_routes.py",
        ]

        for route_file in route_files:
            file_path = os.path.join(service_path, route_file)
            if os.path.exists(file_path):
                print(f"📖 Analizando {route_file} en {service_name}")
                routes = self.analyze_flask_routes(file_path, service_name)
                all_routes.extend(routes)
                print(f"   ✅ Encontradas {len(routes)} rutas")

        return all_routes

    def generate_openapi_spec(self, energy_api_path: str, expert_api_path: str) -> Dict:
        """Genera especificación OpenAPI completa"""

        print("\n🔍 ANALIZANDO MICROSERVICIOS...")

        # Analizar ambos microservicios
        energy_routes = self.analyze_microservice(energy_api_path, "Energy IA API")
        expert_routes = self.analyze_microservice(expert_api_path, "Expert Bot API")

        all_routes = energy_routes + expert_routes
        print(f"\n📊 TOTAL DE ENDPOINTS ENCONTRADOS: {len(all_routes)}")

        # Construir especificación OpenAPI
        spec = self.base_info.copy()
        spec["paths"] = {}

        for route in all_routes:
            path = route["path"]
            if path not in spec["paths"]:
                spec["paths"][path] = {}

            for method in route["methods"]:
                method_lower = method.lower()
                if method.upper() in [
                    "GET",
                    "POST",
                    "PUT",
                    "DELETE",
                    "PATCH",
                    "OPTIONS",
                ]:

                    # Detectar si requiere autenticación
                    requires_auth = any(
                        keyword in route["description"].lower()
                        for keyword in ["token_required", "auth", "authorization"]
                    )

                    endpoint_spec = {
                        "summary": f"{method} {path}",
                        "description": route["description"],
                        "tags": [route["service"]],
                        "responses": {
                            "200": {
                                "description": "Operación exitosa",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "success": {"type": "boolean"},
                                                "data": {"type": "object"},
                                            },
                                        }
                                    }
                                },
                            }
                        },
                    }

                    # Agregar respuestas de error comunes
                    if requires_auth:
                        endpoint_spec["security"] = [{"bearerAuth": []}]
                        endpoint_spec["responses"]["401"] = {
                            "description": "No autorizado"
                        }

                    endpoint_spec["responses"]["400"] = {
                        "description": "Error en la petición"
                    }
                    endpoint_spec["responses"]["500"] = {
                        "description": "Error interno del servidor"
                    }

                    # Agregar parámetros para métodos POST/PUT
                    if method.upper() in ["POST", "PUT", "PATCH"]:
                        endpoint_spec["requestBody"] = {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {
                                                "type": "string",
                                                "example": "Mensaje de ejemplo",
                                            }
                                        },
                                    }
                                }
                            },
                        }

                    spec["paths"][path][method_lower] = endpoint_spec

        # Agregar esquemas de seguridad
        spec["components"] = {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Token JWT de autenticación de Firebase",
                }
            }
        }

        return spec

    def generate_html_documentation(self, spec: Dict, output_path: str):
        """Genera documentación HTML interactiva con Swagger UI"""

        html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmarWatt API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
    <style>
        .swagger-ui .topbar { display: none; }
        .swagger-ui .info hgroup.main h2 { color: #2E7D32; }
        .swagger-ui .info .title { color: #1B5E20; }
        body { margin: 0; background: #fafafa; }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
    <script>
        SwaggerUIBundle({
            url: './openapi.json',
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.presets.standalone
            ],
            layout: "StandaloneLayout",
            deepLinking: true,
            showExtensions: true,
            showCommonExtensions: true
        });
    </script>
</body>
</html>"""

        # Crear directorio si no existe
        os.makedirs(output_path, exist_ok=True)

        # Guardar especificación JSON
        json_path = os.path.join(output_path, "openapi.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)

        # Guardar HTML
        html_path = os.path.join(output_path, "index.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_template)

        print(f"\n✅ DOCUMENTACIÓN GENERADA EXITOSAMENTE")
        print(f"📄 Especificación JSON: {json_path}")
        print(f"🌐 Documentación HTML: {html_path}")
        print(f"\n👉 Para ver la documentación:")
        print(f"   1. Abrir en navegador: {html_path}")
        print(
            f"   2. O servir con: python -m http.server 8080 --directory {output_path}"
        )


def main():
    """Función principal del generador"""
    print("🚀 GENERADOR AUTOMÁTICO DE DOCUMENTACIÓN SMARWATT")
    print("=" * 55)
    print("📝 Generando documentación OpenAPI sin tocar código fuente...")

    # Detectar rutas automáticamente - CORREGIDO
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)  # Subir un nivel

    # Buscar microservicios en el directorio padre
    energy_api_path = current_dir  # Este script está en energy_ia_api_COPY
    expert_api_path = os.path.join(parent_dir, "expert_bot_api_COPY")

    # Directorio de salida
    output_dir = os.path.join(parent_dir, "docs")

    generator = SmarWattDocGenerator()

    if os.path.exists(energy_api_path) and os.path.exists(expert_api_path):
        print(f"📂 Energy IA API: {energy_api_path}")
        print(f"📂 Expert Bot API: {expert_api_path}")
        print(f"📁 Salida: {output_dir}")

        spec = generator.generate_openapi_spec(energy_api_path, expert_api_path)
        generator.generate_html_documentation(spec, output_dir)

    else:
        print("❌ ERROR: No se encontraron los microservicios")
        print(
            f"🔍 Energy API: {energy_api_path} - {'✅' if os.path.exists(energy_api_path) else '❌'}"
        )
        print(
            f"🔍 Expert API: {expert_api_path} - {'✅' if os.path.exists(expert_api_path) else '❌'}"
        )

        # Listar directorios disponibles
        print(f"\n📂 Directorios disponibles en {parent_dir}:")
        try:
            for item in os.listdir(parent_dir):
                if os.path.isdir(os.path.join(parent_dir, item)):
                    print(f"   - {item}")
        except:
            print("   Error listando directorios")


if __name__ == "__main__":
    main()
