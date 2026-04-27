# 🎙️ NetDevOps: Intelligent Network Auditor (AWS Polly + Twilio)
> **Transformando datos operativos en inteligencia de voz mediante integración Multi-Cloud.**

[![Python](https://img.shields.io/badge/Language-Python-blue?style=flat&logo=python)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/Cloud-AWS-orange?style=flat&logo=amazon-aws)](https://aws.amazon.com/)
[![Twilio](https://img.shields.io/badge/API-Twilio-red?style=flat&logo=twilio)](https://www.twilio.com/)

Este repositorio implementa un flujo de trabajo **NetDevOps** avanzado que automatiza la auditoría de dispositivos de red. Inspirado en el concepto de *"Modern Show Version"*, esta herramienta no solo extrae información crítica del hardware, sino que la procesa mediante servicios de Inteligencia Artificial para entregar reportes de estado vía llamadas telefónicas automatizadas.

---

### 📡 Arquitectura del Sistema
La arquitectura sigue un modelo de **Plano de Gestión Programable**:

1.  **Ingesta de Datos:** Utiliza **Netmiko/Nornir** para establecer sesiones SSH seguras con dispositivos de red y recolectar telemetría (Software version, Uptime, Hardware health).
2.  **Procesamiento de Voz (AWS Polly):** El motor de síntesis de voz de AWS convierte los reportes estructurados en audio natural, permitiendo una interpretación rápida sin necesidad de leer logs extensos.
3.  **Entrega de Alerta (Twilio):** Se integra con la API de Twilio para realizar llamadas salientes, asegurando que las anomalías críticas lleguen al administrador de guardia de forma inmediata.

---

### 🚀 Capacidades Destacadas
* **Automatización de Auditoría:** Reduce el error humano y optimiza los ciclos de verificación en infraestructuras de misión crítica.
* **Visibilidad Proactiva:** Ideal para entornos de **Data Center Activo-Activo** donde la detección rápida de cambios en el inventario es vital para mantener el RTO.
* **Diseño Extensible:** Arquitectura modular que permite añadir nuevos comandos de red o diferentes servicios de notificación.

---

### 🛠️ Stack Tecnológico
* **Networking:** Netmiko, Nornir (Automatización de dispositivos).
* **Cloud:** AWS Boto3 (Polly, Secrets Manager para gestión de llaves).
* **DevOps:** Python 3.10+, Git para control de versiones.
* **Telephony:** Twilio SDK.

---

### 🔧 Implementación y Uso

#### Requisitos Previos
* Cuenta de AWS con permisos para Polly.
* Cuenta de Twilio con un número configurado.
* Dispositivos de red con SSH habilitado.

#### Ejecución
```bash
# Instalación de dependencias
pip install -r requirements.txt

# Ejecución del orquestador
python main_polly_notifier.py --inventory inventory.yaml
