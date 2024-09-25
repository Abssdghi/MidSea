from tkinter import *
import time, random, os

def move_player(event):
    global game_status
    if 32 <= event.x <= 356:
        game.coords(player, event.x - 10, game.coords(player)[1])
        if game_status == 0:
            game_status = 1
            spawn_rocks()

def continue_game(rock):
    global game_status, score, score_display, player, upgraded_to_lifeboat, upgraded_to_darknight
    while True:
        root.update()
        try:
            if not game.coords(rock):
                break
            game.move(rock, 0, 14)

            if (game.coords(rock)[0]) < (game.coords(player)[0]) < (game.coords(rock)[0] + rock_image.width()) and (450 < game.coords(rock)[1] < 570):
                game_status = 0
                end_game()
                break

            if game.coords(rock)[1] > 641:
                score += 100
                game.delete(score_display)
                score_display = game.create_text(0, 0, text=f'Score: {score}', font=('system', 20), anchor=NW, fill='white')

                if score > 2000 and not upgraded_to_lifeboat:
                    game.itemconfig(player, image=lifeboat_image)
                    upgraded_to_lifeboat = True
                if score > 5000 and not upgraded_to_darknight:
                    game.itemconfig(player, image=darknight_image)
                    upgraded_to_darknight = True
                break
        except IndexError:
            break
        time.sleep(0.01)

def spawn_rocks():
    global game_status
    while game_status == 1:
        for _ in range(random.randint(1, 3)):
            if game_status == 0:
                return
            rock = game.create_image(random.randint(0, 270), -60, image=rock_image, anchor=NW)
            continue_game(rock)
        root.update()
        root.update_idletasks()

def end_game():
    game.delete("all")
    game.create_image(0, 0, image=gameover_image, anchor=NW)
    root.bind('<Button-1>', restart_game)
    root.bind('<q>', lambda e: os._exit(0))

def restart_game(event):
    root.unbind('<Button-1>')
    start_game()

def start_game():
    global game_status, score, score_display, player, upgraded_to_lifeboat, upgraded_to_darknight
    game_status = 0
    score = 0
    upgraded_to_lifeboat = False
    upgraded_to_darknight = False

    game.pack()
    game.create_image(0, 0, image=background_image, anchor=NW)
    player = game.create_image(181, 574, image=boat_image)
    score_display = game.create_text(0, 0, text=f'Score: {score}', font=('system', 20), anchor=NW, fill='white')

    game.tag_bind(player, "<B1-Motion>", move_player)

WIDTH, HEIGHT = 360, 640
root = Tk()
root.geometry(f'{WIDTH}x{HEIGHT}')
root.resizable(width=0, height=0)
root.title('MidSea')
background_image = PhotoImage(file='sea.png')
gameover_image = PhotoImage(file='gameover.png')
darknight_image = PhotoImage(file='darknight.png')
lifeboat_image = PhotoImage(file='lifeboat.png')
boat_image = PhotoImage(file='boatinthewoods.png')
rock_image = PhotoImage(file='rock.png')
root.iconphoto(1, background_image)

game = Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)

start_game()
root.mainloop()
