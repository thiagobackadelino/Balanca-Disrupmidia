'''
    Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
import time
import sys
import signal
from hx711 import HX711
from flask import Flask, request, redirect, url_for, send_from_directory,render_template

app = Flask(__name__)

# Define a numeração dos pinos de acordo com a placa
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(19000)
hx.reset()
hx.tare()

TRIG = 24
ECHO = 23
sampling_rate = 20.0
speed_of_sound = 349.10
max_distance = 4.0
max_delta_t = max_distance / speed_of_sound
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)
time.sleep(1)
    

# Função para finalizar o acesso à GPIO do Raspberry de forma segura
def clean():
    GPIO.cleanup()

# Função para finalizar o programa de forma segura com CTRL-C
def sigint_handler(signum, instant):
    clean()
    sys.exit()

# Ativar a captura do sinal SIGINT (Ctrl-C)
signal.signal(signal.SIGINT, sigint_handler)
    

def balanca():
    # Read Sensors Status
    val = hx.get_weight(5)
    hx.power_down()
    hx.power_up()
    time.sleep(0.1)
    return round(val,2)

def altura():
     # Gera um pulso de 10ms em TRIG.
    # Essa ação vai resultar na transmissão de ondas ultrassônicas pelo
    # transmissor do módulo sonar.
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Atualiza a variável start_t enquanto ECHO está em nível lógico baixo.
    # Quando ECHO trocar de estado, start_t manterá seu valor, marcando
    # o momento da borda de subida de ECHO. Este é o momento em que as ondas
    # sonoras acabaram de ser enviadas pelo transmissor.
    while GPIO.input(ECHO) == 0:
      start_t = time.time()

    # Atualiza a variável end_t enquando ECHO está em alto. Quando ECHO
    # voltar ao nível baixo, end_t vai manter seu valor, marcando o tempo
    # da borda de descida de ECHO, ou o momento em que as ondas refletidas
    # por um objeto foram captadas pelo receptor. Caso o intervalo de tempo
    # seja maior que max_delta_t, o loop de espera também será interrompido.
    while GPIO.input(ECHO) == 1 and time.time() - start_t < max_delta_t:
      end_t = time.time()

    # Se a diferença entre end_t e start_t estiver dentro dos limites impostos,
    # atualizamos a variável delta_t e calculamos a distância até um obstáculo.
    # Caso o valor de delta_t não esteja nos limites determinados definimos a
    # distância como -1, sinalizando uma medida mal-sucedida.
    if end_t - start_t < max_delta_t:
        delta_t = end_t - start_t
        distance = 100*(0.5 * delta_t * speed_of_sound)
    else:
        distance = -1
    time.sleep(0.1)
    return round(distance, 2)

@app.route("/balanca")
def index():    
    templateData = {
      'senPeso' : balanca(),
      'senAltura'  : altura()
      }
    return render_template('response.json', **templateData)

@app.route("/home")
def home():    
    templateData = {
      }
    return render_template('/home.html', **templateData)

@app.route("/balanca-ajax")
def balanca_ajax():    
    templateData = {
      }
    return render_template('/balanca-ajax.html', **templateData)


    
if __name__ == "__main__":
   app.run(host='192.168.0.105', port=80, debug=True)
   
