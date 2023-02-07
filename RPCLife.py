import sys
import pygame
import random
import argparse
from dataclasses import dataclass
from typing import Optional
from enum import Enum

frames = 0
kill_delay = 1
frame_rate = 15
winner = None
image_scale = (30, 30)
token_spawn_count = 20
min_speed = -5
max_speed = 5
scores: dict = {"Scissors": 0, "Paper": 0, "Rock": 0, "Lizard": 0, "Spock": 0}


class TokenType(Enum):
    ROCK = {"filename": "images/rock2.png", "name": "Rock", "home": (400, 100)}
    PAPER = {"filename": "images/paper.png", "name": "Paper", "home": (100, 300)}
    SCISSOR = {"filename": "images/scissors.png", "name": "Scissors", "home": (700, 300)}
    LIZARD = {"filename": "images/lizard.png", "name": "Lizard", "home": (100, 600)}
    SPOCK = {"filename": "images/spock.png", "name": "Spock", "home": (600, 600)}
    TEXT = {"filename": "", "name": "text", "home": (400, 400)}


@dataclass
class Token:
    Type: TokenType
    Image: Optional[pygame.Surface] = None
    Rect: Optional[pygame.Rect] = None
    Position: Optional[list[int, int]] = None
    Speed: Optional[list[int, int]] = None
    Font: Optional[pygame.font.SysFont] = None
    Msg: Optional[str] = None
    Name: Optional[str] = None

    def __init__(self, my_type: TokenType, msg: Optional[str]=None, pos: Optional[list[int, int]] = None, 
                color: Optional[str] = None, font_size: Optional[int] = None) -> None:
        self.Type: Token.Type = my_type
        self.Name = self.Type.value['name']
        self.Image: Token.Image = None
        self.Rect: Token.Rect = None
        self.Position: Token.Position = None
        self.Speed: Token.Speed = None
        match self.Type:
            case TokenType.TEXT:
                self.Font = pygame.font.SysFont("bahnschrift", font_size, True)
                self.Msg = msg
                self.Image = pygame.font.Font.render(
                    self.my_font, 
                    self.Msg.upper(), 
                    True, 
                    pygame.Color(color)
                )
                self.Rect = self.Image.get_rect()
                self.Position = pos
                self.Speed = [0, 0]
            case _:
                self.Image = pygame.transform.scale(pygame.image.load(self.Type.value["filename"]), image_scale)
                self.Rect = self.Image.get_rect()
                self.Position = pos if pos is not None else pygame.Rect(self.Type.value["home"][0], self.Type.value["home"][1], self.Rect.width, self.Rect.height)
                self.Speed = [random.randint(min_speed, max_speed), random.randint(min_speed, max_speed)]
                self.update_token_counts()
    
    def update_score(self) -> None:
        __msg = f"{self.Msg}: {scores[ ]}"
        self.Image = pygame.font.Font.render(
            self.my_font, 
            msg.upper(), 
            True, 
            pygame.Color(color)
        )
    
    def move_token(self) -> None:
        self.Position.move_ip(self.Speed)
    
    def transform(self, type: TokenType) -> None:
        self.Type = type
        self.Image = pygame.transform.scale(
            pygame.image.load(self.Type.value['filename']), image_scale)

    def update_token_counts(self) -> None:
        match self.Type:
            case TokenType.ROCK:
                scores['Rock'] += 1
            case TokenType.PAPER:
                scores['Scissors'] += 1
            case TokenType.PAPER:
                scores['Paper'] += 1
            case TokenType.LIZARD:
                scores['Lizard'] += 1
            case TokenType.SPOCK:
                scores['Spock'] += 1


pygame.init()
clock: pygame.time.Clock = pygame.time.Clock()
pygame.font.init()
width: int = 800
height: int = 800
screen_size: tuple[int, int] = (width, height)
bg_color: pygame.Color = pygame.Color("darkslategray4")

screen: pygame.display = pygame.display.set_mode(screen_size)

tokens: list[Token] = [Token(TokenType.ROCK) for i in range(token_spawn_count)] + \
    [Token(TokenType.PAPER) for i in range(token_spawn_count)] + \
    [Token(TokenType.SCISSOR) for i in range(token_spawn_count)] + \
    [Token(TokenType.LIZARD) for i in range(token_spawn_count)] + \
    [Token(TokenType.SPOCK) for i in range(token_spawn_count)]

rock_count: Token = Token(TokenType.TEXT, msg=f"ROCKS: {scores['Rock']}", pos=(2, 2), color="crimson", font_size=25)
paper_count: Token = Token(TokenType.TEXT, msg=f"PAPERS: {scores['Paper']}", pos=(150, 2), color="crimson", font_size=25)
scissor_count: Token = Token(TokenType.TEXT, msg=f"SCISSORS: {scores['Scissors']}", pos=(300, 2), color="crimson", font_size=25)
lizard_count: Token = Token(TokenType.TEXT, msg=f"LIZARDS: {scores['Lizard']}", pos=(450, 2), color="crimson", font_size=25)
spock_count: Token = Token(TokenType.TEXT, msg=f"SPOCKS: {scores['Spock']}", pos=(600, 2), color="crimson", font_size=25)


def print_msg(msg: str) -> None:
    global winner
    winner = Token(TokenType.TEXT, msg=msg, pos=((width/2)-(winner.Position.width/2), (height/2)-(winner.Position.height/2)), 
                    color="crimson", font_size=40)


def border_check(i: Token) -> None:
    if i.Position.left < 0 or i.Position.right > width:
        i.Speed[0] = -i.Speed[0]
    if i.Position.top < 0 or i.Position.bottom > height:
        i.Speed[1] = -i.Speed[1]


def token_hit(t: Token, tl: list[Token]) -> None:
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
                    scores[t.Type.value['name']] = scores[t.Type.value['name']] + 1
                    scores[c.Type.value['name']] = scores[c.Type.value['name']] - 1
                # Rock (t) is beaten by Paper & Spock (c)
                elif c.Type in (TokenType.PAPER, TokenType.SPOCK):
                    t.transform(type=c.Type)
                    scores[t.Type.value['name']] -= 1
                    scores[c.Type.value['name']] += 1
            case TokenType.PAPER:
                # Paper (t) defeats Rock & Spock (c)
                if c.Type in (TokenType.ROCK, TokenType.SPOCK):
                    c.transform(type=t.Type)
                    scores[t.Type.value['name']] += 1
                    scores[c.Type.value['name']] -= 1
                # Paper (t) is beaten by Scissors & Lizard (c)
                elif c.Type in (TokenType.SCISSOR, TokenType.LIZARD):
                    t.transform(type=c.Type)
                    scores[t.Type.value['name']] -= 1
                    scores[c.Type.value['name']] += 1
            case TokenType.SCISSOR:
                # Scissors (t) defeats Paper & Lizard (c)
                if c.Type in (TokenType.PAPER, TokenType.LIZARD):
                    c.transform(type=t.Type)
                    scores[t.Type.value['name']] += 1
                    scores[c.Type.value['name']] -= 1
                # Scissors (t) is beaten by Spock & Rock (c)
                elif c.Type in (TokenType.SPOCK, TokenType.ROCK):
                    t.transform(type=c.Type)
                    scores[t.Type.value['name']] -= 1
                    scores[c.Type.value['name']] += 1
            case TokenType.LIZARD:
                # LIzard (t) defeats Spock & Paper (c)
                if c.Type in (TokenType.SPOCK, TokenType.PAPER):
                    c.transform(type=t.Type)
                    scores[t.Type.value['name']] += 1
                    scores[c.Type.value['name']] -= 1
                # Lizard (t) is beaten by Scissors & Rock (c)
                elif c.Type in (TokenType.SCISSOR, TokenType.ROCK):
                    t.transform(type=c.Type)
                    scores[t.Type.value['name']] -= 1
                    scores[c.Type.value['name']] += 1
            case TokenType.SPOCK:
                # Spock (t) defeats Rock & Scissors (c)
                if c.Type in (TokenType.ROCK, TokenType.SCISSOR):
                    c.transform(type=t.Type)
                    scores[t.Type.value['name']] += 1
                    scores[c.Type.value['name']] -= 1
                # Spock (t) is beaten by Lizard & Paper (c)
                elif c.Type in (TokenType.LIZARD, TokenType.PAPER):
                    t.transform(type=c.Type)
                    scores[t.Type.value['name']] -= 1
                    scores[c.Type.value['name']] += 1
    if all(x.Type==tl[0].Type for x in tl) is True:
        print_msg(msg=f"{tl[0].Type.value['name']} WINS !!!")

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
                tokens: list[Token] = [Token(TokenType.ROCK) for i in range(token_spawn_count)] + \
                    [Token(TokenType.PAPER) for i in range(token_spawn_count)] + \
                    [Token(TokenType.SCISSOR) for i in range(token_spawn_count)] + \
                    [Token(TokenType.LIZARD) for i in range(token_spawn_count)] + \
                    [Token(TokenType.SPOCK) for i in range(token_spawn_count)]
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
    screen.blit(rock_count.Image, rock_count.Position)
    screen.blit(paper_count.Image, paper_count.Position)
    screen.blit(scissor_count.Image, scissor_count.Position)
    screen.blit(lizard_count.Image, lizard_count.Position)
    screen.blit(spock_count.Image, spock_count.Position)
    frames += 1
    pygame.display.update()