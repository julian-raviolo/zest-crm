# CRM de Zest (crm.zest.uy)

EspoCRM 10.0.10 con el tema Zest incluido (`custom/Espo/Modules/ZestTheme` y `client/custom/modules/zest-theme`).
Se publica en Hostinger con hPanel → Avanzado → GIT, en la carpeta `public_html/crm`.

- `data/` (configuración, contraseña de la base, adjuntos) se crea en el servidor y está en `.gitignore`: nunca se sube.
- Las personalizaciones del panel y las extensiones que se instalen desde Administración quedan solo en el servidor.
- Para actualizar EspoCRM, hacerlo por este repositorio (reemplazar los archivos por la versión nueva y desplegar),
  no con el actualizador del panel: si el servidor modifica archivos del repositorio, Hostinger ya no puede desplegar.
