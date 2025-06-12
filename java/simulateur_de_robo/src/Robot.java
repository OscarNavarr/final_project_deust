import java.awt.*;

class RobotSimule {
    private Point position;
    private final Color color;

    public RobotSimule(Point start, Color color) {
        this.position = start;
        this.color = color;
    }

    public boolean moveToward(Point target, double speed) {
        double dx = target.x - position.x;
        double dy = target.y - position.y;
        double dist = Math.hypot(dx, dy);
        if (dist < speed) {
            position = target;
            return true;
        }
        int nx = (int) (position.x + dx / dist * speed);
        int ny = (int) (position.y + dy / dist * speed);
        position = new Point(nx, ny);
        return false;
    }

    public void draw(Graphics g) {
        g.setColor(color);
        g.fillOval(position.x - 10, position.y - 10, 20, 20);
    }

    public void setPosition(Point p) {
        this.position = p;
    }

    public Point getPosition() {
        return position;
    }
}
