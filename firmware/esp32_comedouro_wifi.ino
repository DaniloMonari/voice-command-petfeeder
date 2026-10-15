#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

// --- Credenciais da sua rede Wi-Fi ---
const char* ssid = "NOME_DA_SUA_REDE_WIFI";
const char* password = "SENHA_DO_SEU_WIFI";

// Cria o servidor HTTP na porta padrão 80
WebServer server(80);

Servo servoComporta;
const int pinoServo = 18;

const int ANGULO_FECHADO = 0;
const int ANGULO_ABERTO  = 90;

// Rotas do servidor web
void handleAbrir() {
  servoComporta.write(ANGULO_ABERTO);
  server.send(200, "text/plain", "OK: Comporta Aberta");
  Serial.println("Comando recebido: ABRIR");
}

void handleFechar() {
  servoComporta.write(ANGULO_FECHADO);
  server.send(200, "text/plain", "OK: Comporta Fechada");
  Serial.println("Comando recebido: FECHAR");
}

void handleAlimentar() {
  server.send(200, "text/plain", "OK: Alimentando pet");
  Serial.println("Comando recebido: ALIMENTAR");
  servoComporta.write(ANGULO_ABERTO);
  delay(3000); // 3 segundos aberto
  servoComporta.write(ANGULO_FECHADO);
  Serial.println("Comporta Fechada");
}

void handleRoot() {
  server.send(200, "text/plain", "ESP32 Comedouro Conectado e Operacional!");
}

void setup() {
  Serial.begin(115200);

  // Configuração do servo
  ESP32PWM::allocateTimer(0);
  servoComporta.setPeriodHertz(50);
  servoComporta.attach(pinoServo, 500, 2400);
  servoComporta.write(ANGULO_FECHADO);

  // Conexão Wi-Fi
  Serial.print("Conectando ao Wi-Fi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWi-Fi Conectado!");
  Serial.print("Endereço IP atribuído: ");
  Serial.println(WiFi.localIP()); // <-- Anote esse IP para colocar no VS Code!

  // Registro das rotas HTTP
  server.on("/", handleRoot);
  server.on("/abrir", handleAbrir);
  server.on("/fechar", handleFechar);
  server.on("/alimentar", handleAlimentar);

  server.begin();
  Serial.println("Servidor HTTP iniciado com sucesso!");
}

void loop() {
  server.handleClient(); // Processa as requisições HTTP recebidas via Wi-Fi
}
