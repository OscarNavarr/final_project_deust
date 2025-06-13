import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class Main {

    /**
     * Analyse une chaîne JSON très simple (non imbriquée) et la convertit en une carte clé-valeur.
     * ⚠️ Cette méthode ne prend pas en charge les structures JSON complexes ni les tableaux réels.
     */
    public static Map<String, String> parseJson(String json) {
        Map<String, String> data = new HashMap<>();
        json = json.replaceAll("[{}\"]", ""); // supprime les accolades et les guillemets doubles
        String[] entries = json.split(",");

        for (String entry : entries) {
            String[] keyValue = entry.split(":", 2);
            if (keyValue.length == 2) {
                data.put(keyValue[0].trim(), keyValue[1].trim());
            }
        }
        return data;
    }

    /**
     * Convertit une chaîne séparée par des virgules (par exemple, «4,5,6,7») en un tableau d'entiers.
     * Si une valeur n’est pas un nombre, elle est remplacée par -1.
     */
    public static int[] parseInstruction(String instructionString) {
        String[] parts = instructionString.split(",");
        int[] result = new int[parts.length];

        for (int i = 0; i < parts.length; i++) {
            try {
                result[i] = Integer.parseInt(parts[i].trim());
            } catch (NumberFormatException e) {
                System.err.println("⚠️ Erreur de conversion '" + parts[i] + "' au nombre entier.");
                result[i] = -1;
            }
        }

        return result;
    }

    public static void main(String[] args) {
        try {
            // 🛰️ Faire une requête à l'API pour obtenir les données du robot en utilisant son MAC
            String response = RobotClient.getRobotDataByMacAddress("A4:5E:60:11:22:33");

            // 🧩 Analyser la réponse JSON (simple) dans une carte clé-valeur
            Map<String, String> data = parseJson(response);
            System.out.println("🔹 Data del robot: " + data);
            // 📋 Affiche les données de base du robot
            System.out.println("🔹 Nombre del robot: " + data.get("name"));
            System.out.println("🔹 Dirección MAC: " + data.get("mac_address"));
            System.out.println("🔹 Misión asignada: " + data.get("mission"));

            // 📦 Instructions de traitement et d'affichage si présentes
            String instructionStr = data.get("instruction");
            if (instructionStr != null) {
                int[] instructions = parseInstruction(instructionStr);
                System.out.print("🔹 Instructions reçues : ");
                for (int inst : instructions) {
                    System.out.print(inst + " ");
                }
                System.out.println();
            } else {
                System.out.println("⚠️ Aucune instruction trouvée.");
            }

        } catch (IOException e) {
            System.err.println("❌ Erreur lors de l'obtention des données du robot.");
            e.printStackTrace();
        }

        // 🖼️ Lancer l'interface graphique (Swing)
        javax.swing.SwingUtilities.invokeLater(() -> {
            javax.swing.JFrame frame = new javax.swing.JFrame("Simulateur de robot");
            frame.setDefaultCloseOperation(javax.swing.JFrame.EXIT_ON_CLOSE);
            frame.setContentPane(new RobotPanel());
            frame.pack();
            frame.setVisible(true);
        });
    }
}
