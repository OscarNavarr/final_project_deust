import java.awt.*;

class Bouton {
    private final Rectangle bounds;
    private final String text;
    private final Color color;

    public Bouton(int x, int y, int width, int height, String text, Color color) {
        this.bounds = new Rectangle(x, y, width, height);
        this.text = text;
        this.color = color;
    }

    public void draw(Graphics g) {
        g.setColor(color);
        g.fillRect(bounds.x, bounds.y, bounds.width, bounds.height);
        g.setColor(Color.BLACK);
        g.drawString(text, bounds.x + 15, bounds.y + 15);
    }

    public boolean contains(Point p) {
        return bounds.contains(p);
    }


}
