package puente;

import jason.asSemantics.*;
import jason.asSyntax.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.*;

public class llamar_python extends DefaultInternalAction {

    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        // Leemos Origen (args[0]) y Destino (args[1])
        String origen = args[0].toString().replaceAll("\"", "");
        String destino = args[1].toString().replaceAll("\"", "");

        URL url = new URL("http://127.0.0.1:5000/investigar");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Content-Type", "application/json");
        con.setDoOutput(true);

        // Enviamos el JSON actualizado a Python
        String jsonInputString = "{\"origen\": \"" + origen + "\", \"destino\": \"" + destino + "\"}";
        try (OutputStream os = con.getOutputStream()) {
            byte[] input = jsonInputString.getBytes("utf-8");
            os.write(input, 0, input.length);
        }

        BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream(), "utf-8"));
        StringBuilder response = new StringBuilder();
        String responseLine = null;
        while ((responseLine = br.readLine()) != null) {
            response.append(responseLine.trim());
        }

        // El resultado se guarda en args[2]
        return un.unifies(args[2], new StringTermImpl(response.toString()));
    }
}