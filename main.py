import pygame

class Line:
    x: int = 0
    y: int = 0
    x2: int = 0
    y2: int = 0
    yIntercept: int = 0
    gradientRise: int = 0
    gradientRun: int = 0
    calculated: bool = False
    formatteted:bool = False
    method: str = ""
    id: int = 0
    active: bool = False
    colour:tuple = (255, 255, 255)
    
    """def __init__(self, yIntercept: int, gradientRise: int, gradientRun: int):
        self.yIntercept = yIntercept
        self.gradientRise = gradientRise
        self.gradientRun = gradientRun"""
        
    def __init__(self, method: str, id: int):
        self.method = method
        self.id = id
        
    def formatMethod(self, method: str):
        try:
            split = []
            positive: bool = True
            if not 'x' in method:
                if "/" in method:
                    self.gradientRise = int(method.split("/")[0])
                    self.gradientRun = int(method.split("/")[1])
                else:
                    self.gradientRise = int(method)
                    self.gradientRun = 1
            else:
                if "x+" in method:
                    split = method.split("x+")
                elif "x-" in method:
                    split = method.split("x-")
                    positive = False
                gradient = split[0]
                if "/" in gradient:
                    self.gradientRise = int(gradient.split("/")[0])
                    self.gradientRun = int(gradient.split("/")[1])
                else:
                    self.gradientRise = int(gradient)
                    self.gradientRun = 1
                if positive:
                    self.yIntercept = int(split[1])
                elif not positive:
                    self.yIntercept = -int(split[1])
                else:
                    self.yIntercept = 0
            self.formatteted = True
        except:
            self.x = 0
            self.y = 0
            self.x2 = 0
            self.y2 = 0
            
    def setMethod(self, method: str):
        self.method = method
        
    def getMethod(self) -> str:
        return self.method
    
    def getID(self) -> int:
        return self.id
        
    def getFormatteted(self) -> bool:
        return self.formatteted
        
    def getCalculated(self) -> bool:
        return self.calculated
    
    def calculate(self):
        self.formatMethod(self.getMethod())
        self.x = 0
        self.y = -self.yIntercept * 80
        self.x2 = 0
        self.y2 = 0
        for i in range(720):
            self.y += self.gradientRise
            self.y2 -= self.gradientRise
            self.x -= self.gradientRun
            self.x2 += self.gradientRun
        self.calculated = True
        print(f"Line {self.getID() + 1}: {self.getMethod()}({self.gradientRise},{self.gradientRun},{self.yIntercept})")

lines = []
"""lineAmount = int(input("Amount of lines: "))
for i in range(lineAmount):
    method = input(f"Line {i + 1}: ")
    lines.append(Line(method, i))"""

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Graphing calculator')
clock = pygame.time.Clock()
running = True

def drawText(text:str, surface: pygame.surface, x, y, size = 24, colour = (255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, True, colour)
    surface.blit(img, (x, y))
    
def stringWidth(text:str, size = 24) -> int:
    width: int = 0
    for letter in text:
        width += 1
    return width*(size/3)

while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            plus_box = pygame.Rect(20, 40, stringWidth("+", 40), plus_y)
            if plus_box.collidepoint(event.pos):
                lines.append(Line("1x+0", len(lines)))
            for line in lines:
                box = pygame.Rect(20, 40 + (line.getID() * 20), stringWidth(f"{line.getID() + 1}: {line.getMethod()}"), 15)
                if box.collidepoint(event.pos):
                    line.active = not line.active
                    line.calculate()
                else:
                    line.active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                for line in lines:
                    if line.active:
                        line.setMethod(line.method[:-1])
            else:
                for line in lines:
                    if line.active:
                        if event.key == pygame.K_RETURN:
                            line.calculate()
                            line.active = False
                            continue
                        line.setMethod(line.getMethod() + event.unicode)
                        line.calculate()
            
    screen.fill("black")
    width = 1280
    height = 720
    plus_y:int = 40
    colour = (255, 255, 255)
    pygame.draw.line(screen, colour, (width / 2, 0), (width / 2, height), 3)
    pygame.draw.line(screen, colour, (0, height / 2), (width, height / 2), 3)

    for line in lines:
        if not line.getCalculated():
            line.calculate()
        x = line.x
        y = line.y
        x2 = line.x2
        y2 = line.y2
        half_width = width / 2
        half_height = height / 2
        if line.active:
            line.colour = (150, 150, 150)
        else:
            line.colour = (255, 255, 255)
        drawText(f"{line.getID() + 1}: {line.getMethod()}", screen, 20, 40 + (line.getID() * 20), 24, line.colour)
        pygame.draw.line(screen, colour, (half_width + x, half_height + y), (half_width + x2, half_height + y2), 3)
        plus_y += 20
    
    drawText("+", screen, 20, plus_y, 40)

    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()