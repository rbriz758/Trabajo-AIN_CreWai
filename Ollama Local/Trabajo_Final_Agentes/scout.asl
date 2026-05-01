// Creencias iniciales
destino(tokio).
presupuesto(2000).

// Meta inicial
!buscar_vuelos.

// Plan para lograr la meta
+!buscar_vuelos : destino(D)
    <- .print("Iniciando busqueda de vuelos para ", D);
       // Aquí iría la lógica de comunicación con los otros agentes
       .send(analista, tell, vuelo_encontrado(D, 800)).