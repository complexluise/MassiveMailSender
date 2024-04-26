# Aplicación de Mensajería Masiva

Esta aplicación de mensajería masiva permite enviar correos electrónicos personalizados a una lista de contactos obtenida desde un archivo CSV.

## Requisitos Previos

Antes de comenzar, asegúrese de tener Python 3.10 o superior instalado en su sistema y acceso a una cuenta de Gmail para el envío de correos electrónicos.

## Instalación

Para configurar y ejecutar esta aplicación, siga estos pasos:

1. **Clonar el repositorio**

   Abra una terminal y ejecute el siguiente comando para clonar el repositorio:

   ```bash
   git clone https://github.com/complexluise/MassiveMailSender.git
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
   - `SMTP_PASSWORD`: Su Contraseña de Aplicación.

## Uso de Contraseñas de Aplicación con Google

Para enviar correos electrónicos a través de SMTP con Gmail de manera segura, es recomendable utilizar una **contraseña de aplicación** en lugar de su contraseña regular. Esto proporciona un nivel adicional de seguridad y permite que la aplicación acceda a su cuenta de Gmail sin necesidad de exponer su contraseña real.

### Creación de una Contraseña de Aplicación en Gmail

1. **Habilite la verificación en dos pasos**: Antes de poder usar contraseñas de aplicación, debe habilitar la verificación en dos pasos en su cuenta de Google.

   - Visite [la página de seguridad](https://myaccount.google.com/security).
   - En la sección "Acceso a Google", selecciona Verificación en 2 pasos y siga las instrucciones para configurar la verificación en dos pasos.

2. **Cree una contraseña de aplicación**:

   - Una vez activada la verificación en dos pasos, regrese a la [página de seguridad de su cuenta](https://myaccount.google.com/security).
   - En el buscador escriba "Contraseñas de aplicación", y haga clic en "Contraseña de aplicación"
   - Es posible que tenga que volver a ingresar su contraseña de Gmail.
   - En el menú desplegable "Seleccionar aplicación", elija "Otra (nombre personalizado)" y escriba "Mass Messaging App" o el nombre de su elección.
   - Haga clic en "Generar". Google proporcionará una contraseña de 16 caracteres. Anote esta contraseña, ya que no podrá volver a verla.

3. **Configure su aplicación**:

   - Utilice esta contraseña de aplicación en lugar de su contraseña normal en el archivo `.env` bajo `SMTP_PASSWORD`.
   - Asegúrese de no compartir esta contraseña y de almacenarla de forma segura.

## Preparación de Archivos para el Envío de Mensajes

Necesitará un archivo CSV con los detalles de contacto y un archivo JSON para la plantilla del mensaje.

### Creación del Archivo de Contactos

Prepare un archivo CSV con los contactos. Asegúrese de que las columnas coincidan con las variables utilizadas en su plantilla de mensaje.

**Ejemplo de archivo CSV:**

```plaintext
name,email,phone
Alice Johnson,alice@example.com,555-0100
Bob Smith,bob@example.com,555-0101
```

### Creación del Archivo de Campaña

Cree un archivo JSON que contenga la configuración de la campaña. Las variables en la plantilla deben coincidir con las columnas del archivo CSV.

**Ejemplo de archivo de campaña (campaign.json):**

```json
{
  "name": "Example",
  "objective_campain": "Show JSON schema of campaign",
  "subject": "Hello, {{ name }}",
  "body_file": "example.html",
   "attachment_file": "example.pdf"
}
```

* **name**: Un identificador o nombre para la campaña. Esto ayuda a organizar y referenciar la campaña dentro de otros sistemas o registros.
* **objective_campain**: Descripción breve del objetivo de la campaña. Esto puede ser útil para clarificar la intención detrás de la campaña, como informar a los clientes sobre una nueva oferta, reactivar usuarios inactivos, etc.
* **subject**: Asunto del email que será enviado. Este campo puede incluir variables que serán reemplazadas con datos específicos de cada destinatario, como {{ name }}, para personalizar cada mensaje.
* **body_file**: Nombre del archivo HTML que contiene el cuerpo del correo electrónico. Este archivo debe estar diseñado para ser compatible con el formato de email y debería estar preparado para incluir variables dinámicas que se rellenarán en el momento del envío.
* **attachment_file**: Nombre del archivo que contiene el archivo adjunto que se enviara. Este parametro es opcional si no hay un adjunto no se deberia colocar.

### Creación de la plantilla
Cree un archivo con la plantilla del mensaje en HTML (Si no sabe qué es HTML o como usarlo para personalizar los mensajes pidale ayuda a chatGPT （￣︶￣）↗)

Aquí va un ejemplo del archivo
```html
<html>
   <head>
      <style>
        body {font-family: Arial, sans-serif;}
        p {font-size: 14px;}
      </style>
   </head>
   <body>
     <p>Dear {{ name }},<br>
     This is your personalized message!</p>
   </body>
</html>

```


### Uso de Variables Consistentes

Es crucial que las variables utilizadas en la plantilla del mensaje (`{{name}}`, `{{email}}`, `{{phone}}` en el ejemplo) coincidan exactamente con los encabezados de las columnas en el archivo CSV. Cualquier discrepancia en el nombre de las variables resultará en errores o en datos incorrectamente mapeados en los mensajes enviados.

### Instrucciones de Uso

Una vez que tengas listos tus archivos de contactos y de plantilla, puedes ejecutar la aplicación utilizando los comandos especificados en la sección de Uso de este documento. Asegúrate de especificar correctamente las rutas a tus archivos de contactos y plantilla cuando utilices los comandos de la aplicación.

Para enviar correos desde un archivo CSV, utilice el siguiente comando:

```bash
python main.py send_mail --contacts_file ./contacts/contacts.csv --campaign ./ruta/a/campaign.json
```

## Contribuir

Para contribuir a este proyecto, haga un fork del repositorio y envíe un pull request con sus cambios.

## Roadmap
Para las siguientes versiones de la APP se espera.
* Usar inteligencia artificial generativa para personalizar los mensajes a un mayor nivel.
* Hacer pruebas unitarias.
* Cambiar nombre por algo más cool.
* Volver una aplicación pipx
* Usar [HyperModernPython](https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769)
* Hacer Frontend.
* Mejorar Logs.

## Licencia

Este proyecto está licenciado bajo la Licencia Creative Commons Attribution-NonCommercial 4.0 International. Consulte el archivo `LICENSE.md` para más detalles.

MassiveMailSender © 2024 by Luis Higuera is licensed under Creative Commons Attribution-NonCommercial 4.0 International
