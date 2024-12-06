# LinacControl

Sistema de gestión para control de calidad de aceleradores lineares y tratamientos de radioterapia.

## Requerimientos

- [Python 3.10](https://www.python.org/downloads/)
- [MySQL](https://www.mysql.com/downloads/)

## Configuración

1. Copie o renombre el archivo `.env-example` a `.env` en la carpeta `app/`.
2. Modifique las variables de entorno en el archivo `.env` según su configuración.

## Instalación

### Linux

En sistemas Linux, abra una terminal y ejecute los siguientes comandos:

```bash
git clone https://github.com/Ollyxs/linaccontrol.git
cd linaccontrol
./install.sh
```

### Windows

En Windows, abra cmd y ejecute los siguientes comandos:

```cmd
git clone https://github.com/Ollyxs/linaccontrol.git
cd linaccontrol
./install.bat
```

Esto descargará el proyecto, creará el entorno virtual e instalará las dependencias necesarias.

## Ejecución

### Linux

En la carpeta del proyecto, ejecute el siguiente comando:

```bash
./boot.sh
```

### Windows

En la carpeta del proyecto, ejecute el siguiente comando:

```cmd
.\boot.bat
```

Ahora puede acceder a la aplicación en su navegador web en la dirección `http://localhost:8000` o desde cualquier dispositivo en la red local en la dirección `http://<ip-de-su-maquina>:8000`.

> **Nota:** Si quiere ejecutar la aplicación en un puerto diferente, modifique el archivo `boot.sh` o `boot.bat` (dependiendo de su sistema operativo) y cambie el número de puerto del argumento `--port`.

## Ejecutar como servicio

<details>
<summary>
  <h3>Linux</h3>
</summary>
<br>

Para crear un servicio en Linux que ejecute el script `boot.sh` y se inicie automáticamente al encender el sistema, siga estos pasos:

1. Cree un archivo de unidad de sistema para el servicio. Abra una terminal y ejecute:

   ```bash
   sudo nano /etc/systemd/system/linaccontrol.service
   ```

2. Agregue el siguiente contenido al archivo `linaccontrol.service`:

   ```ini
   [Unit]
   Description=LinacControl Service
   After=network.target

   [Service]
   ExecStart=/ruta/a/tu/proyecto/linaccontrol/boot.sh
   WorkingDirectory=/ruta/a/tu/proyecto/linaccontrol
   User=tu_usuario
   Group=tu_grupo
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Asegúrese de reemplazar `/ruta/a/tu/proyecto/linaccontrol` con la ruta real a su proyecto, `tu_usuario` con su nombre de usuario y `tu_grupo` con su grupo.

3. Guarde y cierre el archivo.

4. Recargue los archivos de unidad de sistema para que el sistema reconozca el nuevo servicio:

   ```bash
   sudo systemctl daemon-reload
   ```

5. Habilite el servicio para que se inicie automáticamente al encender el sistema:

   ```bash
   sudo systemctl enable linaccontrol.service
   ```

6. Inicie el servicio:

   ```bash
   sudo systemctl start linaccontrol.service
   ```

</details>

<details>
<summary>
  <h3>Windows</h3>
</summary>
<br>

1. Descargue [NSSM](https://nssm.cc/download) y extraiga el archivo zip en una carpeta de su preferencia.
2. Abra cmd con permisos de administrador y navegue hasta el directorio donde se encuentra `nssm.exe`. Por ejemplo:

   ```cmd
   cd ruta\al\programa\nssm-X.XX\winXX
   ```

3. Ejecute el siguiente comando para instalar el servicio LinacControl:

   ```cmd
   nssm.exe install LinacControlService
   ```

   Reemplace `ruta\al\programa` por la ruta donde extrajo el archivo zip y `X.XX` y `XX` por la versión de NSSM y su arquitectura respectivamente. También puede cambiar el nombre del servicio `LinacControlService` por el que desee.

4. En la ventana que se abre, haga clic en `...` en el campo `Path` y seleccione el archivo `boot.bat` en la carpeta del proyecto. Luego haga clic en `Install service`.

5. Para iniciar el servicio, ejecute el siguiente comando:

   ```cmd
   nssm.exe start LinacControlService
   ```

Ahora puede acceder a la aplicación en su navegador web en la dirección `http://localhost:8000` o desde cualquier dispositivo en la red local en la dirección `http://<ip-de-su-maquina>:8000`. El servicio se iniciará automáticamente al encender su computadora.

</details>
