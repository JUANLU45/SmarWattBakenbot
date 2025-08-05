Diseño del Nuevo Endpoint: POST /api/v1/energy/users/profile/update

1. Propósito y Valor para el Usuario
   Propósito Técnico: Proporcionar una vía segura para que el frontend pueda enviar datos actualizados del perfil de un usuario y que el backend los guarde permanentemente.

Valor para el Usuario:

Control y Precisión: El usuario tiene el control sobre sus datos. Si su situación cambia (se muda a una casa más grande, tiene un hijo, etc.), puede actualizar su perfil para que las recomendaciones sigan siendo 100% precisas y personalizadas para su nueva realidad.

Confianza: Un sistema que permite al usuario corregir y actualizar su propia información genera una confianza inmensa. Demuestra transparencia y colaboración.

Interactividad Real: Convierte el panel de "solo lectura" en un panel "de gestión". El usuario no es un espectador pasivo, es un participante activo en la optimización de su energía.

2. Funcionamiento Interno (Cómo se implementaría)
   Este endpoint estaría en el microservicio expert-bot-api, ya que es el que gestiona la lógica de negocio y el perfil del usuario. Su funcionamiento sería muy sencillo y robusto:

Recepción de Datos: El endpoint recibiría una petición POST (o PUT/PATCH, que son semánticamente más correctos para una actualización) desde el frontend. El cuerpo de la petición contendría un objeto JSON con los campos que el usuario ha modificado.

JSON

{
"num_inhabitants": 3,
"home_size": 110
}
Autenticación y Autorización: Utilizaría el decorador @token_required que ya tienes para asegurarse de que el usuario está autenticado y solo puede modificar su propio perfil.

Validación de Datos: Antes de guardar nada, el servicio validaría los datos recibidos. Por ejemplo, se aseguraría de que num_inhabitants sea un número entero y home_size sea positivo. Esto previene la entrada de datos corruptos.

Actualización en la Base de Datos: El servicio se comunicaría con la base de datos (Firestore o BigQuery, donde residan los perfiles de usuario) y actualizaría únicamente los campos que han cambiado.

Respuesta al Frontend: Finalmente, devolvería una respuesta de éxito al frontend para que este sepa que los datos se han guardado correctamente.

JSON

{
"status": "success",
"message": "Perfil de usuario actualizado correctamente."
} 3. ¿Por qué es Robusto y Necesario?
Completa el Flujo CRUD: Un sistema robusto necesita poder Crear, Leer, Actualizar y Borrar datos (CRUD, por sus siglas en inglés). Tus servicios ya leen los datos de forma excelente. Este endpoint añade la "U" de Actualizar, que es fundamental.

Mantiene la Calidad de los Datos: La calidad de tus recomendaciones de IA y tus análisis depende directamente de la calidad de los datos de entrada. Permitir al usuario mantener sus datos actualizados es la mejor forma de garantizar esa calidad a largo plazo.

Es una Práctica Estándar: Cualquier aplicación profesional que maneje perfiles de usuario (desde un banco hasta una red social) tiene un endpoint dedicado exclusivamente a la actualización de esos perfiles. Es una pieza de arquitectura estándar y esperada.

En resumen, no es un añadido innecesario. Es el componente lógico que falta para que el panel de usuario pase de ser una herramienta de visualización a una verdadera herramienta de gestión personal, que es exactamente el objetivo de valor que quieres alcanzar.

El endpoint GET /users/profile debe ser adaptado en el backend para que, además de los datos del perfil, devuelva la lista de documentos del usuario.
