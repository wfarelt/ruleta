# Background Images

Esta carpeta contiene imágenes estáticas para usar en el sitio web de Pasanaku.

## Fondo de Página

Para añadir un fondo a `base.html`, sigue estos pasos:

1. **Descarga o coloca tu imagen** llamada `background.jpg` en esta carpeta (`static/images/`).
   
   Recomendaciones gratuitas:
   - [Pexels.com](https://www.pexels.com) - Fotos gratuitas y de alta calidad
   - [Unsplash.com](https://unsplash.com) - Imágenes hermosas y gratis
   - [Pixabay.com](https://pixabay.com) - Galería de imágenes públicas

2. **Ubica el archivo en**: `static/images/background.jpg`

3. **El sitio usará automáticamente** la imagen en `background.jpg` gracias a la regla CSS en `templates/base.html`.

4. **Para recopilar estáticos en producción**:
   ```bash
   python manage.py collectstatic --noinput
   ```

## Formatos y Tamaños Recomendados

- **Formato**: JPG (mejor compresión) o PNG (si requieres transparencia)
- **Tamaño**: 1920x1080px o superior (full HD)
- **Peso**: Menos de 500KB para mejor rendimiento web

## Personalización Adicional

Si quieres cambiar la opacidad del overlay o otros estilos, edita el archivo `templates/base.html`:
- Busca la línea con `rgba(0,0,0,0.35)` para ajustar la oscuridad (0-1)
- Modifica `background-size`, `background-position`, etc., según necesites
