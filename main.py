import pandas as pd
from snake import *
from pygame.locals import *
import pygame
import random


def main():
    # PARAMETERS
    iterations = 2
    manual = True
    scores = []
    steps = []

    for i in range(iterations):
        score, avg_steps = play_game(manual)
        scores.append(score)
        steps.append(avg_steps)

        print(f"score: {score}\tsteps: {avg_steps}")

    history = pd.DataFrame({"scores": scores,
                            "avg_steps": steps})

    print(history)


if __name__ == "__main__":
    main()
