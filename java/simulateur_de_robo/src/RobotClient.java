import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.io.*;



public class RobotClient {
    private static final String BASE_URL = "http://127.0.0.1:8000";
    private static final String MAC_ADDRESS = "12312fz-12dd-1dad-11da5";


    // Obtener el estado del robot por su idRobot
    public static String getRobotStatus(String robotId) throws IOException {
        URL url = new URL(BASE_URL + "/robot/" + robotId + "/status");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");
        return readResponse(con);
    }

    // Obtenir les info du robot pour son adresse Mac
    public static String getRobotDataByUUID(String uuid) throws IOException {
        // Crear el JSON para enviar
        String jsonInputString = String.format("{\"uuid\": \"%s\"}", uuid);

        // Crear la URL y conexión
        URL url = new URL(BASE_URL + "/robot_data_by_uuid");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Content-Type", "application/json");
        con.setDoOutput(true);

        // Enviar el JSON en el cuerpo de la solicitud
        try (OutputStream os = con.getOutputStream()) {
            byte[] input = jsonInputString.getBytes("utf-8");
            os.write(input, 0, input.length);
        }


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

    public static String sendRobotStatus(String robotId, int instructionID, String position, String status) throws IOException {
        String jsonInputString = String.format(
                "{\"robot_id\":\"%s\", \"instructionID\":\"%s\", \"position\":\"%s\", \"status\":\"%s\"}",
                robotId, instructionID, position, status
        );

        URL url = new URL(BASE_URL + "/update_status/");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Content-Type", "application/json");
        con.setDoOutput(true);

        try (OutputStream os = con.getOutputStream()) {
            byte[] input = jsonInputString.getBytes("utf-8");
            os.write(input, 0, input.length);
        }

        String response = readResponse(con);
        System.out.println("Respuesta del servidor: " + response);  // 👈 Imprime aquí
        return response;
    }


    // Método reutilizable para leer la respuesta HTTP
    private static String readResponse(HttpURLConnection con) throws IOException {
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(con.getInputStream(), "utf-8"))) {
            StringBuilder response = new StringBuilder();
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
            return response.toString();
        }
    }

}
