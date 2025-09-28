# Siigo Invoice CLI

Una herramienta de línea de comandos para crear facturas de compra en Siigo a partir de archivos Excel.

## 📋 Descripción

Este CLI permite:
- Importar datos de facturas desde un archivo Excel
- Validar los datos según el esquema de Siigo
- Crear facturas de compra en la API de Siigo de forma interactiva o automatizada
- Soporte para credenciales vía variables de entorno, flags de comando o prompts interactivos

## 🔧 Requisitos

- Node.js (o Bun para desarrollo)
- Un archivo Excel con datos de facturas
- Credenciales de Siigo (username, access key, partner ID)

## 🚀 Instalación

1. **Clona o descarga el proyecto:**
   ```bash
   git clone <url-del-repositorio>
   cd CargaFacturas/js
   ```

2. **Instala las dependencias:**
   ```bash
   bun install
   # o npm install
   ```

3. **Construye el proyecto:**
   ```bash
   bun run build
   ```

4. **Construye el ejecutable (opcional):**
   ```bash
   bun run build:exe  # Para el sistema actual
   bun run build:all  # Para todos los sistemas operativos
   ```

## 📖 Uso

### Modo Interactivo
```bash
bun run src/cli.ts
```
El CLI te pedirá:
- Usuario de Siigo
- Clave de acceso
- ID de partner
- Ruta al archivo Excel
- Número de facturas a crear

### Con Flags de Comando
```bash
bun run src/cli.ts --username miusuario --access-key miclave --partner-id miid --file-path /ruta/al/archivo.xlsx
```

### Con Variables de Entorno
```bash
export SIIGO_USERNAME=miusuario
export SIIGO_ACCESS_KEY=miclave
export SIIGO_PARTNER_ID=miid
export EXCEL_FILE_PATH=/ruta/al/archivo.xlsx
bun run src/cli.ts
```

### Con Ejecutable
```bash
./dist/siigo-invoice --username miusuario --access-key miclave --partner-id miid --file-path /ruta/al/archivo.xlsx
```

## 🔑 Configuración

### Credenciales de Siigo
Necesitas obtener estas credenciales de tu cuenta de Siigo:
- **Username**: Tu nombre de usuario en Siigo
- **Access Key**: Clave de acceso de la API
- **Partner ID**: ID de partner proporcionado por Siigo

### Formato del Archivo Excel
El archivo Excel debe contener columnas como:
- `Tipo de documento`
- `CUFE/CUDE`
- `Folio`
- `Prefijo`
- `Divisa`
- `Fecha Emisión`
- `NIT Emisor`
- `Nombre Emisor`
- Y otras columnas de impuestos y totales

## 📝 Ejemplos

### Ejemplo 1: Modo Interactivo
```bash
$ bun run src/cli.ts
🚀 Siigo Invoice CLI - Starting invoice creation process...

? Enter your Siigo username: › miusuario
? Enter your Siigo access key: › [oculto]
? Enter your Siigo partner ID: › miid
? Enter the path to your Excel file: › /home/user/facturas.xlsx
? How many invoices do you want to create? (1-100) › 10

Imported 100 rows from Excel.
Valid invoices: 95
Invalid invoices: 5
Creating 10 invoices...
✅ Created invoice for row 1
...
Process completed.
```

### Ejemplo 2: Con Flags
```bash
bun run src/cli.ts --username miusuario --access-key miclave --partner-id miid --file-path ./facturas.xlsx
```

### Ejemplo 3: Variables de Entorno
```bash
export SIIGO_USERNAME=miusuario
export SIIGO_ACCESS_KEY=miclave
export SIIGO_PARTNER_ID=miid
export EXCEL_FILE_PATH=./facturas.xlsx
bun run src/cli.ts
```

## 🛠️ Comandos Disponibles

- `bun run build`: Construye el proyecto TypeScript
- `bun run build:exe`: Construye ejecutable para el sistema actual
- `bun run build:linux`: Construye ejecutable para Linux
- `bun run build:macos`: Construye ejecutable para macOS
- `bun run build:windows`: Construye ejecutable para Windows
- `bun run src/cli.ts --help`: Muestra ayuda

## 🚨 Solución de Problemas

### Error de Autenticación
- Verifica que tus credenciales de Siigo sean correctas
- Asegúrate de que el `baseURL` en el código sea el correcto para tu región

### Archivo Excel No Encontrado
- Verifica la ruta del archivo
- Usa rutas absolutas si es necesario

### Facturas Inválidas
- Revisa el formato de tu archivo Excel
- Asegúrate de que las columnas requeridas estén presentes
- Consulta los logs de validación para detalles específicos

### Problemas con Ejecutable
- Asegúrate de que el archivo tenga permisos de ejecución: `chmod +x dist/siigo-invoice`
- Reconstruye si hay cambios en el código

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es privado y no tiene licencia pública.

---

¡Gracias por usar Siigo Invoice CLI! Si tienes preguntas, revisa los ejemplos o abre un issue en el repositorio.
