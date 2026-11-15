"""GameOverView: draws the colourful pixel-art "GAME OVER" screen (display only)."""
import pygame

# Each letter is a 5 x 7 grid of pixels ("#" = filled).
GLYPHS = {
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
}
RED, CYAN, YELLOW, GREEN = (235, 40, 40), (90, 200, 245), (250, 240, 40), (90, 235, 40)
LINES = [("GAME", [RED, CYAN, YELLOW, GREEN]),
         ("OVER", [GREEN, YELLOW, CYAN, RED])]


class GameOverView:
    """Dims the game and shows GAME OVER, the final score and the keys."""

    PIXEL = 14          # size of one letter pixel
    OUTLINE = 6         # thickness of the black outline

    def __init__(self):
        self.title = self._build_title()
        self.font = pygame.font.Font(None, 40)
        self.small = pygame.font.Font(None, 30)

    def draw(self, surface, score):
        shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 170))
        surface.blit(shade, (0, 0))

        centre_x = surface.get_width() // 2
        title_rect = self.title.get_rect(center=(centre_x, surface.get_height() // 2 - 50))
        surface.blit(self.title, title_rect)

        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        surface.blit(score_text, score_text.get_rect(center=(centre_x, title_rect.bottom + 35)))
        keys_text = self.small.render("R = play again     Esc = quit", True, (200, 200, 210))
        surface.blit(keys_text, keys_text.get_rect(center=(centre_x, title_rect.bottom + 75)))

    def _build_title(self):
        p, o = self.PIXEL, self.OUTLINE
        letter_w, letter_h, gap = 5 * p, 7 * p, 2 * p
        width = 4 * letter_w + 3 * gap + 2 * o
        height = 2 * letter_h + gap + 2 * o
        image = pygame.Surface((width, height), pygame.SRCALPHA)

        cells = []                                  # (rect, colour) of every lit pixel
        for row, (word, colours) in enumerate(LINES):
            for i, (char, colour) in enumerate(zip(word, colours)):
                left = o + i * (letter_w + gap)
                top = o + row * (letter_h + gap)
                for gy, line in enumerate(GLYPHS[char]):
                    for gx, cell in enumerate(line):
                        if cell == "#":
                            cells.append((pygame.Rect(left + gx * p, top + gy * p, p, p), colour))

        for rect, _ in cells:                       # 1) black outline behind everything
            pygame.draw.rect(image, (0, 0, 0), rect.inflate(2 * o, 2 * o), border_radius=o)
        for rect, colour in cells:                  # 2) the coloured pixels on top
            pygame.draw.rect(image, colour, rect)
        return image
