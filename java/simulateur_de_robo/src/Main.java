import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import javax.swing.*;

public class Main {

    // Variable accesible globalmente dentro de Main
    private static Map<String, String> data = new HashMap<>();

    public static void main(String[] args) {
        obtenerDatosRobot();

        // Lanza la interfaz gráfica con los datos disponibles
        SwingUtilities.invokeLater(() -> lanzarInterfaz());
    }

    /**
     * Obtiene los datos del robot y los guarda en el mapa `data`
     */
    private static void obtenerDatosRobot() {
        try {
            // Simulación de obtención de datos desde API
            String response = RobotClient.getRobotDataByUUID("12312fz-12dd-1dad-11da5");
            System.out.println("🔹 JSON recibido: " + response);

            data = parseJson(response);

            // Muestra datos importantes
            System.out.println("🔹 Nombre del robot: " + data.get("name"));
            System.out.println("🔹 Dirección MAC: " + data.get("mac_address"));
            System.out.println("🔹 Misión asignada: " + data.get("mission"));
            System.out.println("🔹 ID del robot: " + data.get("id"));
            System.out.println("🔹 ID de instrucción: " + data.get("inst_id"));

            // Procesar instrucciones si existen
            String instructionStr = data.get("instruction");
            if (instructionStr != null) {
                int[] instrucciones = parseInstruction(instructionStr);
                System.out.print("🔹 Instrucciones recibidas: ");
                for (int inst : instrucciones) {
                    System.out.print(inst + " ");
                }
                System.out.println();
            } else {
                System.out.println("⚠️ No se encontraron instrucciones.");
            }

        } catch (IOException e) {
            System.err.println("❌ Error al obtener los datos del robot.");
            e.printStackTrace();
        }
    }

    /**
     * Lanza la ventana gráfica del simulador
     */
    private static void lanzarInterfaz() {
        JFrame frame = new JFrame("Simulador de robot");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        String robotId = data.getOrDefault("id", "desconocido");
        String instId = data.getOrDefault("inst_id", "0");

        frame.setContentPane(new RobotPanel(robotId, Integer.parseInt(instId)));
        frame.pack();
        frame.setVisible(true);
    }

    /**
     * Analiza un JSON plano (sin estructuras anidadas ni arrays) y lo convierte a un mapa clave-valor.
     */
    public static Map<String, String> parseJson(String json) {
        Map<String, String> result = new HashMap<>();
        json = json.replaceAll("[{}\"]", ""); // Elimina llaves y comillas
        String[] entries = json.split(",");

        for (String entry : entries) {
            String[] keyValue = entry.split(":", 2); // Solo divide en dos partes
            if (keyValue.length == 2) {
                result.put(keyValue[0].trim(), keyValue[1].trim());
            }
        }
        return result;
    }

    /**
     * Convierte una cadena de números separados por coma en un array de enteros.
     * Los valores no numéricos se reemplazan por -1.
     */
    public static int[] parseInstruction(String instructionString) {
        String[] parts = instructionString.split(",");
        int[] result = new int[parts.length];

        for (int i = 0; i < parts.length; i++) {
            try {
                result[i] = Integer.parseInt(parts[i].trim());
            } catch (NumberFormatException e) {
                System.err.println("⚠️ Error al convertir '" + parts[i] + "' a número.");
                result[i] = -1;
            }
        }
        return result;
    }
}
