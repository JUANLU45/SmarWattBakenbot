#!/usr/bin/env python3
"""
Script para generar token de autenticación Firebase
Utiliza las credenciales del service account para crear un token válido
"""

import json
import sys
from pathlib import Path
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account

def generate_firebase_token():
    """Genera un token de autenticación Firebase válido."""
    
    # Ruta al archivo de credenciales
    credentials_path = Path("firebase-adminsdk-fbsvc-key.json")
    
    if not credentials_path.exists():
        print("❌ ERROR: No se encontró firebase-adminsdk-fbsvc-key.json")
        print("   Asegúrate de que el archivo esté en el directorio actual.")
        return None
    
    try:
        # Cargar credenciales del service account
        print("🔑 Cargando credenciales de Firebase...")
        credentials = service_account.Credentials.from_service_account_file(
            str(credentials_path),
            scopes=[
                'https://www.googleapis.com/auth/firebase',
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/userinfo.email'
            ]
        )
        
        # Obtener token de acceso
        print("🚀 Generando token de acceso...")
        request = Request()
        credentials.refresh(request)
        
        token = credentials.token
        
        if not token:
            print("❌ ERROR: No se pudo generar el token")
            return None
        
        print("✅ Token generado exitosamente!")
        print(f"🔐 Token: {token[:50]}...{token[-20:]}")
        print(f"📅 Expira en: {credentials.expiry}")
        
        # Actualizar archivo .env
        update_env_file(token)
        
        return token
        
    except Exception as e:
        print(f"❌ ERROR generando token: {str(e)}")
        return None

def update_env_file(token):
    """Actualiza el archivo .env con el nuevo token."""
    
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ ERROR: No se encontró archivo .env")
        return
    
    try:
        # Leer contenido actual
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Actualizar línea del token
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('AUTH_TOKEN='):
                lines[i] = f'AUTH_TOKEN={token}\n'
                updated = True
                break
        
        # Si no se encontró la línea, agregarla
        if not updated:
            lines.append(f'AUTH_TOKEN={token}\n')
        
        # Escribir archivo actualizado
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print("✅ Archivo .env actualizado con el nuevo token")
        
    except Exception as e:
        print(f"❌ ERROR actualizando .env: {str(e)}")

def main():
    """Función principal."""
    print("🔥 GENERADOR DE TOKEN FIREBASE")
    print("=" * 50)
    
    token = generate_firebase_token()
    
    if token:
        print("\n🎉 ¡TOKEN GENERADO Y CONFIGURADO!")
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Ejecuta: python autonomous_runner.py")
        print("2. El simulador se ejecutará cada 48 horas")
        print("3. Coste máximo: €5/mes")
        print("\n⚠️  IMPORTANTE:")
        print("   - El token expira cada hora")
        print("   - El script lo renovará automáticamente")
        print("   - Monitorea los logs para verificar el funcionamiento")
    else:
        print("\n❌ No se pudo generar el token")
        print("   Verifica que firebase-adminsdk-fbsvc-key.json esté presente")
        sys.exit(1)

if __name__ == "__main__":
    main()
