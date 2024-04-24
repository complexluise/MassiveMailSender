# Aplicación de Mensajería Masiva

Esta aplicación de mensajería masiva permite enviar correos electrónicos personalizados a una lista de contactos obtenida desde un archivo CSV o desde una hoja de cálculo de Google Sheets.

## Requisitos Previos

Antes de comenzar, asegúrese de tener Python 3.6 o superior instalado en su sistema. También necesitará acceso a una cuenta de Gmail para el envío de correos electrónicos y, si utiliza Google Sheets, acceso a las credenciales de la API de Google.

## Instalación

Para configurar y ejecutar esta aplicación, siga estos pasos:

1. **Clonar el repositorio**

   Abra una terminal y ejecute el siguiente comando para clonar el repositorio:

   ```bash
   git clone https://github.com/su-usuario/mass_messaging_app.git
   cd mass_messaging_app
   ```

2. **Configurar el entorno virtual**

   Es recomendable utilizar un entorno virtual para las dependencias de Python:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows use `venv\Scripts\activate`
   ```

3. **Instalar dependencias**

   Instale todas las dependencias necesarias con pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**

   Copie el archivo de ejemplo `.env.example` a un nuevo archivo llamado `.env` y modifique los valores según sus credenciales y configuración de SMTP:

   ```bash
   cp .env.example .env
   nano .env  # o use otro editor de texto para modificar el archivo
   ```

   Asegúrese de rellenar los siguientes valores:

   - `SMTP_SERVER`: Su servidor SMTP (por ejemplo, para Gmail, `smtp.gmail.com`).
   - `SMTP_PORT`: El puerto utilizado por su servidor SMTP (por ejemplo, `465` para Gmail).
   - `SMTP_USER`: Su correo electrónico de Gmail.
   - `SMTP_PASSWORD`: Contraseña de Aplicación.
   - `GOOGLE_SERVICE_FILE`: Su cuenta de servicio de Google.
   - `GOOGLE_CREDENTIALS_PATH`: La ruta al archivo de credenciales JSON para la API de Google.

## Uso de Contraseñas de Aplicación con Google

Para enviar correos electrónicos a través de SMTP con Gmail de manera segura, es recomendable utilizar una contraseña de aplicación en lugar de su contraseña regular. Esto proporciona un nivel adicional de seguridad y permite que la aplicación acceda a su cuenta de Gmail sin necesidad de exponer su contraseña real.

### Creación de una Contraseña de Aplicación en Gmail

1. **Habilite la verificación en dos pasos**: Antes de poder usar contraseñas de aplicación, debe habilitar la verificación en dos pasos en su cuenta de Google.

   - Visite [la página de verificación en dos pasos de Google](https://myaccount.google.com/security).
   - Haga clic en "Comenzar" y siga las instrucciones para configurar la verificación en dos pasos.

2. **Cree una contraseña de aplicación**:

   - Una vez activada la verificación en dos pasos, regrese a la [página de seguridad de su cuenta](https://myaccount.google.com/security).
   - En la sección "Contraseñas de aplicación", haga clic en "Contraseña de aplicación" o "App passwords".
   - Es posible que tenga que volver a ingresar su contraseña de Gmail.
   - En el menú desplegable "Seleccionar aplicación", elija "Otra (nombre personalizado)" y escriba "Mass Messaging App" o el nombre de su elección.
   - Haga clic en "Generar". Google proporcionará una contraseña de 16 caracteres. Anote esta contraseña, ya que no podrá volver a verla.

3. **Configure su aplicación**:

   - Utilice esta contraseña de aplicación en lugar de su contraseña normal en el archivo `.env` bajo `SMTP_PASSWORD`.
   - Asegúrese de no compartir esta contraseña y de almacenarla de forma segura.

### Ventajas de las Contraseñas de Aplicación

- **Seguridad Mejorada**: Las contraseñas de aplicación son específicas para la aplicación que las usa, lo que significa que si alguna vez se compromete, solo afectará esa aplicación y no tendrá acceso completo a su cuenta de Google.
- **Facilidad de Revocación**: Puede revocar una contraseña de aplicación en cualquier momento sin cambiar su contraseña de Google, lo que hace que sea fácil gestionar y mantener la seguridad.

Al seguir estos pasos, puede configurar su aplicación de mensajería masiva para enviar correos electrónicos de forma segura utilizando el servidor SMTP de Gmail y una contraseña de aplicación.


## Uso

### Enviar Correos desde un Archivo CSV

Para enviar correos desde un archivo CSV, use el siguiente comando:

```bash
python main.py send_mail --contacts_file ./ruta/a/contacts.csv --msg_template ./ruta/a/template.json
```

### Enviar Correos desde Google Sheets

Para enviar correos utilizando datos de Google Sheets, asegúrese de tener las credenciales de la API de Google configuradas correctamente y luego ejecute:

```bash
python main.py send_mail --spreadsheet_id SU_ID_DE_HOJA --range_name 'A1:C2' --msg_template ./ruta/a/template.json
```

### Obtener Credenciales de Google

Si necesita configurar o actualizar sus credenciales para el acceso a Google Sheets, puede utilizar el siguiente comando:

```bash
python main.py get_credentials --service google
```

## Contribuir

Si desea contribuir a este proyecto, por favor considere hacer un fork del repositorio y enviando un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia Creative Commons Attribution-NonCommercial 4.0 International - vea el archivo `LICENSE.md` para más detalles.

MassiveMailSender © 2024 by Luis Higuera is licensed under Creative Commons Attribution-NonCommercial 4.0 International