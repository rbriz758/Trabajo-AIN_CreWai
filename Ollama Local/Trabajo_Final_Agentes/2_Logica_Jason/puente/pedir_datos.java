package puente;

import jason.asSemantics.*;
import jason.asSyntax.*;
import javax.swing.JFrame;
import javax.swing.JOptionPane;

public class pedir_datos extends DefaultInternalAction {

    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        String pregunta = ((StringTerm) args[0]).getString();

        // TRUCO: Creamos un marco invisible y le decimos "Ponte encima de todo"
        JFrame frame = new JFrame();
        frame.setAlwaysOnTop(true);
        frame.setLocationRelativeTo(null); // Lo centra en medio de tu pantalla

        // Mostramos la pregunta pegada a ese marco
        String respuesta = JOptionPane.showInputDialog(frame, pregunta, "Planificador CrewAI",
                JOptionPane.QUESTION_MESSAGE);

        // Limpiamos el marco
        frame.dispose();

        if (respuesta == null || respuesta.trim().isEmpty()) {
            respuesta = "Cancelado";
        }

        return un.unifies(args[1], new StringTermImpl(respuesta));
    }
}