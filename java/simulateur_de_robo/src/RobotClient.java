import java.io.*;
import java.net.*;

public class RobotClient {
    private static final String BASE_URL = "http://127.0.0.1:8000"; // adresse de mon serveur FastAPI

    public static String getRobotStatus(String robotId) throws IOException {
        URL url = new URL(BASE_URL + "/robot/" + robotId + "/status");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");

        BufferedReader in = new BufferedReader(
                new InputStreamReader(con.getInputStream())
        );

        StringBuilder content = new StringBuilder();
        String inputLine;
        while ((inputLine = in.readLine()) != null) {
            content.append(inputLine);
        }
        in.close();
        con.disconnect();

        return content.toString(); // format JSON
    }
}
