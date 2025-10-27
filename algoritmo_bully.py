import time
import random

def bully_election(num_procesos, initiator_id, porcentaje_procesos_muertos, verbose=False):

    mensajes = 0

    all_processes = list(range(num_procesos))
    alive = [p for p in all_processes if random.random() > porcentaje_procesos_muertos/100]

    if len(alive) == 0:
        return {"error": "Todos los procesos fallaron"}

    if initiator_id not in alive:
        initiator_id = random.choice(alive)

    alive.sort()
    if verbose:
        print(f"Procesos vivos: {alive}")
        print(f"Proceso inicio: {initiator_id}")

    # Inicia elección
    mas_alto = [p for p in alive if p > initiator_id]
    mensajes += len(mas_alto)  # mensajes ELECTION

    if verbose:
        print(f"{initiator_id} → envía ELECTION a {mas_alto}")

    # Cada proceso mayor responde (si está vivo)
    for p in mas_alto:
        mensajes += 1  # respuesta OK
        sub_mas_alto = [x for x in alive if x > p]
        # si hay más altos, este también inicia su propia elección
        if sub_mas_alto:
            mensajes += len(sub_mas_alto)  # ELECTION
            mensajes += len(sub_mas_alto)  # OKs
            if verbose:
                print(f"{p} inicia nueva elección con {sub_mas_alto}")

    # El proceso más alto vivo gana
    leader = max(alive)
    mensajes += len(alive) - 1  # COORDINATOR broadcast

    return {
        "Procesos totales": num_procesos,
        "Procesos vivos": len(alive),
        "Proceso iniciador": initiator_id,
        "Proceso líder": leader,
        "Mensajes enviados": mensajes
    }
# Ejecución con distintas cantidad de procesos vivos, y con IDs aleatorios

#for porcentaje_procesos_muertos in [0]: //Evaluación del peor escenario, donde todos los procesos están vivos
for porcentaje_procesos_muertos in [0, 20, 40, 60]:
    resultado = bully_election(num_procesos=100, initiator_id=0,
                porcentaje_procesos_muertos=porcentaje_procesos_muertos,verbose=False)
    print(resultado)