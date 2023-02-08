# import pyjsdl
import sys
import argparse
import pygame
import random
from dataclasses import dataclass
from typing import Optional
from enum import Enum

parser = argparse.ArgumentParser(
    prog="RPSLife", 
    description="A simple sim game of rock, paper, sicssors. Oh and also lizard and Spock."
)
parser.add_argument('-w', '--width', default=800, dest="width", type=int, metavar="WIDTH", help="Width of the game window.")
parser.add_argument('-v', '--height', default=800, dest="height", type=int, metavar="HEIGHT", help="Height of the game window.")
parser.add_argument('-f', '--frame_rate', default=15, dest='frame_rate', type=int, metavar="FRAMERATE", help="Game's max frame rate.")
parser.add_argument('-c', '--spawn_count', default=20, dest="spawn_count", type=int, metavar="SPAWNCOUNT", help="Number of enteies to spawn.")
parser.add_argument('-m', '--min_speed', default=-5, dest='min_speed', type=int, metavar="MINSPEED", help="Game tokens min move speed.")
parser.add_argument('-x', '--max_speed', default=5, dest='max_speed', type=int, metavar="MAXSPEED", help="Game tokens max move speed.")

width: int = 800
height: int = 800
frames: int = 0
kill_delay: int = 3
frame_rate: int = 15
image_scale: tuple[int, int] = (30, 30)
token_spawn_count: int = 20
min_speed: int = -5
max_speed: int = 5
scores: dict = {"Scissors": 0, "Paper": 0, "Rock": 0, "Lizard": 0, "Spock": 0}
winner = None


class TokenType(Enum):
    ROCK = {"filename": "RPSLife/images/rock2.png", "name": "Rock", "home": (400, 100)}
    PAPER = {"filename": "RPSLife/images/paper.png", "name": "Paper", "home": (100, 300)}
    SCISSOR = {"filename": "RPSLife/images/scissors.png", "name": "Scissors", "home": (700, 300)}
    LIZARD = {"filename": "RPSLife/images/lizard.png", "name": "Lizard", "home": (100, 600)}
    SPOCK = {"filename": "RPSLife/images/spock.png", "name": "Spock", "home": (600, 600)}
    TEXT = {"filename": "", "name": "text", "home": (400, 400)}


@dataclass
class Token:
    Type: TokenType
    Image: Optional[pygame.Surface] = None
    Rect: Optional[pygame.Rect] = None
    Position: Optional[list[int, int]] = None
    Speed: Optional[list[int, int]] = None
    Font: Optional[pygame.font.SysFont] = None
    Name: Optional[str] = None

    def __init__(self, my_type: TokenType, msg: Optional[str]=None, pos: Optional[list[int, int]] = None, 
                color: Optional[str] = None, font_size: Optional[int] = None) -> None:
        self.Type: Token.Type = my_type
        self.Name: str = self.Type.value['name']
        self.Image: Token.Image = None
        self.Rect: Token.Rect = None
        self.Position: Token.Position = None
        self.Speed: Token.Speed = None
        match self.Type:
            case TokenType.TEXT:
                self.Font = pygame.font.SysFont("bahnschrift", font_size, True)
                self.Image = pygame.font.Font.render(self.Font, msg.upper(), True, pygame.Color(color))
                self.Rect = self.Image.get_rect()
                self.Position = pos
                self.Speed = [0, 0]
            case _:
                self.Image = pygame.transform.scale(pygame.image.load(self.Type.value["filename"]), image_scale)
                self.Rect = self.Image.get_rect()
                self.Position = pos if pos is not None else pygame.Rect(self.Type.value["home"][0], self.Type.value["home"][1], self.Rect.width, self.Rect.height)
                self.Speed = [random.randint(min_speed, max_speed), random.randint(min_speed, max_speed)]
                self.Name = self.Type.value["name"]
                self.update_token_counts()
    
    def move_token(self) -> None:
        self.Position.move_ip(self.Speed)
    
    def transform(self, type: TokenType) -> None:
        scores[self.Type.value['name']] -= 1
        self.Type = type
        scores[self.Type.value['name']] += 1
        self.Image = pygame.transform.scale(
            pygame.image.load(self.Type.value['filename']), image_scale)

    def update_token_counts(self) -> None:
        match self.Type:
            case TokenType.ROCK:
                scores['Rock'] += 1
            case TokenType.SCISSOR:
                scores['Scissors'] += 1
            case TokenType.PAPER:
                scores['Paper'] += 1
            case TokenType.LIZARD:
                scores['Lizard'] += 1
            case TokenType.SPOCK:
                scores['Spock'] += 1


def print_msg(msg: str) -> None:
    global winner, width, height
    winner = Token(TokenType.TEXT, msg=msg, color="crimson", font_size=40)
    winner.Rect = winner.Image.get_rect()
    winner.Position = ((width/2)-(winner.Rect.width/2), (height/2)-(winner.Rect.height/2))


def border_check(i: Token) -> None:
    global width, height
    if i.Position.left < 0 or i.Position.right > width:
        i.Speed[0] = -i.Speed[0]
    if i.Position.top < 20 or i.Position.bottom > height - 20:
        i.Speed[1] = -i.Speed[1]


def token_hit(t: Token, tl: list[Token]) -> None:
    global scores
    # Checks if t collides with any rect in tl and return the first index otherwise -1
    r = t.Position.collidelist([tr.Position for tr in tl])
    c = tl[r]
    if r == -1:
        pass
    else:
        match t.Type:
            case TokenType.ROCK:
                # Rock (t) defeats Scissors & Lizard (c)
                if c.Type in (TokenType.SCISSOR, TokenType.LIZARD):
                    c.transform(type=t.Type)
                # Rock (t) is beaten by Paper & Spock (c)
                elif c.Type in (TokenType.PAPER, TokenType.SPOCK):
                    t.transform(type=c.Type)
            case TokenType.PAPER:
                # Paper (t) defeats Rock & Spock (c)
                if c.Type in (TokenType.ROCK, TokenType.SPOCK):
                    c.transform(type=t.Type)
                # Paper (t) is beaten by Scissors & Lizard (c)
                elif c.Type in (TokenType.SCISSOR, TokenType.LIZARD):
                    t.transform(type=c.Type)
            case TokenType.SCISSOR:
                # Scissors (t) defeats Paper & Lizard (c)
                if c.Type in (TokenType.PAPER, TokenType.LIZARD):
                    c.transform(type=t.Type)
                # Scissors (t) is beaten by Spock & Rock (c)
                elif c.Type in (TokenType.SPOCK, TokenType.ROCK):
                    t.transform(type=c.Type)
            case TokenType.LIZARD:
                # LIzard (t) defeats Spock & Paper (c)
                if c.Type in (TokenType.SPOCK, TokenType.PAPER):
                    c.transform(type=t.Type)
                # Lizard (t) is beaten by Scissors & Rock (c)
                elif c.Type in (TokenType.SCISSOR, TokenType.ROCK):
                    t.transform(type=c.Type)
            case TokenType.SPOCK:
                # Spock (t) defeats Rock & Scissors (c)
                if c.Type in (TokenType.ROCK, TokenType.SCISSOR):
                    c.transform(type=t.Type)
                # Spock (t) is beaten by Lizard & Paper (c)
                elif c.Type in (TokenType.LIZARD, TokenType.PAPER):
                    t.transform(type=c.Type)
    if all(x.Type==tl[0].Type for x in tl) is True:
        print_msg(msg=f"{tl[0].Type.value['name']} WINS !!!")


def main(*args, **kwargs) -> None:
    global width, height, frames, frame_rate, token_spawn_count, min_speed, max_speed, scores, winner, kill_delay
    width = kwargs['width']
    height = kwargs['height']
    frame_rate = kwargs['frame_rate']
    token_spawn_count = kwargs['spawn_count']
    min_speed = kwargs['min_speed']
    max_speed = kwargs['max_speed']

    pygame.init()
    pygame.font.init()
    clock: pygame.time.Clock = pygame.time.Clock()
    pygame.mixer.music.load('RPSLife/music/8-bit-game-music.mp3')
    pygame.mixer.music.play(loops=-1, fade_ms=kill_delay * 3000)
    
    screen_size: tuple[int, int] = (width, height)
    bg_color: pygame.Color = pygame.Color("darkslategray4")

    screen: pygame.display = pygame.display.set_mode(screen_size)

    tokens: list[Token] = [Token(TokenType.ROCK) for i in range(token_spawn_count)] + \
        [Token(TokenType.PAPER) for i in range(token_spawn_count)] + \
        [Token(TokenType.SCISSOR) for i in range(token_spawn_count)] + \
        [Token(TokenType.LIZARD) for i in range(token_spawn_count)] + \
        [Token(TokenType.SPOCK) for i in range(token_spawn_count)]

    rock_count: Token = Token(TokenType.TEXT, msg=f"ROCKS: {scores['Rock']}", pos=(50, 4), color="crimson", font_size=25)
    paper_count: Token = Token(TokenType.TEXT, msg=f"PAPERS: {scores['Paper']}", pos=(200, 4), color="crimson", font_size=25)
    scissor_count: Token = Token(TokenType.TEXT, msg=f"SCISSORS: {scores['Scissors']}", pos=(350, 4), color="crimson", font_size=25)
    lizard_count: Token = Token(TokenType.TEXT, msg=f"LIZARDS: {scores['Lizard']}", pos=(500, 4), color="crimson", font_size=25)
    spock_count: Token = Token(TokenType.TEXT, msg=f"SPOCKS: {scores['Spock']}", pos=(650, 4), color="crimson", font_size=25)

    controls: Token = Token(
        TokenType.TEXT, 
        msg=f"Controls: Press q to quit | Press r to restart", 
        pos=(4, 780), 
        color="crimson", 
        font_size=25
    )

    while True:
        clock.tick(frame_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                event_attributes = event.__dict__
                if event_attributes['unicode'] == "r":
                    print("Restarting...")
                    frames = 0
                    winner = None
                    scores = {
                        "Scissors": 0, 
                        "Paper": 0, 
                        "Rock": 0, 
                        "Lizard": 0, 
                        "Spock": 0
                    }
                    tokens: list[Token] = [Token(TokenType.ROCK) for i in range(token_spawn_count)] + \
                        [Token(TokenType.PAPER) for i in range(token_spawn_count)] + \
                        [Token(TokenType.SCISSOR) for i in range(token_spawn_count)] + \
                        [Token(TokenType.LIZARD) for i in range(token_spawn_count)] + \
                        [Token(TokenType.SPOCK) for i in range(token_spawn_count)]
                    pygame.mixer.music.play(loops=-1, fade_ms=kill_delay * 3000)
                elif event_attributes['unicode'] == 'q':
                    print("Quitting...")
                    pygame.quit()
                    sys.exit()

        screen.fill(bg_color)    
        for i in tokens:
            if frames > (frame_rate * kill_delay):
                i.move_token()
                border_check(i=i)
                token_hit(t=i, tl=tokens)
                screen.blit(i.Image, i.Position)
            elif frames <= (frame_rate * kill_delay):
                screen.blit(i.Image, i.Position)
        if winner:
            screen.blit(winner.Image, winner.Position)
        rock_count.Image = pygame.font.Font.render(rock_count.Font, f"ROCKS: {scores['Rock']}".upper(), True, pygame.Color("crimson"))
        screen.blit(rock_count.Image, rock_count.Position)
        paper_count.Image = pygame.font.Font.render(paper_count.Font, f"PAPERS: {scores['Paper']}".upper(), True, pygame.Color("crimson"))
        screen.blit(paper_count.Image, paper_count.Position)
        scissor_count.Image = pygame.font.Font.render(scissor_count.Font, f"SCISSORS: {scores['Scissors']}".upper(), True, pygame.Color("crimson"))
        screen.blit(scissor_count.Image, scissor_count.Position)
        lizard_count.Image = pygame.font.Font.render(lizard_count.Font, f"LIZARDS: {scores['Lizard']}".upper(), True, pygame.Color("crimson"))
        screen.blit(lizard_count.Image, lizard_count.Position)
        spock_count.Image = pygame.font.Font.render(spock_count.Font, f"SPOCKS: {scores['Spock']}".upper(), True, pygame.Color("crimson"))
        screen.blit(spock_count.Image, spock_count.Position)
        screen.blit(controls.Image, controls.Position)
        frames += 1
        pygame.display.update()


def rps_life() -> None:
    args = parser.parse_args()
    main(**vars(args))


if __name__ == "__main__":
    args = parser.parse_args()
    main(**vars(args))
