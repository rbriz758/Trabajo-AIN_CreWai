!iniciar_app.

+!iniciar_app
    <- .print("=== APP DE VIAJES INICIADA ===");
       
       puente.pedir_datos("¿Desde qué ciudad sales?", Origen);
       puente.pedir_datos("¿A qué ciudad te gustaría viajar?", Destino);
       puente.pedir_datos("¿Cuál es tu presupuesto máximo en euros?", Presupuesto_Str);
       
       .term2string(Presupuesto, Presupuesto_Str);
       
       .print("Usuario quiere ir de ", Origen, " a ", Destino, " con ", Presupuesto, " euros.");
       .print("Enviando solicitud al Director...");
       
       // Pasamos el Origen en el mensaje
       .send(director, tell, peticion_viaje(Origen, Destino, Presupuesto)).