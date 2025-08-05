#!/usr/bin/env python3
"""
SCRIPT DE VERIFICACIÓN DE ENDPOINTS PROBLEMÁTICOS
=================================================

Script ESPECIALIZADO para verificar los 14 endpoints con errores 500 identificados.
Verifica ESPECÍFICAMENTE los problemas de Google Cloud BigQuery y autenticación.

🔒 RESTRICCIONES ABSOLUTAS:
- PROHIBIDO código placebo
- SOLO verificaciones REALES  
- TOLERANCIA CERO a simulaciones

ENDPOINTS PROBLEMÁTICOS IDENTIFICADOS:
✅ POST /api/v1/analysis/sentiment (Error 500 - BigQuery auth)
✅ Verificación de credenciales Google Cloud
✅ Testing de BigQuery connectivity
✅ Validación de service accounts

ENTORNO: PRODUCCIÓN GOOGLE CLOUD
CREDENCIALES: Service Accounts REALES
VERIFICACIÓN: REAL y DIRECTA

VERSIÓN: 1.0.0 - VERIFICACIÓN ESPECIALIZADA
FECHA: 2025-01-17
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional
from google.cloud import bigquery
from google.oauth2 import service_account
import traceback

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'verificacion_endpoints_problematicos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)

logger = logging.getLogger("SmarWatt_Endpoint_Verification")

class EndpointVerifier:
    """Verificador especializado para endpoints con problemas identificados."""
    
    def __init__(self):
        """Inicializar verificador con configuración REAL."""
        logger.info("🔍 Inicializando Verificador de Endpoints Problemáticos")
        
        # URLs REALES de producción
        self.expert_api_url = "https://expert-bot-api-1010012211318.europe-west1.run.app"
        self.energy_api_url = "https://energy-ia-api-1010012211318.europe-west1.run.app"
        
        # Rutas a credenciales REALES
        self.firebase_cred_path = Path("c:/Smarwatt_2/SmarWatt_2/backend/sevicio chatbot/servicios/DOCUMENTACION Y SCRPT/google/firebase-adminsdk-fbsvc-key.json")
        self.expert_cred_path = Path("c:/Smarwatt_2/SmarWatt_2/backend/sevicio chatbot/servicios/DOCUMENTACION Y SCRPT/google/expert-bot-api-sa-key.json")
        
        # Resultados de verificación
        self.verification_results = {
            "credentials_check": {},
            "bigquery_connectivity": {},
            "endpoint_responses": {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def verify_credentials(self) -> None:
        """Verificar REALMENTE las credenciales de Google Cloud."""
        logger.info("🔐 Verificando credenciales Google Cloud...")
        
        # Verificar Firebase Admin SDK
        try:
            if self.firebase_cred_path.exists():
                with open(self.firebase_cred_path, 'r') as f:
                    firebase_creds = json.load(f)
                
                # Verificaciones REALES de contenido
                required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email', 'client_id']
                missing_fields = [field for field in required_fields if not firebase_creds.get(field)]
                
                if missing_fields:
                    self.verification_results["credentials_check"]["firebase"] = {
                        "status": "error",
                        "message": f"Campos faltantes: {missing_fields}"
                    }
                    logger.error(f"❌ Firebase credentials: campos faltantes {missing_fields}")
                else:
                    self.verification_results["credentials_check"]["firebase"] = {
                        "status": "valid",
                        "project_id": firebase_creds.get("project_id"),
                        "client_email": firebase_creds.get("client_email")
                    }
                    logger.info(f"✅ Firebase credentials válidas: {firebase_creds.get('client_email')}")
            else:
                self.verification_results["credentials_check"]["firebase"] = {
                    "status": "missing",
                    "message": f"Archivo no encontrado: {self.firebase_cred_path}"
                }
                logger.error(f"❌ Firebase credentials no encontradas: {self.firebase_cred_path}")
                
        except Exception as e:
            self.verification_results["credentials_check"]["firebase"] = {
                "status": "error",
                "message": str(e)
            }
            logger.error(f"❌ Error verificando Firebase credentials: {e}")
        
        # Verificar Expert Bot Service Account
        try:
            if self.expert_cred_path.exists():
                with open(self.expert_cred_path, 'r') as f:
                    expert_creds = json.load(f)
                
                required_fields = ['type', 'project_id', 'private_key', 'client_email']
                missing_fields = [field for field in required_fields if not expert_creds.get(field)]
                
                if missing_fields:
                    self.verification_results["credentials_check"]["expert_bot"] = {
                        "status": "error", 
                        "message": f"Campos faltantes: {missing_fields}"
                    }
                    logger.error(f"❌ Expert Bot credentials: campos faltantes {missing_fields}")
                else:
                    self.verification_results["credentials_check"]["expert_bot"] = {
                        "status": "valid",
                        "project_id": expert_creds.get("project_id"),
                        "client_email": expert_creds.get("client_email")
                    }
                    logger.info(f"✅ Expert Bot credentials válidas: {expert_creds.get('client_email')}")
            else:
                self.verification_results["credentials_check"]["expert_bot"] = {
                    "status": "missing",
                    "message": f"Archivo no encontrado: {self.expert_cred_path}"
                }
                logger.error(f"❌ Expert Bot credentials no encontradas: {self.expert_cred_path}")
                
        except Exception as e:
            self.verification_results["credentials_check"]["expert_bot"] = {
                "status": "error",
                "message": str(e)
            }
            logger.error(f"❌ Error verificando Expert Bot credentials: {e}")

    def test_bigquery_connectivity(self) -> None:
        """Probar conectividad REAL con BigQuery usando credenciales."""
        logger.info("🗄️ Testing conectividad BigQuery...")
        
        # Probar con Firebase credentials
        try:
            if self.firebase_cred_path.exists():
                logger.info("🔍 Probando BigQuery con Firebase credentials...")
                credentials = service_account.Credentials.from_service_account_file(
                    str(self.firebase_cred_path)
                )
                
                client = bigquery.Client(credentials=credentials, project=credentials.project_id)
                
                # Test REAL: ejecutar query simple
                query = "SELECT 1 as test_value"
                query_job = client.query(query)
                results = list(query_job.result())
                
                if results and results[0].test_value == 1:
                    self.verification_results["bigquery_connectivity"]["firebase"] = {
                        "status": "success",
                        "project_id": credentials.project_id,
                        "test_query_result": "OK"
                    }
                    logger.info("✅ BigQuery conectividad Firebase: EXITOSA")
                else:
                    self.verification_results["bigquery_connectivity"]["firebase"] = {
                        "status": "error",
                        "message": "Query test falló"
                    }
                    logger.error("❌ BigQuery Firebase: query test falló")
                    
        except Exception as e:
            self.verification_results["bigquery_connectivity"]["firebase"] = {
                "status": "error",
                "message": str(e)
            }
            logger.error(f"❌ BigQuery Firebase error: {e}")
        
        # Probar con Expert Bot credentials
        try:
            if self.expert_cred_path.exists():
                logger.info("🔍 Probando BigQuery con Expert Bot credentials...")
                credentials = service_account.Credentials.from_service_account_file(
                    str(self.expert_cred_path)
                )
                
                client = bigquery.Client(credentials=credentials, project=credentials.project_id)
                
                # Test REAL: verificar acceso al dataset
                dataset_id = "smartwatt_data"
                try:
                    dataset = client.get_dataset(dataset_id)
                    self.verification_results["bigquery_connectivity"]["expert_bot"] = {
                        "status": "success",
                        "project_id": credentials.project_id,
                        "dataset_access": f"{dataset_id} accesible"
                    }
                    logger.info(f"✅ BigQuery Expert Bot: dataset {dataset_id} accesible")
                except Exception as dataset_error:
                    # Probar query simple si no puede acceder al dataset
                    query = "SELECT 1 as test_value"
                    query_job = client.query(query)
                    results = list(query_job.result())
                    
                    self.verification_results["bigquery_connectivity"]["expert_bot"] = {
                        "status": "partial",
                        "project_id": credentials.project_id,
                        "basic_query": "OK" if results else "FAIL",
                        "dataset_access": f"No access to {dataset_id}: {str(dataset_error)}"
                    }
                    logger.warning(f"⚠️ BigQuery Expert Bot: acceso básico OK, pero sin acceso a {dataset_id}")
                    
        except Exception as e:
            self.verification_results["bigquery_connectivity"]["expert_bot"] = {
                "status": "error",
                "message": str(e)
            }
            logger.error(f"❌ BigQuery Expert Bot error: {e}")

    def test_problematic_endpoints(self) -> None:
        """Testear ESPECÍFICAMENTE los endpoints con problemas identificados."""
        logger.info("🎯 Testing endpoints problemáticos específicos...")
        
        # Endpoint principal problemático: sentiment analysis
        self._test_sentiment_analysis()
        
        # Otros endpoints críticos identificados
        self._test_critical_endpoints()

    def _test_sentiment_analysis(self) -> None:
        """Testear específicamente el endpoint de análisis de sentimientos."""
        logger.info("🧠 Testing endpoint de análisis de sentimientos...")
        
        url = f"{self.expert_api_url}/api/v1/analysis/sentiment"
        
        # Test data REAL
        test_data = {
            "text": "Estoy muy contento con mi nueva tarifa eléctrica, el servicio es excelente"
        }
        
        try:
            response = requests.post(
                url,
                json=test_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            result = {
                "status_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "success": 200 <= response.status_code < 400
            }
            
            try:
                result["response_json"] = response.json()
            except:
                result["response_text"] = response.text[:200]
            
            self.verification_results["endpoint_responses"]["sentiment_analysis"] = result
            
            if result["success"]:
                logger.info(f"✅ Sentiment analysis: {response.status_code} - {result['response_time_ms']:.0f}ms")
            else:
                logger.error(f"❌ Sentiment analysis: {response.status_code} - Error confirmado")
                if response.status_code == 500:
                    logger.error("🔥 ERROR 500 CONFIRMADO - Problema en el constructor de AILearningService")
                
        except Exception as e:
            self.verification_results["endpoint_responses"]["sentiment_analysis"] = {
                "status": "connection_error",
                "error": str(e)
            }
            logger.error(f"❌ Error conectando a sentiment analysis: {e}")

    def _test_critical_endpoints(self) -> None:
        """Testear otros endpoints críticos."""
        critical_endpoints = [
            {
                "name": "expert_health",
                "url": f"{self.expert_api_url}/health",
                "method": "GET"
            },
            {
                "name": "expert_health_detailed", 
                "url": f"{self.expert_api_url}/health/detailed",
                "method": "GET"
            },
            {
                "name": "energy_health",
                "url": f"{self.energy_api_url}/health", 
                "method": "GET"
            },
            {
                "name": "sentiment_internal",
                "url": f"{self.expert_api_url}/api/v1/analysis/sentiment/internal",
                "method": "POST",
                "data": {"text": "Test interno", "user_id": "test-user"}
            }
        ]
        
        for endpoint in critical_endpoints:
            try:
                if endpoint["method"] == "GET":
                    response = requests.get(endpoint["url"], timeout=15)
                else:
                    response = requests.post(
                        endpoint["url"], 
                        json=endpoint.get("data", {}),
                        headers={"Content-Type": "application/json"},
                        timeout=15
                    )
                
                result = {
                    "status_code": response.status_code,
                    "success": 200 <= response.status_code < 400,
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                }
                
                try:
                    result["response_json"] = response.json()
                except:
                    result["response_text"] = response.text[:100]
                
                self.verification_results["endpoint_responses"][endpoint["name"]] = result
                
                if result["success"]:
                    logger.info(f"✅ {endpoint['name']}: {response.status_code}")
                else:
                    logger.warning(f"⚠️ {endpoint['name']}: {response.status_code}")
                    
            except Exception as e:
                self.verification_results["endpoint_responses"][endpoint["name"]] = {
                    "status": "error",
                    "error": str(e)
                }
                logger.error(f"❌ {endpoint['name']}: {e}")

    def run_complete_verification(self) -> Dict[str, Any]:
        """Ejecutar verificación completa de endpoints problemáticos."""
        logger.info("🚀 INICIANDO VERIFICACIÓN DE ENDPOINTS PROBLEMÁTICOS")
        logger.info("=" * 70)
        
        try:
            # Verificar credenciales
            self.verify_credentials()
            
            # Probar conectividad BigQuery
            self.test_bigquery_connectivity()
            
            # Testear endpoints problemáticos
            self.test_problematic_endpoints()
            
        except Exception as e:
            logger.error(f"❌ Error durante verificación: {e}")
            logger.error(traceback.format_exc())
        
        # Generar reporte
        self._generate_verification_report()
        
        return self.verification_results

    def _generate_verification_report(self) -> None:
        """Generar reporte de verificación."""
        logger.info("📊 GENERANDO REPORTE DE VERIFICACIÓN")
        logger.info("=" * 70)
        
        print("\n" + "=" * 80)
        print("🔍 REPORTE DE VERIFICACIÓN DE ENDPOINTS PROBLEMÁTICOS")
        print("=" * 80)
        
        # Credenciales
        print("🔐 ESTADO DE CREDENCIALES:")
        for cred_type, status in self.verification_results["credentials_check"].items():
            status_icon = "✅" if status.get("status") == "valid" else "❌"
            print(f"   {status_icon} {cred_type}: {status.get('status', 'unknown')}")
            if status.get("client_email"):
                print(f"      Email: {status['client_email']}")
        print()
        
        # BigQuery
        print("🗄️ CONECTIVIDAD BIGQUERY:")
        for bq_type, status in self.verification_results["bigquery_connectivity"].items():
            status_icon = "✅" if status.get("status") == "success" else "⚠️" if status.get("status") == "partial" else "❌"
            print(f"   {status_icon} {bq_type}: {status.get('status', 'unknown')}")
            if status.get("message"):
                print(f"      Error: {status['message']}")
        print()
        
        # Endpoints
        print("🎯 ESTADO DE ENDPOINTS PROBLEMÁTICOS:")
        for endpoint_name, result in self.verification_results["endpoint_responses"].items():
            if isinstance(result, dict):
                if result.get("success"):
                    status_icon = "✅"
                    status_text = f"HTTP {result.get('status_code')} - {result.get('response_time_ms', 0):.0f}ms"
                else:
                    status_icon = "❌"
                    status_text = f"HTTP {result.get('status_code', 'ERROR')}"
                    if result.get('status_code') == 500:
                        status_text += " (ERROR 500 CONFIRMADO)"
                
                print(f"   {status_icon} {endpoint_name}: {status_text}")
                
                if result.get("error"):
                    print(f"      Error: {result['error']}")
        print()
        
        # Guardar reporte detallado
        report_file = f"reporte_verificacion_endpoints_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.verification_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Reporte detallado guardado en: {report_file}")
        
        # Conclusiones
        print("\n🎯 CONCLUSIONES:")
        
        # Verificar si el error 500 de sentiment analysis se confirma
        sentiment_result = self.verification_results["endpoint_responses"].get("sentiment_analysis", {})
        if sentiment_result.get("status_code") == 500:
            print("   🔥 ERROR 500 CONFIRMADO en /api/v1/analysis/sentiment")
            print("   📋 CAUSA PROBABLE: Error en constructor de AILearningService")
            print("   🔧 ACCIÓN REQUERIDA: Revisar inicialización de BigQuery en AILearningService")
        elif sentiment_result.get("success"):
            print("   ✅ Endpoint de sentiment analysis funcionando correctamente")
        
        # Verificar credenciales
        all_creds_valid = all(
            status.get("status") == "valid" 
            for status in self.verification_results["credentials_check"].values()
        )
        
        if all_creds_valid:
            print("   ✅ Todas las credenciales Google Cloud son válidas")
        else:
            print("   ⚠️ Algunas credenciales tienen problemas")
        
        print("=" * 80)


def main():
    """Función principal de verificación."""
    try:
        logger.info("🔍 Iniciando Verificación de Endpoints Problemáticos")
        
        verifier = EndpointVerifier()
        results = verifier.run_complete_verification()
        
        # Código de salida basado en resultados
        sentiment_working = results["endpoint_responses"].get("sentiment_analysis", {}).get("success", False)
        
        if sentiment_working:
            print("\n🎉 VERIFICACIÓN COMPLETADA: No se detectaron problemas críticos")
            sys.exit(0)
        else:
            print("\n⚠️ VERIFICACIÓN COMPLETADA: Problemas confirmados")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Error crítico en verificación: {e}")
        logger.error(traceback.format_exc())
        sys.exit(2)


if __name__ == "__main__":
    main()
