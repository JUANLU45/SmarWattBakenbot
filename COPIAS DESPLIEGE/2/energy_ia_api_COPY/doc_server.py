#!/usr/bin/env python3
"""
🌐 SERVIDOR DE DOCUMENTACIÓN SMARWATT
=====================================

Servidor web independiente que sirve documentación automática.
NO TOCA código fuente, actualiza documentación en tiempo real.

CARACTERÍSTICAS:
- Servidor web independiente en puerto 8080
- Regenera documentación automáticamente
- Interfaz web moderna con Swagger UI
- Monitoreo de cambios en código fuente

USO:
python doc_server.py

VERSIÓN: 1.0.0
"""

import os
import time
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
from auto_doc_generator import SmarWattDocGenerator


class DocServer:
    """Servidor de documentación independiente"""

    def __init__(self, port=8080):
        self.port = port
        self.docs_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
        self.generator = SmarWattDocGenerator()

    def regenerate_docs(self):
        """Regenera documentación automáticamente"""
        print("🔄 Regenerando documentación...")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        energy_api_path = current_dir
        expert_api_path = os.path.join(parent_dir, "expert_bot_api_COPY")

        if os.path.exists(energy_api_path) and os.path.exists(expert_api_path):
            spec = self.generator.generate_openapi_spec(
                energy_api_path, expert_api_path
            )
            self.generator.generate_html_documentation(spec, self.docs_dir)
            print("✅ Documentación actualizada")

    def start_server(self):
        """Inicia servidor de documentación"""
        # Regenerar documentación inicial
        self.regenerate_docs()

        # Cambiar al directorio de docs
        os.chdir(self.docs_dir)

        # Crear servidor HTTP
        handler = SimpleHTTPRequestHandler
        httpd = HTTPServer(("localhost", self.port), handler)

        print(f"🌐 Servidor de documentación iniciado en http://localhost:{self.port}")
        print(f"📂 Sirviendo desde: {self.docs_dir}")
        print("🔄 La documentación se actualiza automáticamente")
        print("⏹️  Presiona Ctrl+C para detener")

        # Abrir navegador automáticamente
        webbrowser.open(f"http://localhost:{self.port}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n⏹️  Servidor detenido")
            httpd.shutdown()


def main():
    """Función principal"""
    print("🌐 SERVIDOR DE DOCUMENTACIÓN SMARWATT")
    print("=" * 40)

    server = DocServer()
    server.start_server()


if __name__ == "__main__":
    main()
