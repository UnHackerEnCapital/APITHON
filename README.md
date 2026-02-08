# 🐍 APITHON – Protocol Analysis & Gateway PoC (v3.0)

<img width="290" height="263" alt="APITHON Logo" src="https://github.com/user-attachments/assets/295acb6c-0773-4201-85b1-563c16cbcbec" />



Bienvenido a **APITHON**, un entorno de laboratorio desarrollado por **UnHackerEnCapital** para la **interceptación, sincronización y puenteo (bridging)** de protocolos de comunicación en arquitecturas de modelos de lenguaje a gran escala.

Esta herramienta permite transformar una sesión de navegador autenticada en una pasarela programática (**API Gateway**) compatible con estándares industriales, facilitando auditorías de latencia, seguridad de red y análisis de cabeceras en entornos controlados.

> ⚖️ **Aviso de Auditoría:** Este software se proporciona con fines estrictamente educativos y de investigación en ciberseguridad. El usuario es el único responsable de asegurar que el análisis se realice sobre servicios donde tenga autorización explícita para auditar protocolos.

---

## 🚀 Características Principales

* **Sincronización de Túnel Automatizada:** Inyecta validaciones de actividad automatizadas para estabilizar el flujo de datos y capturar tokens de sesión.
* **Detección de Entorno Inteligente:** Adapta los comandos, escapes de caracteres y la interfaz según se ejecute en **Windows (CMD/PowerShell)** o **Linux (Bash)**.
* **Selector de Alcance de Red:**
    * **Modo Local (L):** Restringe el acceso a la pasarela únicamente al equipo host (127.0.0.1).
    * **Modo LAN (N):** Expone la interfaz en la red local (0.0.0.0), detectando automáticamente la IP privada del equipo para facilitar la conexión desde otros dispositivos.
* **TLS Fingerprinting:** Implementa mimetismo de navegador (Chrome 120) para evitar discrepancias en la capa de transporte y asegurar la integridad del túnel.

---

## 🔍 ¿Cómo funciona la PoC?

El sistema opera en tres fases críticas de análisis:

1.  **Interceptación (Sniffing):** Utilizando `Playwright`, el script captura los tokens de persistencia y el contexto dinámico del flujo de datos del objetivo definido.
2.  **Validación Emulada:** El script automatiza el envío de una señal de validación (`.`) para activar el intercambio de paquetes en el backend del objetivo de forma inmediata.
3.  **Puenteo (Gateway):** Levanta un servidor Flask que traduce peticiones REST estándar al protocolo interno capturado, permitiendo interoperabilidad con herramientas externas.

---

## ⚙️ Configuración y Uso

### 1️⃣ Instalación de Dependencias
Se recomienda el uso de un entorno virtual para mantener la integridad del sistema:
```bash
pip install flask playwright curl_cffi
playwright install chromium
```

### 2️⃣ Ejecución
```bash
python apithon.py
```

### 3️⃣ Flujo de Trabajo
1.  **Ingreso de URL:** El sistema solicitará la URL del servicio a analizar (ej: `app.targetservice.io`). El script gestiona automáticamente el protocolo `https://`.
2.  **Sincronización:** Se abrirá un navegador controlado. **APITHON** intentará validar la sesión automáticamente enviando una señal de actividad (`.`). Una vez sincronizado, los tokens se almacenan de forma segura en memoria volátil.
3.  **Selección de Modo:**
    * **Opción 1:** Inicia el servidor API y despliega un tutorial dinámico con comandos `curl` optimizados para **PowerShell**, **CMD** o **Bash**.
    * **Opción 2:** Abre una terminal de chat directa para interactuar con el backend y analizar las respuestas en crudo.

---

### 📸 Guía de Implementación (Modo Pasarela)
Al activar el modo **Gateway**, APITHON genera el comando exacto que necesitas según tu terminal detectada para asegurar la interoperabilidad:

* **PowerShell:** Utiliza `curl.exe` y formato de escape de comillas específico para evitar conflictos con los alias internos de Windows (`Invoke-WebRequest`).
* **CMD:** Proporciona la sintaxis clásica de Windows para ejecución directa en la consola estándar.
* **Linux/Bash:** Genera una estructura con escapes de línea estándar (`\`) para entornos Unix y manejo de comillas simples para el JSON.

---

### ⚠️ Descargo de Responsabilidad (Disclaimer)
> Esta herramienta ha sido creada exclusivamente para la comunidad de ciberseguridad. El autor no promueve ni se responsabiliza por el uso de **APITHON** para actividades que infrinjan los Términos de Servicio de cualquier plataforma o que violen leyes locales de acceso a sistemas informáticos.
>
> **La ética es el pilar fundamental del analista de seguridad.**

---
**Desarrollado por Hefin.net** – 2026
