# 🎙️ Comedouro Automático por Comando de Voz (ESP32 + Servo MG996R)

Sistema de automação para alimentação de pets utilizando reconhecimento de comandos de voz em Python (VS Code) e controle mecânico de comporta via microcontrolador ESP32 e servo motor MG996R, integrado por rede Wi-Fi local (HTTP REST).

---

## 📌 Sumário
- [Visão Geral](#-visão-geral)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Conexões de Hardware](#-conexões-de-hardware)
- [Comandos de Voz Aceitos](#-comandos-de-voz-aceitos)
- [Como Executar](#-como-executar)
- [Licença](#-licença)

---

## 🎯 Visão Geral
* **Firmware (ESP32):** Atua como servidor HTTP recebendo rotas de acionamento (`/abrir`, `/fechar`, `/alimentar`).
* **Módulo de Voz (Python):** Capta o áudio pelo microfone do computador via `SpeechRecognition`, reconhece palavras-chave e dispara as requisições HTTP para a placa.

---

## 📂 Estrutura do Projeto
* [`firmware/esp32_comedouro_wifi.ino`](firmware/esp32_comedouro_wifi.ino): Código em C++ para gravação via Arduino IDE.
* [`src/voz_wifi.py`](src/voz_wifi.py): Script de reconhecimento de fala e requisições HTTP.
* [`requirements.txt`](requirements.txt): Relação de bibliotecas Python necessárias.

---

## 🔌 Conexões de Hardware

| Componente | Pino / Fio | Conexão no ESP32 / Fonte |
| :--- | :--- | :--- |
| **Servo MG996R** | Vermelho (VCC) | +5V (Fonte externa 2A) |
| **Servo MG996R** | Marrom/Preto (GND) | GND da fonte e GND comum do ESP32 |
| **Servo MG996R** | Amarelo/Laranja (Sinal) | GPIO 18 do ESP32 |

---

## 🗣️ Comandos de Voz Aceitos
* **Controle do Sistema:** `iniciar`, `ativar`, `desativar`, `pausar`, `encerrar`.
* **Mecânica da Comporta:** `abrir`, `fechar`, `alimentar` (ciclo automático de dosagem).

---

## 🚀 Como Executar

1. **Gravar a Placa:** Abra o arquivo `firmware/esp32_comedouro_wifi.ino` no Arduino IDE, insira o Wi-Fi local e realize o upload.
2. **Identificar o IP:** Anote o endereço IP no Monitor Serial (ex: `192.168.1.15`).
3. **Instalar Dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Executar:** Atualize o IP no arquivo `src/voz_wifi.py` e execute:
   ```bash
   python src/voz_wifi.py
   ```

---

## 📄 Licença
Distribuído sob a licença MIT.