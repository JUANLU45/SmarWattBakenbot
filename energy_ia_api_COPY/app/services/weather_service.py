# energy_ia_api_COPY/app/services/weather_service.py
# 🌦️ SERVICIO PARA INTEGRACIÓN CON OPENWEATHERMAP Y GENERACIÓN DE CONSEJOS

import logging
import requests
from flask import current_app
from typing import Dict, Any

from utils.error_handlers import AppError
from expert_bot_api_COPY.utils.auth_client import get_service_to_service_token

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Servicio para obtener datos climáticos y generar consejos energéticos contextuales.
    """

    def __init__(self):
        self.api_key = current_app.config.get("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise AppError("La clave de API para OpenWeatherMap no está configurada.", 500)
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.expert_bot_api_url = current_app.config["EXPERT_BOT_API_URL"]

    def get_weather_based_advice(self, user_id: str) -> Dict[str, Any]:
        """
        Orquesta la obtención de datos del perfil, datos del clima y la generación de consejos.
        """
        user_profile = self._get_user_profile(user_id)
        postal_code = user_profile.get("last_invoice_data_json", {}).get("codigo_postal")
        if not postal_code:
            raise AppError("No se encontró un código postal en el perfil del usuario para obtener datos climáticos.", 404)

        weather_data = self._get_weather_data(postal_code)
        advice = self._generate_advice(user_profile, weather_data)
        
        return advice

    def _get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Obtiene el perfil del usuario de forma segura desde expert_bot_api."""
        try:
            profile_endpoint = f"{self.expert_bot_api_url}/users/profile"
            auth_token = get_service_to_service_token(audience_url=self.expert_bot_api_url)
            headers = {"Authorization": f"Bearer {auth_token}"}
            
            response = requests.get(profile_endpoint, headers=headers, params={"user_id": user_id}, timeout=10)
            response.raise_for_status()
            return response.json().get("data", {})
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener el perfil del usuario {user_id}: {e}")
            raise AppError("No se pudo obtener el perfil del usuario para el consejo contextual.", 503)

    def _get_weather_data(self, postal_code: str) -> Dict[str, Any]:
        """Llama a la API de OpenWeatherMap."""
        try:
            params = {
                "zip": f"{postal_code},ES",
                "appid": self.api_key,
                "units": "metric",
                "lang": "es"
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al llamar a OpenWeatherMap API para el código postal {postal_code}: {e}")
            raise AppError("El servicio de datos climáticos no está disponible en este momento.", 503)

    def _generate_advice(self, user_profile: Dict[str, Any], weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera un consejo basado en el perfil y el clima."""
        temp = weather_data.get("main", {}).get("temp", 20)
        condition = weather_data.get("weather", [{}])[0].get("main", "").lower()
        
        title = "Consejo Energético Personalizado"
        message = "Mantén tus hábitos de consumo actuales. ¡Lo estás haciendo bien!"
        estimated_impact_percent = 0

        # Lógica para olas de calor
        if temp > 30:
            title = "¡Ola de Calor! Optimiza tu Aire Acondicionado"
            message = (
                f"Detectamos una temperatura de {temp}°C en tu zona. "
                "Se prevé un aumento en tu consumo por el aire acondicionado. "
                "Te recomendamos ajustarlo a 24-25°C para un balance óptimo entre confort y ahorro."
            )
            estimated_impact_percent = 15 # Aumento del 15%

        # Lógica para frentes fríos
        elif temp < 10:
            title = "¡Bajas Temperaturas! Optimiza tu Calefacción"
            message = (
                f"Detectamos una temperatura de {temp}°C en tu zona. "
                "El uso de la calefacción podría disparar tu factura. "
                "Asegúrate de tener un buen aislamiento y ajusta el termostato a 19-21°C."
            )
            estimated_impact_percent = 20 # Aumento del 20%
            
        # Lógica para días de lluvia (si el usuario tiene secadora)
        elif "rain" in condition and user_profile.get("has_dryer"):
             title = "Día Lluvioso: Uso Eficiente de la Secadora"
             message = "Hoy es un día lluvioso. Si usas la secadora, asegúrate de centrifugar bien la ropa y limpiar los filtros para reducir el consumo."
             estimated_impact_percent = 5

        return {
            "title": title,
            "message": message,
            "estimated_impact_percent": estimated_impact_percent,
            "current_weather": {
                "temperature_celsius": temp,
                "condition": condition,
                "location": weather_data.get("name")
            }
        }
