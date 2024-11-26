#!/bin/bash

# Verificar si se pasó la versión como argumento
if [ -z "$1" ]; then
    echo "Uso: $0 <nueva_version>"
    exit 1
fi

VERSION=$1
VERSION_FILE="version.txt"

# Actualizar el archivo version.txt
echo "$VERSION" > "$VERSION_FILE"

# Agregar y hacer commit del archivo actualizado
git add "$VERSION_FILE"
git commit -m "Update version to $VERSION"

# Crear el tag con la versión
git tag -a "$VERSION" -m "Release $VERSION"

# Subir el commit y el tag al repositorio remoto
git push origin main  # Cambia "main" por la rama en la que trabajas
git push origin "$VERSION"

echo "Versión $VERSION actualizada, commit realizado, y tag creado."
