

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Arrays;


public class RobotPanel extends JPanel implements ActionListener, MouseListener {
    private final int WIDTH = 800, HEIGHT = 800;
    private final Color BLANC = Color.WHITE;
    private final Color NOIR = Color.BLACK;
    private final Color[] CUBE_COULEURS = {
            Color.RED, Color.YELLOW, Color.GREEN, new Color(255, 105, 180), new Color(128, 0, 128)
    };

    private ArrayList<Point> parcoursPoints;
    private int[] cubeIndices = {10, 30, 60, 90, 50};
    private boolean[] cubeAttrapes;
    private boolean[] cubeDeposes;
    private int selectedCubeIndex = -1;
    private int indexPoint = 0;
    private String modeRobot = "attente";
    private Timer timer;
    private ArrayList<Bouton> boutons;
    private boolean aLeCube = false;
    private RobotSimule robot;

    private final int zoneStockageIndex1 = 20;
    private final int zoneStockageIndex2 = 80;
    private final int zoneTraitOffset = 15;

    private String robotId = "robot003"; // Valeur par défaut

    public RobotPanel() {
        setPreferredSize(new Dimension(WIDTH, HEIGHT));
        setBackground(BLANC);
        addMouseListener(this);

        parcoursPoints = new ArrayList<>();
        double centerX = WIDTH / 2.0;
        double centerY = HEIGHT / 2.0;
        double width = 450;
        double height = 250;
        int steps = 100;

        for (int i = 0; i < steps; i++) {
            double t = (double) i / steps;
            double angle = 2 * Math.PI * t;
            double rx = width / 2 * (1 + 0.1 * Math.sin(3 * angle));
            double ry = height / 2 * (1 + 0.1 * Math.cos(5 * angle));
            int x = (int) (centerX + rx * Math.cos(angle));
            int y = (int) (centerY + ry * Math.sin(angle));
            parcoursPoints.add(new Point(x, y));
        }

        robot = new RobotSimule(parcoursPoints.get(0), new Color(0, 100, 255));


        cubeAttrapes = new boolean[cubeIndices.length];
        cubeDeposes = new boolean[cubeIndices.length];
        Arrays.fill(cubeAttrapes, false);
        Arrays.fill(cubeDeposes, false);
        boutons = new ArrayList<>();

        timer = new Timer(16, this);
        timer.start();
    }

    public void setRobotId(String id) {
        this.robotId = id;
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;

        // Ligne
        g2.setColor(NOIR);
        for (int i = 0; i < parcoursPoints.size() - 1; i++) {
            Point p1 = parcoursPoints.get(i);
            Point p2 = parcoursPoints.get(i + 1);
            g2.drawLine(p1.x, p1.y, p2.x, p2.y);
        }

        // Zones stockage
        float[] dash = {10f, 10f};
        g2.setStroke(new BasicStroke(4, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER, 10f, dash, 0f));
        g2.setColor(Color.DARK_GRAY);

        Point zone1 = parcoursPoints.get(zoneStockageIndex1);
        g2.drawLine(zone1.x - zoneTraitOffset - 10, zone1.y, zone1.x - zoneTraitOffset + 1, zone1.y);

        Point zone2 = parcoursPoints.get(zoneStockageIndex2);
        g2.drawLine(zone2.x - zoneTraitOffset - 10, zone2.y, zone2.x - zoneTraitOffset + 15, zone2.y);

        // Cubes
        for (int i = 0; i < cubeIndices.length; i++) {
            if (!cubeAttrapes[i]) {
                Point p = parcoursPoints.get(cubeIndices[i]);
                g2.setColor(CUBE_COULEURS[i]);
                g2.fillRect(p.x - 10, p.y - 10, 20, 20);
            } else if (cubeDeposes[i]) {
                Point stockage = parcoursPoints.get((i % 2 == 0) ? zoneStockageIndex1 : zoneStockageIndex2);
                g2.setColor(CUBE_COULEURS[i]);
                g2.fillRect(stockage.x - 10 + i * 5, stockage.y - 10 + i * 5, 15, 15);
                g2.setColor(Color.BLACK);
                g2.drawString("Cube " + (i + 1) + " déposé", stockage.x + 20, stockage.y + 20 + i * 10);
            }
        }

        robot.draw(g2);

        boutons.clear();
        for (int i = 0; i < cubeIndices.length; i++) {
            Bouton bouton = new Bouton(20, 20 + i * 50, 100, 20, "Cube " + (i + 1), CUBE_COULEURS[i]);
            bouton.draw(g2);
            boutons.add(bouton);
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if ("vers_cube".equals(modeRobot) && selectedCubeIndex >= 0) {
            int cibleIdx = cubeIndices[selectedCubeIndex];
            if (indexPoint != cibleIdx) {
                indexPoint = moveRobot(indexPoint, cibleIdx);
            } else {
                cubeAttrapes[selectedCubeIndex] = true;
                aLeCube = true;
                modeRobot = "vers_stockage";
            }
        } else if ("vers_stockage".equals(modeRobot)) {
            int stockageIndex = (selectedCubeIndex % 2 == 0) ? zoneStockageIndex1 : zoneStockageIndex2;
            if (indexPoint != stockageIndex) {
                indexPoint = moveRobot(indexPoint, stockageIndex);
            } else {
                aLeCube = false;
                cubeDeposes[selectedCubeIndex] = true;
                modeRobot = "attente";

                // ENVOI API : cube déposé
                try {
                    RobotClient.sendRobotStatus(robotId, String.valueOf(indexPoint), "drop_c" + selectedCubeIndex);
                } catch (Exception ex) {
                    System.out.println("Erreur API: " + ex.getMessage());
                }

                selectedCubeIndex = -1;
            }
        }
        repaint();
    }

    private int moveRobot(int current, int target) {
        int next = (current < target) ? current + 1 : current - 1;
        Point cible = parcoursPoints.get(next);
        if (robot.moveToward(cible, 2)) {
            return next;
        }
        return current;
    }

    @Override
    public void mouseClicked(MouseEvent e) {
        Point pos = e.getPoint();
        for (int i = 0; i < boutons.size(); i++) {
            if (boutons.get(i).contains(pos) && !cubeAttrapes[i]) {
                selectedCubeIndex = i;
                indexPoint = findClosestPointIndex(robot.getPosition());
                modeRobot = "vers_cube";

                // ENVOI API : cube choisi
                try {
                    RobotClient.sendRobotStatus(robotId, String.valueOf(indexPoint), "pickup_c" + selectedCubeIndex);
                } catch (Exception ex) {
                    System.out.println("Erreur API: " + ex.getMessage());
                }
                break;
            }
        }
    }

    private int findClosestPointIndex(Point p) {
        int minIndex = 0;
        double minDist = Double.MAX_VALUE;
        for (int i = 0; i < parcoursPoints.size(); i++) {
            double d = p.distance(parcoursPoints.get(i));
            if (d < minDist) {
                minDist = d;
                minIndex = i;
            }
        }
        return minIndex;
    }

    @Override public void mousePressed(MouseEvent e) {}
    @Override public void mouseReleased(MouseEvent e) {}
    @Override public void mouseEntered(MouseEvent e) {}
    @Override public void mouseExited(MouseEvent e) {}
}
