#!/usr/bin/env python3
"""
Script para verificar y actualizar los datos del usuario principal de test
para que tenga datos completos necesarios para las recomendaciones ML.
"""

import os
import sys
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import random

# Configuración Firebase
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "smatwatt",
    "private_key_id": "b45b1234567890abcdef1234567890abcdef1234",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC5...\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-xyz@smatwatt.iam.gserviceaccount.com",
    "client_id": "123456789012345678901",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/v1/metadata/x509/firebase-adminsdk-xyz%40smatwatt.iam.gserviceaccount.com"
})

# Inicializar Firebase solo si no está ya inicializado
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_user_uid_by_email(email):
    """Obtener UID del usuario por email (simulado)"""
    # Para simplificar, usaremos un UID conocido del usuario principal
    # En un entorno real, necesitarías la Auth API para obtener el UID real
    return "juanluvaldi_uid_123456"  # UID simulado

def verificar_datos_usuario(user_uid):
    """Verificar qué datos tiene el usuario"""
    print(f"🔍 Verificando datos del usuario: {user_uid}")
    
    try:
        # Verificar documento del usuario
        user_doc = db.collection('users').document(user_uid).get()
        if not user_doc.exists:
            print("❌ El usuario no existe en Firestore")
            return None
        
        user_data = user_doc.to_dict()
        print("📄 Datos del usuario:")
        print(json.dumps(user_data, indent=2, ensure_ascii=False, default=str))
        
        # Verificar historial de facturas
        facturas_ref = db.collection('users').document(user_uid).collection('facturas')
        facturas = facturas_ref.get()
        
        print(f"\n📊 Número de facturas: {len(facturas)}")
        
        if facturas:
            # Analizar facturas existentes
            tiene_campos_criticos = False
            for i, factura in enumerate(facturas[:3]):  # Solo mostrar las primeras 3
                factura_data = factura.to_dict()
                print(f"\n📋 Factura {i+1}:")
                print(f"  - ID: {factura.id}")
                print(f"  - avg_kwh: {'✅' if 'avg_kwh' in factura_data else '❌'}")
                print(f"  - contracted_power_kw: {'✅' if 'contracted_power_kw' in factura_data else '❌'}")
                print(f"  - peak_percent: {'✅' if 'peak_percent' in factura_data else '❌'}")
                
                if 'avg_kwh' in factura_data and 'contracted_power_kw' in factura_data and 'peak_percent' in factura_data:
                    tiene_campos_criticos = True
            
            return {
                'user_data': user_data,
                'num_facturas': len(facturas),
                'tiene_campos_criticos': tiene_campos_criticos
            }
        else:
            print("❌ No hay facturas para este usuario")
            return {
                'user_data': user_data,
                'num_facturas': 0,
                'tiene_campos_criticos': False
            }
    
    except Exception as e:
        print(f"❌ Error verificando datos: {e}")
        return None

def generar_factura_completa():
    """Generar una factura con todos los campos requeridos para ML"""
    ahora = datetime.now()
    periodo_inicio = ahora.replace(day=1) - timedelta(days=30)
    periodo_fin = ahora.replace(day=1) - timedelta(days=1)
    
    # Datos realistas para España 2025
    contracted_power = round(random.uniform(3.45, 5.75), 2)  # kW típicos vivienda
    avg_kwh = round(random.uniform(180, 320), 2)  # kWh/mes típicos
    peak_percent = round(random.uniform(25, 45), 1)  # % consumo en punta
    
    factura = {
        'periodo_facturacion': {
            'inicio': periodo_inicio.isoformat(),
            'fin': periodo_fin.isoformat()
        },
        'datos_consumo': {
            'consumo_kwh': avg_kwh,
            'avg_kwh': avg_kwh,
            'contracted_power_kw': contracted_power,
            'peak_percent': peak_percent,
            'potencia_contratada': f"{contracted_power} kW",
            'tipo_tarifa': '2.0TD',
            'discriminacion_horaria': True
        },
        'costos': {
            'termino_energia': round(avg_kwh * 0.15, 2),
            'termino_potencia': round(contracted_power * 3.85 * 30, 2),
            'impuestos': round(avg_kwh * 0.15 * 0.21, 2),
            'total': round((avg_kwh * 0.15 + contracted_power * 3.85 * 30) * 1.21, 2)
        },
        'recomendaciones_ml': {
            'tarifa_recomendada': '2.0TD' if contracted_power <= 5.0 else '3.0TD',
            'ahorro_estimado': round(random.uniform(15, 45), 2),
            'motivo': 'Optimización basada en patrón de consumo'
        },
        'timestamp': ahora.isoformat(),
        'procesada_ml': True
    }
    
    return factura

def actualizar_usuario_principal(user_uid):
    """Actualizar el usuario principal con datos completos"""
    print(f"🔄 Actualizando datos del usuario: {user_uid}")
    
    try:
        # Actualizar datos del usuario
        user_data = {
            'email': 'juanluvaldi@gmail.com',
            'nombre': 'Juan Luis Valdés',
            'tipo_usuario': 'premium',
            'fecha_registro': datetime.now().isoformat(),
            'perfil_consumo': {
                'tipo_vivienda': 'piso',
                'habitantes': 3,
                'superficie_m2': 85,
                'tiene_calefaccion_electrica': False,
                'vehiculo_electrico': False
            },
            'configuracion': {
                'notificaciones': True,
                'recomendaciones_ml': True,
                'compartir_datos': True
            }
        }
        
        db.collection('users').document(user_uid).set(user_data, merge=True)
        print("✅ Datos del usuario actualizados")
        
        # Generar 3 facturas con datos completos
        for i in range(3):
            factura = generar_factura_completa()
            factura_id = f"factura_{datetime.now().strftime('%Y%m')}-{i+1:02d}"
            
            db.collection('users').document(user_uid).collection('facturas').document(factura_id).set(factura)
            print(f"✅ Factura {i+1} insertada: {factura_id}")
        
        print("🎉 Usuario principal actualizado con datos completos para ML")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando usuario: {e}")
        return False

def main():
    print("🔧 VERIFICACIÓN Y ACTUALIZACIÓN DEL USUARIO PRINCIPAL")
    print("=" * 60)
    
    email_principal = "juanluvaldi@gmail.com"
    user_uid = get_user_uid_by_email(email_principal)
    
    # Verificar datos actuales
    datos_actuales = verificar_datos_usuario(user_uid)
    
    if datos_actuales is None:
        print("❌ No se pudieron obtener los datos del usuario")
        return
    
    # Determinar si necesita actualización
    necesita_actualizacion = (
        datos_actuales['num_facturas'] == 0 or 
        not datos_actuales['tiene_campos_criticos']
    )
    
    if necesita_actualizacion:
        print(f"\n⚠️  El usuario necesita datos actualizados")
        print(f"   - Facturas: {datos_actuales['num_facturas']}")
        print(f"   - Campos críticos ML: {'✅' if datos_actuales['tiene_campos_criticos'] else '❌'}")
        
        respuesta = input("\n¿Deseas actualizar los datos del usuario principal? (s/n): ")
        if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            if actualizar_usuario_principal(user_uid):
                print("\n🎯 ¡ÉXITO! Usuario principal actualizado")
                print("Ahora puedes ejecutar los tests de endpoints")
            else:
                print("\n❌ Error actualizando el usuario")
        else:
            print("\n⏭️  Actualización cancelada")
    else:
        print(f"\n✅ El usuario ya tiene datos suficientes para ML")
        print(f"   - Facturas: {datos_actuales['num_facturas']}")
        print(f"   - Campos críticos ML: ✅")

if __name__ == "__main__":
    main()
