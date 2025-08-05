#!/usr/bin/env python3
"""
🔍 ANALIZADOR AVANZADO DE LÓGICA DE ENDPOINTS
============================================

Analiza automáticamente la LÓGICA INTERNA de cada endpoint.
Extrae parámetros, validaciones, llamadas a servicios, y flujo de datos.

CARACTERÍSTICAS AVANZADAS:
- Extrae parámetros de request y response
- Identifica validaciones y checks
- Detecta llamadas a servicios externos
- Analiza flujo de datos y transformaciones
- Documenta manejo de errores
- Identifica patrones de autenticación

VERSIÓN: 1.0.0 - ANALIZADOR LÓGICO
FECHA: 2025-08-03
"""

import os
import re
import ast
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path


class EndpointLogicAnalyzer:
    """Analizador avanzado de lógica interna de endpoints"""

    def __init__(self):
        self.service_patterns = {
            "bigquery": r"bigquery|bq_client|BigQuery",
            "firebase": r"firebase|auth|token_required",
            "gemini": r"gemini|genai|GenerativeModel",
            "vertex_ai": r"vertex|aiplatform|VertexAI",
            "requests": r"requests\.|http",
            "pandas": r"pd\.|pandas|DataFrame",
            "numpy": r"np\.|numpy",
            "logging": r"logging|logger",
        }

        self.validation_patterns = {
            "required_fields": r"required|mandatory|obligatorio",
            "type_validation": r"isinstance|type\(|str\(|int\(|float\(",
            "range_validation": r"len\(|range\(|min\(|max\(",
            "format_validation": r"regex|pattern|format|validate",
        }

    def analyze_endpoint_logic(
        self, file_path: str, function_name: str
    ) -> Dict[str, Any]:
        """Analiza la lógica completa de un endpoint específico"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extraer código de la función
            function_code = self._extract_function_code(content, function_name)
            if not function_code:
                return {"error": "Function not found"}

            analysis = {
                "function_name": function_name,
                "file_path": file_path,
                "logic_analysis": {
                    "parameters": self._analyze_parameters(function_code),
                    "validations": self._analyze_validations(function_code),
                    "services_used": self._analyze_services(function_code),
                    "data_flow": self._analyze_data_flow(function_code),
                    "error_handling": self._analyze_error_handling(function_code),
                    "response_structure": self._analyze_response_structure(
                        function_code
                    ),
                    "business_logic": self._extract_business_logic(function_code),
                    "database_operations": self._analyze_database_operations(
                        function_code
                    ),
                    "external_calls": self._analyze_external_calls(function_code),
                },
            }

            return analysis

        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def _extract_function_code(self, content: str, function_name: str) -> Optional[str]:
        """Extrae el código completo de una función"""
        try:
            # Buscar definición de función
            pattern = (
                rf"def\s+{re.escape(function_name)}\s*\([^)]*\)(?:\s*->\s*[^:]+)?:"
            )
            match = re.search(pattern, content)

            if not match:
                return None

            start_pos = match.start()
            lines = content[start_pos:].split("\n")

            # Encontrar indentación base
            first_line = lines[0]
            base_indent = len(first_line) - len(first_line.lstrip())

            function_lines = [lines[0]]  # Incluir definición

            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "":  # Línea vacía
                    function_lines.append(line)
                    continue

                current_indent = len(line) - len(line.lstrip())

                # Si la indentación es menor o igual a la base Y no es línea vacía, fin de función
                if current_indent <= base_indent and line.strip():
                    break

                function_lines.append(line)

            return "\n".join(function_lines)

        except Exception:
            return None

    def _analyze_parameters(self, code: str) -> Dict[str, Any]:
        """Analiza parámetros de entrada y validaciones"""
        parameters = {
            "request_data": [],
            "path_parameters": [],
            "query_parameters": [],
            "headers": [],
            "validation_rules": [],
        }

        # Buscar request.json, request.args, etc.
        if "request.json" in code:
            json_extractions = re.findall(
                r'request\.json\.get\(["\']([^"\']+)["\']', code
            )
            parameters["request_data"].extend(json_extractions)

        if "request.args" in code:
            args_extractions = re.findall(
                r'request\.args\.get\(["\']([^"\']+)["\']', code
            )
            parameters["query_parameters"].extend(args_extractions)

        if "request.headers" in code:
            header_extractions = re.findall(
                r'request\.headers\.get\(["\']([^"\']+)["\']', code
            )
            parameters["headers"].extend(header_extractions)

        # Buscar validaciones
        validation_patterns = [
            r"if\s+not\s+(\w+)",
            r"if\s+(\w+)\s+is\s+None",
            r"if\s+len\((\w+)\)",
            r"validate_(\w+)\(",
        ]

        for pattern in validation_patterns:
            matches = re.findall(pattern, code)
            parameters["validation_rules"].extend(matches)

        return parameters

    def _analyze_validations(self, code: str) -> List[Dict[str, str]]:
        """Identifica validaciones implementadas"""
        validations = []

        # Patrones de validación comunes
        validation_checks = [
            (r"if\s+not\s+(\w+)", "required_field"),
            (r"if\s+(\w+)\s+is\s+None", "null_check"),
            (r"if\s+len\(([^)]+)\)\s*[<>=]", "length_validation"),
            (r"isinstance\(([^,]+),\s*(\w+)\)", "type_validation"),
            (r"if\s+(\w+)\s+not\s+in", "enum_validation"),
            (r'raise\s+AppError\(["\']([^"\']+)["\']', "custom_error"),
        ]

        for pattern, validation_type in validation_checks:
            matches = re.findall(pattern, code)
            for match in matches:
                if isinstance(match, tuple):
                    validations.append(
                        {
                            "type": validation_type,
                            "field": match[0] if match else "unknown",
                            "details": str(match),
                        }
                    )
                else:
                    validations.append(
                        {"type": validation_type, "field": match, "details": match}
                    )

        return validations

    def _analyze_services(self, code: str) -> Dict[str, List[str]]:
        """Identifica servicios externos utilizados"""
        services = {}

        for service, pattern in self.service_patterns.items():
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                services[service] = list(set(matches))

        # Buscar imports específicos
        imports = re.findall(r"from\s+([^\s]+)\s+import", code)
        if imports:
            services["imports"] = imports

        return services

    def _analyze_data_flow(self, code: str) -> List[str]:
        """Analiza el flujo de datos principal"""
        flow_steps = []

        # Identificar pasos principales del flujo
        step_patterns = [
            r"# .*?([A-Z][^#\n]*)",  # Comentarios con pasos
            r'logger\.info\(["\']([^"\']+)["\']',  # Logs informativos
            r"(\w+)\s*=\s*.*?\.get\(",  # Obtención de datos
            r"(\w+)\s*=\s*.*?Service\(",  # Uso de servicios
            r"return\s+jsonify\(",  # Retornos
        ]

        for pattern in step_patterns:
            matches = re.findall(pattern, code)
            flow_steps.extend(
                [match if isinstance(match, str) else match[0] for match in matches]
            )

        return flow_steps[:10]  # Primeros 10 pasos

    def _analyze_error_handling(self, code: str) -> Dict[str, List[str]]:
        """Analiza manejo de errores"""
        error_handling = {
            "try_catch_blocks": [],
            "custom_exceptions": [],
            "error_responses": [],
            "logging_errors": [],
        }

        # Try-catch blocks
        try_blocks = re.findall(r"try:\s*\n(.*?)except\s+([^:]+):", code, re.DOTALL)
        error_handling["try_catch_blocks"] = [exc[1].strip() for exc in try_blocks]

        # Custom exceptions
        custom_exceptions = re.findall(r"raise\s+(\w+Error)\(", code)
        error_handling["custom_exceptions"] = list(set(custom_exceptions))

        # Error responses
        error_responses = re.findall(r"return\s+jsonify\(.*?error.*?\)", code)
        error_handling["error_responses"] = error_responses[:5]

        # Error logging
        error_logs = re.findall(r'logger\.error\(["\']([^"\']+)["\']', code)
        error_handling["logging_errors"] = error_logs

        return error_handling

    def _analyze_response_structure(self, code: str) -> Dict[str, Any]:
        """Analiza estructura de respuestas"""
        response_analysis = {
            "return_patterns": [],
            "response_fields": [],
            "status_codes": [],
        }

        # Patrones de retorno
        return_patterns = re.findall(r"return\s+(.*?)(?:\n|$)", code)
        response_analysis["return_patterns"] = return_patterns[:5]

        # Campos de respuesta en jsonify
        jsonify_content = re.findall(r"jsonify\(\s*{([^}]+)}\s*\)", code)
        for content in jsonify_content:
            fields = re.findall(r'["\']([^"\']+)["\']:', content)
            response_analysis["response_fields"].extend(fields)

        # Códigos de estado
        status_codes = re.findall(r"return\s+.*?,\s*(\d{3})", code)
        response_analysis["status_codes"] = list(set(status_codes))

        return response_analysis

    def _extract_business_logic(self, code: str) -> List[str]:
        """Extrae lógica de negocio principal"""
        business_logic = []

        # Buscar comentarios explicativos
        comments = re.findall(r"#\s*([A-Z][^#\n]{10,})", code)
        business_logic.extend(comments)

        # Buscar operaciones importantes
        operations = [
            r"if\s+.*?:\s*\n\s*#\s*([^#\n]+)",  # Condiciones con comentarios
            r"for\s+.*?:\s*\n\s*#\s*([^#\n]+)",  # Loops con comentarios
            r"(\w+_service\.[\w_]+\()",  # Llamadas a servicios
            r"(calculate_\w+\()",  # Funciones de cálculo
            r"(process_\w+\()",  # Funciones de procesamiento
        ]

        for pattern in operations:
            matches = re.findall(pattern, code)
            business_logic.extend(
                [match if isinstance(match, str) else match[0] for match in matches]
            )

        return business_logic[:8]  # Top 8 elementos

    def _analyze_database_operations(self, code: str) -> Dict[str, List[str]]:
        """Analiza operaciones de base de datos"""
        db_ops = {"queries": [], "inserts": [], "updates": [], "tables_accessed": []}

        # Queries
        query_patterns = [
            r"SELECT\s+.*?FROM\s+(\w+)",
            r'query\s*=\s*["\']([^"\']+)["\']',
            r'\.query\(["\']([^"\']+)["\']',
        ]

        for pattern in query_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            db_ops["queries"].extend(matches)

        # Inserts
        insert_patterns = [r"INSERT\s+INTO\s+(\w+)", r"insert_rows\(", r"\.insert\("]

        for pattern in insert_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            db_ops["inserts"].extend(matches)

        # Tablas mencionadas
        table_mentions = re.findall(r'["\'](\w*table\w*)["\']', code, re.IGNORECASE)
        db_ops["tables_accessed"] = list(set(table_mentions))

        return db_ops

    def _analyze_external_calls(self, code: str) -> List[Dict[str, str]]:
        """Analiza llamadas a APIs externas"""
        external_calls = []

        # Requests HTTP
        http_calls = re.findall(r'requests\.(\w+)\(["\']([^"\']+)["\']', code)
        for method, url in http_calls:
            external_calls.append(
                {"type": "HTTP", "method": method.upper(), "endpoint": url}
            )

        # URLs configuradas
        url_configs = re.findall(r"(\w+_URL)\s*=", code)
        for url_config in url_configs:
            external_calls.append(
                {
                    "type": "CONFIG_URL",
                    "service": url_config.replace("_URL", "").lower(),
                }
            )

        return external_calls


class AdvancedDocGenerator:
    """Generador avanzado de documentación con análisis de lógica"""

    def __init__(self):
        self.analyzer = EndpointLogicAnalyzer()
        self.base_generator = None  # Will import the basic generator

    def generate_enhanced_documentation(
        self, energy_api_path: str, expert_api_path: str
    ):
        """Genera documentación mejorada con análisis de lógica"""

        # Analizar ambos microservicios
        enhanced_docs = {
            "energy_ia_api": self._analyze_service_logic(
                energy_api_path, "Energy IA API"
            ),
            "expert_bot_api": self._analyze_service_logic(
                expert_api_path, "Expert Bot API"
            ),
            "summary": {
                "total_endpoints": 0,
                "services_used": set(),
                "common_patterns": [],
            },
        }

        return enhanced_docs

    def _analyze_service_logic(
        self, service_path: str, service_name: str
    ) -> Dict[str, Any]:
        """Analiza lógica de un microservicio completo"""
        service_analysis = {
            "service_name": service_name,
            "endpoints": [],
            "common_services": set(),
            "error_patterns": [],
            "business_patterns": [],
        }

        # Archivos de rutas a analizar
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
                print(f"🔍 Analizando lógica en {route_file}")
                endpoints = self._extract_and_analyze_endpoints(file_path)
                service_analysis["endpoints"].extend(endpoints)

        return service_analysis

    def _extract_and_analyze_endpoints(self, file_path: str) -> List[Dict[str, Any]]:
        """Extrae y analiza endpoints de un archivo"""
        endpoints = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Buscar definiciones de rutas y funciones
            route_pattern = r'@\w+\.route\(["\']([^"\']+)["\'](?:,\s*methods\s*=\s*\[([^\]]+)\])?\)\s*(?:@\w+\s*)*\s*def\s+(\w+)\s*\('

            matches = re.finditer(route_pattern, content)

            for match in matches:
                route_path = match.group(1)
                methods = match.group(2) if match.group(2) else "GET"
                function_name = match.group(3)

                # Analizar lógica del endpoint
                logic_analysis = self.analyzer.analyze_endpoint_logic(
                    file_path, function_name
                )

                endpoint_doc = {
                    "path": route_path,
                    "methods": [m.strip().strip("\"'") for m in methods.split(",")],
                    "function": function_name,
                    "file": os.path.basename(file_path),
                    "logic": logic_analysis.get("logic_analysis", {}),
                    "complexity_score": self._calculate_complexity(logic_analysis),
                }

                endpoints.append(endpoint_doc)
                print(
                    f"   ✅ {function_name}: Complejidad {endpoint_doc['complexity_score']}/10"
                )

        except Exception as e:
            print(f"⚠️ Error analizando {file_path}: {e}")

        return endpoints

    def _calculate_complexity(self, analysis: Dict[str, Any]) -> int:
        """Calcula un score de complejidad del endpoint (1-10)"""
        if "error" in analysis:
            return 1

        logic = analysis.get("logic_analysis", {})
        complexity = 1

        # Aumentar por servicios utilizados
        services = logic.get("services_used", {})
        complexity += len(services)

        # Aumentar por validaciones
        validations = logic.get("validations", [])
        complexity += len(validations)

        # Aumentar por operaciones DB
        db_ops = logic.get("database_operations", {})
        complexity += sum(len(ops) for ops in db_ops.values())

        # Aumentar por llamadas externas
        external_calls = logic.get("external_calls", [])
        complexity += len(external_calls)

        return min(10, complexity)

    def save_enhanced_documentation(self, docs: Dict[str, Any], output_path: str):
        """Guarda documentación mejorada"""
        os.makedirs(output_path, exist_ok=True)

        # Guardar análisis completo en JSON
        json_path = os.path.join(output_path, "enhanced_api_analysis.json")
        with open(json_path, "w", encoding="utf-8") as f:
            # Convertir sets a listas para JSON
            json_docs = self._prepare_for_json(docs)
            json.dump(json_docs, f, indent=2, ensure_ascii=False)

        # Generar HTML con análisis detallado
        html_path = os.path.join(output_path, "logic_analysis.html")
        self._generate_logic_html(docs, html_path)

        print(f"✅ Documentación mejorada guardada:")
        print(f"📄 JSON: {json_path}")
        print(f"🌐 HTML: {html_path}")

    def _prepare_for_json(self, obj):
        """Prepara objeto para serialización JSON"""
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, dict):
            return {k: self._prepare_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._prepare_for_json(item) for item in obj]
        else:
            return obj

    def _generate_logic_html(self, docs: Dict[str, Any], html_path: str):
        """Genera HTML con análisis de lógica"""
        html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmarWatt - Análisis de Lógica de Endpoints</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1 { color: #2E7D32; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }
        h2 { color: #1976D2; margin-top: 30px; }
        h3 { color: #795548; }
        .endpoint { background: #f9f9f9; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 5px solid #4CAF50; }
        .complexity { display: inline-block; padding: 4px 12px; border-radius: 15px; color: white; font-weight: bold; }
        .complexity-low { background: #4CAF50; }
        .complexity-medium { background: #FF9800; }
        .complexity-high { background: #F44336; }
        .logic-section { margin: 15px 0; }
        .logic-title { font-weight: bold; color: #1976D2; margin-bottom: 8px; }
        .logic-list { background: white; padding: 10px; border-radius: 4px; }
        .method-tag { display: inline-block; padding: 2px 8px; margin: 2px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .method-get { background: #4CAF50; color: white; }
        .method-post { background: #2196F3; color: white; }
        .method-put { background: #FF9800; color: white; }
        .method-delete { background: #F44336; color: white; }
        pre { background: #263238; color: #ECEFF1; padding: 15px; border-radius: 4px; overflow-x: auto; }
        .service-tag { display: inline-block; padding: 2px 6px; margin: 2px; background: #E3F2FD; color: #1976D2; border-radius: 3px; font-size: 11px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 SmarWatt - Análisis de Lógica de Endpoints</h1>
        <p><strong>Análisis automático de lógica interna de endpoints</strong> - Generado automáticamente</p>
"""

        # Generar contenido para cada servicio
        for service_key, service_data in docs.items():
            if service_key == "summary":
                continue

            service_name = service_data.get("service_name", service_key)
            endpoints = service_data.get("endpoints", [])

            html_content += f"""
        <h2>🔧 {service_name}</h2>
        <p><strong>Total de endpoints analizados:</strong> {len(endpoints)}</p>
"""

            for endpoint in endpoints:
                complexity = endpoint.get("complexity_score", 1)
                complexity_class = (
                    "complexity-low"
                    if complexity <= 3
                    else "complexity-medium" if complexity <= 6 else "complexity-high"
                )
                complexity_text = (
                    "Baja"
                    if complexity <= 3
                    else "Media" if complexity <= 6 else "Alta"
                )

                methods_html = "".join(
                    [
                        f'<span class="method-tag method-{method.lower()}">{method}</span>'
                        for method in endpoint.get("methods", [])
                    ]
                )

                html_content += f"""
        <div class="endpoint">
            <h3>{endpoint.get('path', 'Unknown')} <span class="complexity {complexity_class}">Complejidad: {complexity_text} ({complexity}/10)</span></h3>
            <p><strong>Métodos:</strong> {methods_html}</p>
            <p><strong>Función:</strong> <code>{endpoint.get('function', 'N/A')}</code> | <strong>Archivo:</strong> {endpoint.get('file', 'N/A')}</p>
"""

                logic = endpoint.get("logic", {})

                # Parámetros
                params = logic.get("parameters", {})
                if any(params.values()):
                    html_content += """
            <div class="logic-section">
                <div class="logic-title">📝 Parámetros:</div>
                <div class="logic-list">
"""
                    for param_type, param_list in params.items():
                        if param_list:
                            html_content += f'<strong>{param_type.replace("_", " ").title()}:</strong> {", ".join(param_list)}<br>'

                    html_content += "</div></div>"

                # Servicios utilizados
                services = logic.get("services_used", {})
                if services:
                    html_content += """
            <div class="logic-section">
                <div class="logic-title">🔧 Servicios Utilizados:</div>
                <div class="logic-list">
"""
                    for service, usage in services.items():
                        service_tags = "".join(
                            [f'<span class="service-tag">{u}</span>' for u in usage]
                        )
                        html_content += (
                            f"<strong>{service.title()}:</strong> {service_tags}<br>"
                        )

                    html_content += "</div></div>"

                # Validaciones
                validations = logic.get("validations", [])
                if validations:
                    html_content += """
            <div class="logic-section">
                <div class="logic-title">✅ Validaciones:</div>
                <div class="logic-list">
"""
                    for validation in validations[:5]:
                        html_content += f'• <strong>{validation.get("type", "unknown")}:</strong> {validation.get("field", "N/A")}<br>'

                    html_content += "</div></div>"

                # Lógica de negocio
                business_logic = logic.get("business_logic", [])
                if business_logic:
                    html_content += """
            <div class="logic-section">
                <div class="logic-title">💼 Lógica de Negocio:</div>
                <div class="logic-list">
"""
                    for logic_item in business_logic[:5]:
                        html_content += f"• {logic_item}<br>"

                    html_content += "</div></div>"

                html_content += "</div>"

        html_content += """
    </div>
</body>
</html>"""

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)


def main():
    """Función principal del analizador avanzado"""
    print("🔍 ANALIZADOR AVANZADO DE LÓGICA DE ENDPOINTS")
    print("=" * 50)

    # Detectar rutas
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    energy_api_path = current_dir
    expert_api_path = os.path.join(parent_dir, "expert_bot_api_COPY")
    output_dir = os.path.join(parent_dir, "docs")

    generator = AdvancedDocGenerator()

    if os.path.exists(energy_api_path) and os.path.exists(expert_api_path):
        print(f"📂 Energy IA API: {energy_api_path}")
        print(f"📂 Expert Bot API: {expert_api_path}")
        print(f"📁 Salida: {output_dir}")

        docs = generator.generate_enhanced_documentation(
            energy_api_path, expert_api_path
        )
        generator.save_enhanced_documentation(docs, output_dir)

        print("\n✅ ANÁLISIS DE LÓGICA COMPLETADO")
        print("👉 Ver análisis detallado en: docs/logic_analysis.html")

    else:
        print("❌ ERROR: No se encontraron los microservicios")


if __name__ == "__main__":
    main()
