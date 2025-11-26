# Bookstore FastAPI

API creada con FastAPI que expone CRUD para las tablas definidas en `bookstoredb.sql`.

Requisitos:
- Definir la variable de entorno `DATABASE_URL` con la URL de PostgreSQL (Render). Ejemplo:

```
postgresql://user:password@hostname:5432/dbname
```

Instalación (en PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Arrancar la app (desarrollo):

```powershell
$env:DATABASE_URL = "postgresql://user:pass@host:5432/dbname"
uvicorn app.main:app --reload --port 8000
```

Rutas principales (ejemplos):
- `GET /authors/`, `POST /authors/`, `GET /authors/{id}`, `PUT /authors/{id}`, `DELETE /authors/{id}`
- `GET /books/`, `POST /books/`, etc. (mismo patrón para `categories`, `customers`, `orders`, `orderings`)

Filtrado disponible en `GET /books/` mediante query params:
- `author_id` (int)
- `category_id` (int)
- `title` (substring search)
- `year` (int)
- `min_price` y `max_price` (rango de precio)

Ejemplo:
```
GET /books/?author_id=3&min_price=100&max_price=500
```

Endpoint para obtener la imagen de un libro (si está almacenada en la BD):
- `GET /books/{book_id}/image` — devuelve la imagen como bytes con el `Content-Type` detectado (ej: `image/jpeg`, `image/png`).

Ejemplo de consumo desde .NET MAUI (C#):

```csharp
using System.Net.Http;
using System.IO;
using Microsoft.Maui.Controls;

public async Task<ImageSource?> GetBookImageAsync(int bookId)
{
	try
	{
		using var client = new HttpClient();
		var url = $"http://127.0.0.1:8000/books/{bookId}/image";
		var bytes = await client.GetByteArrayAsync(url);
		return ImageSource.FromStream(() => new MemoryStream(bytes));
	}
	catch (HttpRequestException)
	{
		// not found or network error
		return null;
	}
}

// Usage in a Page/ViewModel
// myImage.Source = await GetBookImageAsync(1);
```

Notas:
- La API intenta detectar el tipo de imagen con firma de bytes; si necesitas confiar en el `Content-Type` original, almacena también el tipo MIME en la BD.
- Para producción usa la URL pública de tu API en lugar de `127.0.0.1` y añade manejo de autenticación y caching.

Despliegue en Render (Docker)
--------------------------------

Archivos añadidos para despliegue con Docker:
- `Dockerfile` — construye la imagen y arranca Uvicorn.
- `.dockerignore` — excluye venvs y `.env` del contexto.
- `render.yaml` — plantilla de manifiesto para Render (opcional).

Pasos básicos:

1) Asegúrate de no commitear tu `.env` con credenciales. El repositorio contiene `.gitignore` que ya incluye `.env`.

2) Probar localmente con Docker:

```powershell
docker build -t bookstore-api:local .
docker run -e DATABASE_URL="postgresql://user:pass@host:5432/dbname" -p 8000:8000 bookstore-api:local
```

3) Subir el repo a GitHub y crear el Web Service en Render:
	- En Render elige "Create a new Web Service" y conecta tu repo.
	- Selecciona "Docker" (Render usará tu `Dockerfile`).
	- En Settings → Environment, añade `DATABASE_URL` con la cadena de conexión a tu Postgres (Render también la proporciona si usas su managed DB).
	- Deploy automático: Render construirá la imagen y desplegará el servicio.

4) Alternativamente puedes mantener `render.yaml` en el repo para que Render lo use como manifiesto.

Notas de producción:
- Para producción considera usar Gunicorn con Uvicorn workers, habilitar logging y health checks y usar almacenamiento externo (S3/Blob) para imágenes grandes.
- Nunca subas credenciales en `.env` al repo; usa las Environment Variables de Render.

