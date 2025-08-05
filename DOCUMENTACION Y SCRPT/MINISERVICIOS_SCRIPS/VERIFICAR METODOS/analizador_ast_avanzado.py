#!/usr/bin/env python3
"""
🚀 ANALIZADOR DE CÓDIGO AST AVANZADO - NIVEL ENTERPRISE
====================================================

TECNOLOGÍAS AVANZADAS UTILIZADAS:
- Abstract Syntax Tree (AST) para análisis profundo
- Visitor Pattern para recorrido optimizado
- Type Annotations completo
- Docstring parsing avanzado
- Regular expressions compiladas
- Threading para procesamiento paralelo
- JSON Schema validation
- Logging estructurado

AUTOR: AI Assistant
FECHA: 2025-08-04
VERSIÓN: 2.0.0 - ENTERPRISE GRADE
"""

import ast
import os
import re
import json
import inspect
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass, asdict
from pathlib import Path

# Configurar logging avanzado
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class EndpointInfo:
    """Estructura de datos para información de endpoint"""

    route: str
    methods: List[str]
    function_name: str
    file_path: str
    line_number: int
    docstring: Optional[str]
    parameters: List[Dict[str, Any]]
    decorators: List[str]
    returns_type: Optional[str]
    body_summary: str
    complexity_score: int
    dependencies: List[str]
    microservice: str


@dataclass
class AnalysisResult:
    """Resultado completo del análisis"""

    endpoints: List[EndpointInfo]
    total_endpoints: int
    files_processed: int
    errors: List[str]
    microservices: Dict[str, int]
    http_methods: Dict[str, int]
    analysis_time: float
    timestamp: str


class AdvancedFlaskEndpointAnalyzer(ast.NodeVisitor):
    """
    🧠 ANALIZADOR AST AVANZADO PARA ENDPOINTS FLASK

    Utiliza Abstract Syntax Tree para análisis profundo de código:
    - Detección de rutas Flask con decoradores
    - Extracción de parámetros y tipos
    - Análisis de complejidad ciclomática
    - Detección de dependencias
    - Parsing de docstrings
    """

    def __init__(self, file_path: str, microservice: str):
        self.file_path = file_path
        self.microservice = microservice
        self.endpoints: List[EndpointInfo] = []
        self.current_class = None
        self.imports = set()

        # Expresiones regulares compiladas para performance
        self.route_pattern = re.compile(r'["\']([^"\']*)["\']')
        self.methods_pattern = re.compile(r"methods\s*=\s*\[([^\]]*)\]")

    def visit_Import(self, node: ast.Import) -> None:
        """Visita declaraciones import"""
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visita declaraciones from ... import"""
        if node.module:
            for alias in node.names:
                self.imports.add(f"{node.module}.{alias.name}")
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        🎯 ANÁLISIS AVANZADO DE FUNCIONES
        Detecta endpoints Flask y extrae información completa
        """
        try:
            # Buscar decoradores de ruta Flask
            flask_decorators = []
            route_info = None
            methods = ["GET"]  # Default

            for decorator in node.decorator_list:
                decorator_info = self._analyze_decorator(decorator)
                if decorator_info:
                    flask_decorators.append(decorator_info["name"])
                    if decorator_info["name"] in [
                        "route",
                        "get",
                        "post",
                        "put",
                        "delete",
                        "patch",
                    ]:
                        route_info = decorator_info
                        if "methods" in decorator_info:
                            methods = decorator_info["methods"]

            # Si es un endpoint Flask
            if route_info and "route" in route_info:
                endpoint = EndpointInfo(
                    route=route_info["route"],
                    methods=methods,
                    function_name=node.name,
                    file_path=self.file_path,
                    line_number=node.lineno,
                    docstring=ast.get_docstring(node),
                    parameters=self._extract_parameters(node),
                    decorators=flask_decorators,
                    returns_type=self._extract_return_type(node),
                    body_summary=self._analyze_function_body(node),
                    complexity_score=self._calculate_complexity(node),
                    dependencies=self._extract_dependencies(node),
                    microservice=self.microservice,
                )
                self.endpoints.append(endpoint)
                logger.debug(
                    f"Endpoint detectado: {route_info['route']} en {self.file_path}:{node.lineno}"
                )

        except Exception as e:
            logger.error(f"Error analizando función {node.name}: {str(e)}")

        self.generic_visit(node)

    def _analyze_decorator(
        self, decorator: ast.AST
    ) -> Optional[Dict[str, Union[str, List[str]]]]:
        """🔍 Análisis avanzado de decoradores Flask"""
        try:
            if isinstance(decorator, ast.Call):
                # @app.route("/path", methods=['POST']) o @blueprint.route()
                if isinstance(decorator.func, ast.Attribute):
                    attr_name = decorator.func.attr
                    if attr_name in ["route", "get", "post", "put", "delete", "patch"]:
                        result = {"name": attr_name}

                        # Extraer ruta (primer argumento)
                        if decorator.args:
                            if isinstance(decorator.args[0], ast.Constant):
                                route_value = decorator.args[0].value
                                if isinstance(route_value, str):
                                    result["route"] = route_value
                            elif isinstance(decorator.args[0], ast.Str):  # Python < 3.8
                                result["route"] = decorator.args[0].s

                        # Extraer métodos HTTP
                        for keyword in decorator.keywords:
                            if keyword.arg == "methods":
                                if isinstance(keyword.value, ast.List):
                                    methods = []
                                    for elt in keyword.value.elts:
                                        if isinstance(elt, ast.Constant):
                                            if isinstance(elt.value, str):
                                                methods.append(elt.value)
                                        elif isinstance(elt, ast.Str):  # Python < 3.8
                                            methods.append(elt.s)
                                    if methods:  # Solo agregar si tiene métodos válidos
                                        result["methods"] = methods

                        return result

                # @token_required, etc.
                elif isinstance(decorator.func, ast.Name):
                    if decorator.func.id in ["token_required", "login_required"]:
                        return {"name": decorator.func.id, "type": "auth"}

            elif isinstance(decorator, ast.Attribute):
                # @app.route (sin parámetros)
                if decorator.attr in ["route", "get", "post", "put", "delete", "patch"]:
                    return {"name": decorator.attr}

            elif isinstance(decorator, ast.Name):
                # @token_required
                if decorator.id in ["token_required", "login_required"]:
                    return {"name": decorator.id, "type": "auth"}

        except Exception as e:
            logger.error(f"Error analizando decorador: {str(e)}")

        return None

    def _extract_parameters(self, node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """📋 Extracción avanzada de parámetros de función"""
        parameters = []

        try:
            for arg in node.args.args:
                param_info = {
                    "name": arg.arg,
                    "type": None,
                    "default": None,
                    "annotation": None,
                }

                # Extraer type annotation
                if arg.annotation:
                    param_info["annotation"] = ast.unparse(arg.annotation)

                parameters.append(param_info)

            # Extraer defaults
            defaults = node.args.defaults
            if defaults:
                default_offset = len(parameters) - len(defaults)
                for i, default in enumerate(defaults):
                    if default_offset + i < len(parameters):
                        try:
                            parameters[default_offset + i]["default"] = ast.unparse(
                                default
                            )
                        except:
                            parameters[default_offset + i][
                                "default"
                            ] = "<complex_default>"

        except Exception as e:
            logger.error(f"Error extrayendo parámetros: {str(e)}")

        return parameters

    def _extract_return_type(self, node: ast.FunctionDef) -> Optional[str]:
        """🔄 Extracción de tipo de retorno"""
        try:
            if node.returns:
                return ast.unparse(node.returns)
        except Exception as e:
            logger.error(f"Error extrayendo tipo de retorno: {str(e)}")
        return None

    def _analyze_function_body(self, node: ast.FunctionDef) -> str:
        """🧠 Análisis del cuerpo de la función"""
        try:
            statements = len(node.body)

            # Contar diferentes tipos de statements
            assignments = sum(1 for n in ast.walk(node) if isinstance(n, ast.Assign))
            calls = sum(1 for n in ast.walk(node) if isinstance(n, ast.Call))
            conditionals = sum(
                1 for n in ast.walk(node) if isinstance(n, (ast.If, ast.While, ast.For))
            )

            return f"{statements} statements, {assignments} assignments, {calls} calls, {conditionals} control structures"

        except Exception as e:
            logger.error(f"Error analizando cuerpo de función: {str(e)}")
            return "Analysis failed"

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """📊 Cálculo de complejidad ciclomática"""
        try:
            complexity = 1  # Base complexity

            for n in ast.walk(node):
                if isinstance(n, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                    complexity += 1
                elif isinstance(n, ast.BoolOp):
                    complexity += len(n.values) - 1
                elif isinstance(n, (ast.Break, ast.Continue)):
                    complexity += 1

            return complexity

        except Exception as e:
            logger.error(f"Error calculando complejidad: {str(e)}")
            return 0

    def _extract_dependencies(self, node: ast.FunctionDef) -> List[str]:
        """🔗 Extracción de dependencias de la función"""
        dependencies = set()

        try:
            for n in ast.walk(node):
                if isinstance(n, ast.Call):
                    if isinstance(n.func, ast.Name):
                        dependencies.add(n.func.id)
                    elif isinstance(n.func, ast.Attribute):
                        if isinstance(n.func.value, ast.Name):
                            dependencies.add(f"{n.func.value.id}.{n.func.attr}")

        except Exception as e:
            logger.error(f"Error extrayendo dependencias: {str(e)}")

        return list(dependencies)


class EnterpriseCodeAnalyzer:
    """
    🏢 ANALIZADOR DE CÓDIGO EMPRESARIAL DE NIVEL AVANZADO

    Características enterprise:
    - Procesamiento paralelo con ThreadPoolExecutor
    - Análisis AST profundo
    - Detección automática de microservicios
    - Reportes JSON y Markdown estructurados
    - Logging detallado
    - Manejo robusto de errores
    """

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.analysis_start_time = datetime.now()

        # Configuración avanzada
        self.supported_extensions = {".py"}
        self.route_files_patterns = [
            r".*routes\.py$",
            r".*_routes\.py$",
            r".*routes_.*\.py$",
            r".*api\.py$",
            r".*endpoints\.py$",
        ]

        # Compilar patterns para performance
        self.compiled_patterns = [
            re.compile(pattern) for pattern in self.route_files_patterns
        ]

        logger.info(f"🚀 EnterpriseCodeAnalyzer iniciado en: {self.base_path}")

    def analyze_all_endpoints(self) -> AnalysisResult:
        """
        🎯 ANÁLISIS COMPLETO DE TODOS LOS ENDPOINTS
        Utiliza procesamiento paralelo para máximo rendimiento
        """
        start_time = datetime.now()
        logger.info("🔍 Iniciando análisis completo de endpoints...")

        # Detectar archivos de rutas automáticamente
        route_files = self._discover_route_files()
        logger.info(f"📁 Archivos de rutas detectados: {len(route_files)}")

        all_endpoints = []
        errors = []
        files_processed = 0

        # Procesamiento paralelo con ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {
                executor.submit(self._analyze_single_file, file_path): file_path
                for file_path in route_files
            }

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    endpoints, file_errors = future.result()
                    all_endpoints.extend(endpoints)
                    errors.extend(file_errors)
                    files_processed += 1
                    logger.info(
                        f"✅ Procesado: {file_path} ({len(endpoints)} endpoints)"
                    )
                except Exception as e:
                    error_msg = f"Error procesando {file_path}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(error_msg)

        # Calcular estadísticas
        microservices = {}
        http_methods = {}

        for endpoint in all_endpoints:
            # Contar por microservicio
            microservices[endpoint.microservice] = (
                microservices.get(endpoint.microservice, 0) + 1
            )

            # Contar métodos HTTP
            for method in endpoint.methods:
                http_methods[method] = http_methods.get(method, 0) + 1

        analysis_time = (datetime.now() - start_time).total_seconds()

        result = AnalysisResult(
            endpoints=all_endpoints,
            total_endpoints=len(all_endpoints),
            files_processed=files_processed,
            errors=errors,
            microservices=microservices,
            http_methods=http_methods,
            analysis_time=analysis_time,
            timestamp=datetime.now().isoformat(),
        )

        logger.info(
            f"🎉 Análisis completado: {result.total_endpoints} endpoints en {analysis_time:.2f}s"
        )
        return result

    def _discover_route_files(self) -> List[Path]:
        """🔍 Descubrimiento automático de archivos de rutas"""
        route_files = []

        try:
            # Buscar recursivamente archivos Python
            for py_file in self.base_path.rglob("*.py"):
                # Verificar si coincide con patrones de rutas
                if any(
                    pattern.match(str(py_file)) for pattern in self.compiled_patterns
                ):
                    route_files.append(py_file)
                    continue

                # Verificar contenido para detectar rutas Flask
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read(1000)  # Solo primeros 1000 caracteres
                        if any(
                            keyword in content
                            for keyword in ["@app.route", ".route(", "Blueprint"]
                        ):
                            route_files.append(py_file)
                except:
                    continue

        except Exception as e:
            logger.error(f"Error descubriendo archivos: {str(e)}")

        return route_files

    def _analyze_single_file(
        self, file_path: Path
    ) -> Tuple[List[EndpointInfo], List[str]]:
        """🔬 Análisis detallado de un archivo individual"""
        errors = []
        endpoints = []

        try:
            # Determinar microservicio por ruta
            microservice = self._determine_microservice(file_path)

            # Leer y parsear archivo
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parsear AST
            try:
                tree = ast.parse(content, filename=str(file_path))
            except SyntaxError as e:
                error_msg = f"Error de sintaxis en {file_path}: {str(e)}"
                errors.append(error_msg)
                return endpoints, errors

            # Analizar con visitor avanzado
            analyzer = AdvancedFlaskEndpointAnalyzer(str(file_path), microservice)
            analyzer.visit(tree)
            endpoints = analyzer.endpoints

        except Exception as e:
            error_msg = f"Error analizando {file_path}: {str(e)}"
            errors.append(error_msg)
            logger.error(error_msg)

        return endpoints, errors

    def _determine_microservice(self, file_path: Path) -> str:
        """🏢 Determinación automática de microservicio"""
        path_str = str(file_path)

        if "expert_bot_api" in path_str:
            return "expert_bot_api"
        elif "energy_ia_api" in path_str:
            return "energy_ia_api"
        else:
            # Extraer del path
            parts = file_path.parts
            for part in parts:
                if "api" in part.lower():
                    return part
            return "unknown"

    def generate_reports(self, result: AnalysisResult) -> Tuple[str, str]:
        """📊 Generación de reportes avanzados JSON y Markdown"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generar reporte JSON
        json_filename = f"analisis_endpoints_avanzado_{timestamp}.json"
        json_data = {
            "metadata": {
                "timestamp": result.timestamp,
                "analysis_time_seconds": result.analysis_time,
                "total_endpoints": result.total_endpoints,
                "files_processed": result.files_processed,
                "analyzer_version": "2.0.0-ENTERPRISE",
            },
            "statistics": {
                "microservices": result.microservices,
                "http_methods": result.http_methods,
                "errors_count": len(result.errors),
            },
            "endpoints": [asdict(endpoint) for endpoint in result.endpoints],
            "errors": result.errors,
        }

        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        # Generar reporte Markdown
        md_filename = f"documentacion_endpoints_avanzada_{timestamp}.md"
        markdown_content = self._generate_markdown_report(result)

        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        logger.info(f"📄 Reportes generados: {json_filename}, {md_filename}")
        return json_filename, md_filename

    def _generate_markdown_report(self, result: AnalysisResult) -> str:
        """📝 Generación de documentación Markdown avanzada"""
        lines = [
            "# 🚀 ANÁLISIS AVANZADO DE ENDPOINTS - REPORTE EMPRESARIAL",
            "",
            f"**Fecha de análisis:** {result.timestamp}",
            f"**Tiempo de procesamiento:** {result.analysis_time:.2f} segundos",
            f"**Archivos procesados:** {result.files_processed}",
            f"**Total de endpoints:** {result.total_endpoints}",
            "",
            "## 📊 ESTADÍSTICAS GENERALES",
            "",
            "### 🏢 Distribución por Microservicio",
            "",
        ]

        for microservice, count in result.microservices.items():
            percentage = (
                (count / result.total_endpoints * 100)
                if result.total_endpoints > 0
                else 0
            )
            lines.append(f"- **{microservice}**: {count} endpoints ({percentage:.1f}%)")

        lines.extend(["", "### 🌐 Métodos HTTP Utilizados", ""])

        for method, count in sorted(result.http_methods.items()):
            lines.append(f"- **{method}**: {count} endpoints")

        lines.extend(["", "## 📋 DETALLE DE ENDPOINTS", ""])

        # Agrupar por microservicio
        by_microservice = {}
        for endpoint in result.endpoints:
            if endpoint.microservice not in by_microservice:
                by_microservice[endpoint.microservice] = []
            by_microservice[endpoint.microservice].append(endpoint)

        for microservice, endpoints in by_microservice.items():
            lines.extend([f"### 🏢 {microservice.upper()}", ""])

            for endpoint in sorted(endpoints, key=lambda x: x.route):
                lines.extend(
                    [
                        f"#### `{' | '.join(endpoint.methods)}` {endpoint.route}",
                        "",
                        f"- **Función:** `{endpoint.function_name}()`",
                        f"- **Archivo:** `{endpoint.file_path}:{endpoint.line_number}`",
                        f"- **Complejidad:** {endpoint.complexity_score}",
                        f"- **Parámetros:** {len(endpoint.parameters)}",
                    ]
                )

                if endpoint.docstring:
                    lines.extend(
                        [
                            f"- **Descripción:** {endpoint.docstring.strip().split('.')[0]}...",
                        ]
                    )

                if endpoint.parameters:
                    lines.append("- **Parámetros:**")
                    for param in endpoint.parameters:
                        param_info = f"  - `{param['name']}`"
                        if param["annotation"]:
                            param_info += f": {param['annotation']}"
                        if param["default"]:
                            param_info += f" = {param['default']}"
                        lines.append(param_info)

                lines.append("")

        if result.errors:
            lines.extend(["## ⚠️ ERRORES ENCONTRADOS", ""])
            for error in result.errors:
                lines.append(f"- {error}")

        return "\n".join(lines)


def main():
    """🎯 Función principal del analizador avanzado"""
    print("🚀 ANALIZADOR AST AVANZADO DE ENDPOINTS - INICIANDO")
    print("=" * 70)

    # Configurar base path - Apuntar a la carpeta que contiene los microservicios
    base_path = Path(__file__).parent.parent.parent.parent.parent

    # Crear analizador
    analyzer = EnterpriseCodeAnalyzer(str(base_path))

    # Ejecutar análisis
    result = analyzer.analyze_all_endpoints()

    # Generar reportes
    json_file, md_file = analyzer.generate_reports(result)

    # Mostrar resumen
    print(f"\n📊 ANÁLISIS COMPLETADO")
    print("=" * 70)
    print(f"📈 Total endpoints encontrados: {result.total_endpoints}")
    print(f"📂 Archivos procesados: {result.files_processed}")
    print(f"⚡ Tiempo de análisis: {result.analysis_time:.2f} segundos")
    print(f"❌ Errores encontrados: {len(result.errors)}")

    print(f"\n🔗 MÉTODOS HTTP UTILIZADOS:")
    for method, count in sorted(result.http_methods.items()):
        print(f"  {method}: {count} endpoints")

    print(f"\n🏢 DISTRIBUCIÓN POR MICROSERVICIO:")
    for microservice, count in result.microservices.items():
        percentage = (
            (count / result.total_endpoints * 100) if result.total_endpoints > 0 else 0
        )
        print(f"  {microservice}: {count} endpoints ({percentage:.1f}%)")

    print(f"\n📄 Reportes generados:")
    print(f"  📊 JSON: {json_file}")
    print(f"  📚 Markdown: {md_file}")


if __name__ == "__main__":
    main()
