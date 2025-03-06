# ast-tennis-app

## Guía de uso de Pipenv

### 1. Ubicarse en el folder del proyecto

Antes de ejecutar algun comando ir a la ruta del proyecto por ejemplo **/ast-tennis-app**

### 2. Instalación de Pipenv

Si aún no tienes Pipenv instalado, ejecuta:

```bash
pip install pipenv
```

### 3. Instalación de Dependencias

En la raíz del proyecto, instala todas las dependencias definidas en el Pipfile ejecutando:

```bash
pipenv install
```

Este comando creará el entorno virtual e instalará todas las dependencias.

### 4. Activación del Entorno Virtual

Para activar el entorno virtual y trabajar dentro de él, ejecuta:

```bash
pipenv shell
```

### 5. Ejecución de la Aplicación

Una vez dentro del entorno virtual, puedes ejecutar la aplicación o cualquier script, por ejemplo:

```bash
python main.py
```

### 6. Instalación de una Nueva Dependencia

Si necesitas agregar una nueva dependencia al proyecto, utiliza el siguiente comando (reemplazando **nombre_del_paquete** por el nombre de la dependencia):

```bash
pipenv install nombre_del_paquete
```

Este comando actualizará automáticamente el Pipfile y generará o actualizará el Pipfile.lock. Asegúrate de hacer commit de estos archivos para que el resto del equipo disponga de la configuración actualizada.
