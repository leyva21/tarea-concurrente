import threading
import time
import random


entrada_count = 0
salida_count = 0
lock = threading.Lock()  # la exclusión mutua para las variables compartidas

# Función para la entrada de un visitante/microsegundos
def entrada():
    global entrada_count
    with lock:
        entrada_count += 1
        print(f"Entrada - Visitante ingresado por Puerta 1. Total de entrada: {entrada_count}")
    time.sleep(random.uniform(0, 0.1))

# Función para simular la salida de un visitante/microsegundos
def salida():
    global salida_count
    with lock:
        salida_count += 1
        print(f"Salida - Visitante salido por Puerta 2. Total de salida: {salida_count}")
    time.sleep(random.uniform(0, 0.1))

# Función para contar el tiempo en segundo plano
def contar_tiempo():
    tiempo_inicio = time.time()
    while True:
        tiempo_transcurrido = time.time() - tiempo_inicio
        print(f"Tiempo transcurrido: {tiempo_transcurrido:.2f} segundos")
        time.sleep(1)  # Actualizar cada segundo

# Función para contar el número de personas en la sala en segundo plano
def contar_personas():
    while True:
        with lock:
            personas_en_sala = entrada_count - salida_count
            print(f"Personas en la sala: {personas_en_sala}")
        time.sleep(2)

# Hilo para contar el tiempo en segundo plano
hilo_tiempo = threading.Thread(target=contar_tiempo)
hilo_tiempo.daemon = True  # Configura el hilo como demonio para que se detenga cuando el programa principal termine

# Hilo para contar el número de personas en la sala en segundo plano
hilo_contar_personas = threading.Thread(target=contar_personas)
hilo_contar_personas.daemon = True  # Configura el hilo como demonio para que se detenga cuando el programa principal termine

# Inicia los hilos
hilo_tiempo.start()
hilo_contar_personas.start()

try:
    # Ejecutar la simulación de entrada y salida de visitantes durante 5 minutos de trabajo
    tiempo_de_trabajo = 5 * 60 
    tiempo_inicio_simulacion = time.time()

    while time.time() - tiempo_inicio_simulacion < tiempo_de_trabajo:
        if random.choice([True, False]):  # Simular entrada o salida aleatoria
            hilo_entrada = threading.Thread(target=entrada)
            hilo_entrada.start()
        else:
            hilo_salida = threading.Thread(target=salida)
            hilo_salida.start()

        time.sleep(random.uniform(0.1, 0.5))  # Esperar un tiempo aleatorio antes de la siguiente operación

except KeyboardInterrupt:
    print("\nInterrupción del usuario. Saliendo del programa.")

# except Exception as e:
    # print(f"Excepción capturada: {e}")

# Espera a que todos los hilos de entrada/salida terminen antes de salir del programa
hilo_entrada.join()
hilo_salida.join()

# Imprime el resultado final después de 5 minutos de trabajo
with lock:
    personas_en_sala_final = entrada_count - salida_count
    print(f"\nTrabajo terminado. Personas en la sala: {personas_en_sala_final}")
