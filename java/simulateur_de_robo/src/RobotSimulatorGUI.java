import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class RobotSimulatorGUI extends JFrame {
    private JLabel statusLabel;
    private JTextField robotIdField;

    public RobotSimulatorGUI() {
        setTitle("Simulateur de Robot");
        setSize(500, 200);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        // Campo de texto para ID del robot
        JLabel robotIdLabel = new JLabel("UUID du robot : ");
        robotIdField = new JTextField("robot003", 20); // valor por defecto

        // Botón para obtener el estado
        JButton getStatusButton = new JButton("Obtenir le statut");

        // Etiqueta donde se muestra el estado
        statusLabel = new JLabel("Statut: ...");

        // Acción del botón
        getStatusButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                fetchAndDisplayStatus();
            }
        });

        // Paneles
        JPanel inputPanel = new JPanel();
        inputPanel.add(robotIdLabel);
        inputPanel.add(robotIdField);
        inputPanel.add(getStatusButton);

        JPanel statusPanel = new JPanel();
        statusPanel.add(statusLabel);

        // Layout de la ventana
        setLayout(new BorderLayout());
        add(inputPanel, BorderLayout.NORTH);
        add(statusPanel, BorderLayout.CENTER);
    }

    private void fetchAndDisplayStatus() {
        String robotId = robotIdField.getText().trim();
        try {
            String status = RobotClient.getRobotStatus(robotId);
            statusLabel.setText("Statut: " + status);
        } catch (Exception ex) {
            statusLabel.setText("Erreur : " + ex.getMessage());
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            RobotSimulatorGUI gui = new RobotSimulatorGUI();
            gui.setVisible(true);
        });
    }
}
