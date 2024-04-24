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

## Preparación de Archivos para el Envío de Mensajes

Para utilizar la aplicación de mensajería masiva, necesitarás preparar dos tipos de archivos:

1. **Archivo de Contactos**: Este es un archivo CSV que contiene los datos de los contactos a quienes deseas enviar el mensaje. Debes asegurarte de que este archivo esté correctamente formateado y contenga todas las columnas necesarias para tu plantilla de mensaje.

2. **Archivo de Plantilla de Mensaje**: Este es un archivo JSON que contiene la plantilla del mensaje que se enviará. Las variables utilizadas en esta plantilla deben coincidir exactamente con los nombres de las columnas en tu archivo CSV de contactos.

### Creación del Archivo de Contactos

El archivo CSV de contactos debe incluir todas las columnas que necesitarás en tu mensaje. Por ejemplo, si tu plantilla de mensaje hace referencia a `{{name}}`, `{{email}}` y `{{phone}}`, tu archivo CSV debe incluir estas columnas exactamente con esos encabezados.

**Ejemplo de archivo CSV:**

```plaintext
name,email,phone
Alice Johnson,alice@example.com,555-0100
Bob Smith,bob@example.com,555-0101
```

### Creación del Archivo de Plantilla de Mensaje

Debes crear un archivo JSON que defina el sujeto y el cuerpo del mensaje, utilizando las variables que corresponden a las columnas de tu archivo de contactos. 

**Ejemplo de archivo de plantilla (template.json):**

```json
{
  "subject": "Hello {{name}}",
  "body": "Dear {{name}},\nYour contact email is {{email}} and your phone number is {{phone}}.\nBest regards."
}
```

### Uso de Variables Consistentes

Es crucial que las variables utilizadas en la plantilla del mensaje (`{{name}}`, `{{email}}`, `{{phone}}` en el ejemplo) coincidan exactamente con los encabezados de las columnas en el archivo CSV. Cualquier discrepancia en el nombre de las variables resultará en errores o en datos incorrectamente mapeados en los mensajes enviados.

### Instrucciones de Uso

Una vez que tengas listos tus archivos de contactos y de plantilla, puedes ejecutar la aplicación utilizando los comandos especificados en la sección de Uso de este documento. Asegúrate de especificar correctamente las rutas a tus archivos de contactos y plantilla cuando utilices los comandos de la aplicación.


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