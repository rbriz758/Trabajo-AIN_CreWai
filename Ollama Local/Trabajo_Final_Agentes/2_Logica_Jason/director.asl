// Recibimos Origen, Destino y Presupuesto
+peticion_viaje(Origen, Destino, Presupuesto)[source(Agente)]
    <- .print("He recibido la solicitud del agente ", Agente);
       .print("Evaluando viabilidad logistica...");
       
       if (Presupuesto < 500) {
           .print("ALERTA: El presupuesto es muy bajo. Cancelando operacion.");
       } else {
           .print("Presupuesto aprobado. Despertando a los agentes de IA en Python...");
           // IMPORTANTE: Pasamos Origen, Destino y la variable Informe
           puente.llamar_python(Origen, Destino, Informe);
           
           .print("====================================");
           .print("      INFORME FINAL RECIBIDO        ");
           .print("====================================");
           .print(Informe);
       }
.