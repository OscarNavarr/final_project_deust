import java.util.Scanner;

public class RobotSimulator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Entrez l'UUID du robot à simuler : ");
        String robotId = scanner.nextLine();

        System.out.println("Début de la simulation du robot " + robotId + "...\n");

        while (true) {
            try {
                String status = RobotClient.getRobotStatus(robotId);
                System.out.println("État du robot : " + status);
                Thread.sleep(3000); // attend 3 secondes
            } catch (Exception e) {
                System.out.println("Erreur lors de la communication avec le serveur : " + e.getMessage());
                break;
            }
        }

        scanner.close();
    }
}
