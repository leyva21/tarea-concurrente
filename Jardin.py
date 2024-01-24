import threading
import time
import random
import asyncio

entrada_count = 0
salida_count = 0
lock = threading.Lock()

entry_threads = []
exit_threads = []

def entrada():
    global entrada_count
    with lock:
        entrada_count += 1
        print(f"Entrada - Visitante ingresado por Puerta 1. Total de entrada: {entrada_count}")
    time.sleep(random.uniform(0, 0.1)) 

def salida():
    global salida_count
    with lock:
        salida_count += 1
        print(f"Salida - Visitante salido por Puerta 2. Total de salida: {salida_count}")
    time.sleep(random.uniform(0, 0.1)) 

def contar_tiempo():
    tiempo_inicio = time.time()
    while True:
        tiempo_transcurrido = time.time() - tiempo_inicio
        print(f"Tiempo transcurrido: {tiempo_transcurrido:.2f} segundos")
        time.sleep(1)  

def contar_personas():
    while True:
        with lock:
            personas_en_sala = entrada_count - salida_count
            print(f"Personas en la sala: {personas_en_sala}")
            if personas_en_sala < 0:
                raise ValueError("Número negativo de personas en la sala.")

        time.sleep(2)

async def simulacion():
    while True:
        try:
            if random.choice([True, False]): 
                entrada()
            else:
                salida()

            await asyncio.sleep(random.uniform(0.1, 0.5))  

        except ValueError as ve:
            print(f"Excepción capturada: {ve}")
            
            global entrada_count, salida_count
            entrada_count = 0
            salida_count = 0
            await asyncio.sleep(2)  

async def main():

    hilo_tiempo = threading.Thread(target=contar_tiempo)
    hilo_tiempo.daemon = True  
    hilo_tiempo.start()

    hilo_contar_personas = threading.Thread(target=contar_personas)
    hilo_contar_personas.daemon = True  
    hilo_contar_personas.start()

    await asyncio.gather(simulacion())

asyncio.run(main())

for thread in entry_threads:
    thread.join()

for thread in exit_threads:
    thread.join()

with lock:
    personas_en_sala_final = entrada_count - salida_count
    print(f"\nTrabajo terminado. Personas en la sala: {personas_en_sala_final}")
