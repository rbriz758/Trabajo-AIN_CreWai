destino(tokio).
presupuesto(2000).

!buscar_vuelos.

+!buscar_vuelos : destino(D)
    <- .print("Iniciando busqueda de vuelos para ", D);
       .send(analista, tell, vuelo_encontrado(D, 800)).