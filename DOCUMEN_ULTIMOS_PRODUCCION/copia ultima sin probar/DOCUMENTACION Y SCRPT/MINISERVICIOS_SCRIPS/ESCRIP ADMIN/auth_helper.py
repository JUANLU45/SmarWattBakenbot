#!/usr/bin/env python3
"""
🔐 MÓDULO DE AUTENTICACIÓN REAL - FIREBASE
=========================================

PROPÓSITO: Generar tokens reales de Firebase para testing de endpoints
URL FIREBASE: https://smatwatt.firebaseapp.com
"""

import os
import json
import requests
import firebase_admin
from firebase_admin import credentials, auth
from datetime import datetime, timedelta


class SmarWattAuth:
    """Autenticador real para SmarWatt con Firebase"""

    def __init__(self, firebase_key_path=None):
        if not firebase_key_path:
            firebase_key_path = os.path.join(
                os.path.dirname(__file__), "..", "firebase-adminsdk-fbsvc-key.json"
            )

        # Inicializar Firebase solo si no está ya inicializado
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_key_path)
            firebase_admin.initialize_app(cred)

        print(f"🔐 Firebase inicializado correctamente")

    def _custom_token_to_id_token(self, custom_token):
        """Convertir custom token a ID token usando Firebase REST API"""
        try:
            # Firebase REST API para intercambiar custom token por ID token
            url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken"
            params = {
                "key": "AIzaSyADn923Z6fKnEF2r-J2Ym1FkSWjWdXlxjw"
            }  # Firebase Web API Key correcta

            payload = {"token": custom_token, "returnSecureToken": True}

            response = requests.post(url, params=params, json=payload)
            response.raise_for_status()

            data = response.json()
            return data.get("idToken")

        except Exception as e:
            print(f"❌ Error convirtiendo a ID token: {e}")
            return custom_token  # Fallback al custom token

    def create_test_user_token(self, email="testuser@smarwatt.com", uid=None):
        """Crear token real de usuario para testing"""
        try:
            if not uid:
                uid = f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Crear custom token real
            custom_token = auth.create_custom_token(
                uid,
                {
                    "email": email,
                    "testing": True,
                    "created_at": datetime.now().isoformat(),
                },
            )

            # Convertir custom token a ID token
            id_token = self._custom_token_to_id_token(custom_token.decode("utf-8"))

            print(f"✅ Token creado para UID: {uid}")
            return id_token, uid

        except Exception as e:
            print(f"❌ Error creando token: {e}")
            return None, None

    def get_production_user_token(self, user_uid="juanluvaldi_uid_123456"):
        """Obtener token de usuario real de producción"""
        try:
            # Para usuario real existente
            custom_token = auth.create_custom_token(
                user_uid,
                {
                    "production_user": True,
                    "verified": True,
                    "test_session": datetime.now().isoformat(),
                },
            )

            # Convertir custom token a ID token
            id_token = self._custom_token_to_id_token(custom_token.decode("utf-8"))

            print(f"✅ Token de producción para UID: {user_uid}")
            return id_token

        except Exception as e:
            print(f"❌ Error creando token de producción: {e}")
            return None


def get_auth_headers(token_type="test"):
    """Obtener headers de autenticación para requests"""
    auth_helper = SmarWattAuth()

    if token_type == "production":
        token = auth_helper.get_production_user_token()
    else:
        token, uid = auth_helper.create_test_user_token()

    if token:
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    else:
        # Fallback token para testing básico
        return {
            "Authorization": "Bearer test_token_fallback",
            "Content-Type": "application/json",
        }


if __name__ == "__main__":
    print("🔐 TESTING AUTENTICACIÓN FIREBASE")

    auth_helper = SmarWattAuth()

    # Test token creation
    token, uid = auth_helper.create_test_user_token("test@smarwatt.com")
    if token:
        print(f"✅ Token de test: {token[:50]}...")

    # Production token
    prod_token = auth_helper.get_production_user_token()
    if prod_token:
        print(f"✅ Token de producción: {prod_token[:50]}...")
