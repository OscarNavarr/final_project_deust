import java.io.IOException;
import java.util.Map;
import javax.swing.*;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;

public class Main {

    // Données du robot récupérées depuis l'API (stockées sous forme de clé-valeur)
    private static Map<String, String> data;

    public static void main(String[] args) {
        obtenirDonneesRobot();

        // Lancer l'interface graphique avec les données obtenues
        SwingUtilities.invokeLater(Main::lancerInterface);
    }

    /**
     * Récupère les données du robot via l'API REST et les stocke dans `data`
     */
    private static void obtenirDonneesRobot() {
        try {
            // Appel à l'API REST (POST /robot_data_by_uuid)
            String uuid = "12312fz-12dd-1dad-11da5";
            String response = RobotClient.getRobotDataByUUID(uuid);

            System.out.println("📦 Réponse JSON brute reçue :");
            System.out.println(response);

            // Conversion en Map<String, String> avec Gson
            data = parseJson(response);

            // Affichage des données essentielles
            System.out.println("\n🔹 Données du robot :");
            System.out.println("   ➤ Nom           : " + data.get("name"));
            System.out.println("   ➤ Adresse MAC   : " + data.get("mac_address"));
            System.out.println("   ➤ Mission       : " + data.get("mission"));
            System.out.println("   ➤ ID du robot   : " + data.get("id"));
            System.out.println("   ➤ ID instruction: " + data.get("inst_id"));

            // Traitement de la séquence d'instructions
            String instructionStr = data.get("instruction");
            if (instructionStr != null) {
                int[] instructions = parseInstruction(instructionStr);
                System.out.print("   ➤ Instructions  : ");
                for (int inst : instructions) {
                    System.out.print(inst + " ");
                }
                System.out.println("\n");
            } else {
                System.out.println("⚠️ Aucune instruction reçue.");
            }

        } catch (IOException e) {
            System.err.println("❌ Erreur lors de la récupération des données du robot :");
            e.printStackTrace();
        }
    }

    /**
     * Lance l'interface graphique principale du simulateur
     */
    private static void lancerInterface() {
        JFrame frame = new JFrame("Simulateur de Robot");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Récupération des IDs depuis les données API
        String robotId = data.getOrDefault("id", "inconnu");
        String instId = data.getOrDefault("inst_id", "0");
        int[]  cubes= convertirEnTableau(data.getOrDefault("instruction", "0"));

        // Ajout du panneau principal
        frame.setContentPane(new RobotPanel(robotId, Integer.parseInt(instId), cubes));
        frame.pack();
        frame.setVisible(true);
    }

    /**
     * Utilise Gson pour parser une chaîne JSON en un dictionnaire clé-valeur
     */
    public static Map<String, String> parseJson(String json) {
        Gson gson = new Gson();
        Type type = new TypeToken<Map<String, String>>() {}.getType();
        return gson.fromJson(json, type);
    }

    /**
     * Convertit une chaîne comme "3,4,5" en un tableau d'entiers
     */
    public static int[] parseInstruction(String instructionString) {
        String[] parts = instructionString.split(",");
        int[] result = new int[parts.length];

        for (int i = 0; i < parts.length; i++) {
            try {
                result[i] = Integer.parseInt(parts[i].trim());
            } catch (NumberFormatException e) {
                System.err.println("⚠️ Erreur de conversion pour '" + parts[i] + "' → remplacé par -1.");
                result[i] = -1;
            }
        }
        return result;
    }

    public static int[] convertirEnTableau(String str) {
        String[] parties = str.split(",");                // Divide la cadena por comas
        int[] resultat = new int[parties.length];

        for (int i = 0; i < parties.length; i++) {
            try {
                resultat[i] = Integer.parseInt(parties[i].trim());  // Elimina espacios y convierte
            } catch (NumberFormatException e) {
                resultat[i] = -1; // Si hay error, ponemos -1
                System.err.println("⚠️ Erreur de conversion pour '" + parties[i] + "'");
            }
        }

        return resultat;
    }
}
