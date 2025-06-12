import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

public class RobotClient {
    private static final String BASE_URL = "http://127.0.0.1:8000";

    // Obtener el estado del robot
    public static String getRobotStatus(String robotId) throws IOException {
        URL url = new URL(BASE_URL + "/robot/" + robotId + "/status");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");
        return readResponse(con);
    }

    // Crear un nuevo robot
    public static String createRobot(String name) throws IOException {
        String query = String.format("/robot/?name=%s", URLEncoder.encode(name, "UTF-8"));
        URL url = new URL(BASE_URL + query);
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("POST");
        return readResponse(con);
    }

    // Enviar un nuevo estado del robot
    public static String sendStatus(String robotId, String position, String status) throws IOException {
        String query = String.format(
                "/status/?robot_id=%s&position=%s&status=%s",
                URLEncoder.encode(robotId, "UTF-8"),
                URLEncoder.encode(position, "UTF-8"),
                URLEncoder.encode(status, "UTF-8")
        );
        URL url = new URL(BASE_URL + query);
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("POST");
        return readResponse(con);
    }
    public static String getInstructions(String robotId) throws IOException {
        String query = String.format("/instructions?robot_id=%s", URLEncoder.encode(robotId, "UTF-8"));
        URL url = new URL(BASE_URL + query);
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");
        return readResponse(con);
    }

    // Listar todos los robots
    public static String listRobots() throws IOException {
        URL url = new URL(BASE_URL + "/robots/");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");
        return readResponse(con);
    }

    public static String sendRobotStatus(String robotId, String position, String status) throws IOException {
        String query = String.format(
                "/update_status/?robot_id=%s&position=%s&status=%s",
                URLEncoder.encode(robotId, "UTF-8"),
                URLEncoder.encode(position, "UTF-8"),
                URLEncoder.encode(status, "UTF-8")
        );
        URL url = new URL(BASE_URL + query);
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("POST");
        return readResponse(con);
    }


    // Método reutilizable para leer la respuesta HTTP
    private static String readResponse(HttpURLConnection con) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
        StringBuilder content = new StringBuilder();
        String inputLine;
        while ((inputLine = in.readLine()) != null) {
            content.append(inputLine);
        }
        in.close();
        con.disconnect();
        return content.toString();
    }
}
