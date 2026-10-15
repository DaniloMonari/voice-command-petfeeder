import speech_recognition as sr
import requests
import time

# --- Configuração de Rede do ESP32 ---
# Substitua pelo IP exibido pelo ESP32 no Serial Monitor
ESP32_IP = "http://192.168.1.15"

def enviar_comando_wifi(endpoint):
    """Envia requisição GET para o ESP32 via Wi-Fi."""
    url = f"{ESP32_IP}/{endpoint}"
    try:
        resposta = requests.get(url, timeout=3)
        if resposta.status_code == 200:
            print(f"[ESP32 Wi-Fi] -> {resposta.text}")
        else:
            print(f"[Aviso] O ESP32 respondeu com status {resposta.status_code}")
    except requests.exceptions.RequestException as erro:
        print(f"[Erro de Conexão Wi-Fi] Não foi possível alcançar o ESP32: {erro}")


def ouvir_microfone(microfone, source):
    """Escuta o áudio do microfone e transcreve para texto."""
    try:
        print("\nOuvindo...")
        audio = microfone.listen(source, timeout=5, phrase_time_limit=5)
        frase = microfone.recognize_google(audio, language="pt-BR").lower()
        print(f"Você disse: '{frase}'")
        return frase
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        print("Não entendi o que foi falado.")
        return ""
    except sr.RequestError as e:
        print(f"Erro no serviço de reconhecimento: {e}")
        return ""


def main():
    microfone = sr.Recognizer()
    sistema_ativo = False

    print("=" * 60)
    print("SISTEMA DE COMANDO DE VOZ VIA WI-FI - COMEDOURO ESP32")
    print(f"Destino: {ESP32_IP}")
    print("Controle: 'ativar' / 'iniciar'  |  'desativar' / 'pausar'  |  'sair'")
    print("Ações:    'abrir'  |  'fechar'  |  'alimentar'")
    print("=" * 60)

    # Teste inicial de conectividade
    try:
        res = requests.get(ESP32_IP, timeout=2)
        print(f"Conexão com ESP32 confirmada: {res.text}")
    except Exception:
        print("Aviso: ESP32 não respondeu na inicialização. Verifique se estão na mesma rede Wi-Fi.")

    with sr.Microphone() as source:
        print("\nCalibrando ruído ambiente...")
        microfone.adjust_for_ambient_noise(source, duration=1.5)
        print("Calibração concluída! Diga 'ativar' ou 'iniciar' para começar.")

        while True:
            frase = ouvir_microfone(microfone, source)
            if not frase:
                continue

            # 1. Encerramento geral
            if any(palavra in frase for palavra in ["encerrar", "sair", "fechar programa"]):
                print("\nEncerrando o programa de comando de voz. Até logo!")
                break

            # 2. Desativação / Pausa
            if any(palavra in frase for palavra in ["desativar", "pausar", "parar escuta"]):
                if sistema_ativo:
                    sistema_ativo = False
                    print(">> Sistema pausado. Diga 'ativar' para retornar.")
                else:
                    print(">> O sistema já está inativo.")
                continue

            # 3. Acionamento do sistema
            if any(palavra in frase for palavra in ["iniciar", "ativar", "ligar sistema", "acordar"]):
                sistema_ativo = True
                print(">> SISTEMA ATIVADO! Comandos liberados ('abrir', 'fechar', 'alimentar').")
                continue

            # 4. Comandos de acionamento do comedouro
            if sistema_ativo:
                if any(palavra in frase for palavra in ["abrir", "abre", "liberar"]):
                    print(">> Enviando comando: ABRIR via Wi-Fi")
                    enviar_comando_wifi("abrir")

                elif any(palavra in frase for palavra in ["fechar", "fecha", "travar"]):
                    print(">> Enviando comando: FECHAR via Wi-Fi")
                    enviar_comando_wifi("fechar")

                elif any(palavra in frase for palavra in ["alimentar", "comida", "dar ração"]):
                    print(">> Enviando comando: CICLO DE ALIMENTAÇÃO via Wi-Fi")
                    enviar_comando_wifi("alimentar")

                else:
                    print(f">> Comando '{frase}' não reconhecido.")
            else:
                print(">> Sistema em espera. Diga 'ativar' antes de emitir um comando.")


if __name__ == "__main__":
    main()