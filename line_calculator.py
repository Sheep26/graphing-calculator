import pygame

class Line:
    x: int = 0
    y: int = 0
    x2: int = 0
    y2: int = 0
    
    def __init__(self, yIntercept: int, gradientRise: int, gradientRun: int):
        self.y = -yIntercept * 108
        for i in range(1080):
            self.y += gradientRise
            self.y2 += -gradientRise
            self.x += gradientRun
            self.x2 -= gradientRun

lines = []
lineAmount = int(input("Amount of lines: "))
for i in range(lineAmount):
    print(f"Line {i + 1}")
    gradientRiseInput = int(input("Gradient rise: "))
    gradientRunInput = int(input("Gradient run: "))
    yInterceptInput = int(input("Y Intercept: "))
    lines.append(Line(yInterceptInput, gradientRiseInput, gradientRunInput))

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    width = 1920
    height = 1080
    colour = (255, 255, 255)
    pygame.draw.line(screen, colour, (width / 2, 0), (width / 2, height), 3)
    pygame.draw.line(screen, colour, (0, height / 2), (width, height / 2), 3)
        
    for line in lines:
        x = line.x
        y = line.y
        x2 = line.x2
        y2 = line.y2
        half_width = width / 2
        half_height = height / 2
        pygame.draw.line(screen, colour, (half_width + x, half_height + y), (half_width + x2, half_height + y2), 3)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()