  # autor "kebe kadiatou"
try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
except:
    import Tkinter as tk

#cree le defenderer
class Defender(object):
    def __init__(self):
        self.width = 20
        self.height = 20
        self.move_delta = 20
        self.id = None
        self.max_fired_bullets = 8
        self.fired_bullets = []

    def install_in(self, canvas):
        lx = 600 + self.width / 2
        ly = 600 - self.height - 10
        self.id = canvas.create_rectangle(lx, ly, lx + self.width, ly + self.height, fill="white")

    #gere le deplacement sur les absices
    def move_in(self, canvas, dx):
        x1, y1, x2, y2 = canvas.bbox(self.id)
        if x2 > 1000 or x1 < 0:
            dx = -dx
        canvas.move(self.id, dx, 0)
        print(dx)

    #ajoute les bullets dans dans la liste tanque le max est aps atteint, gere leur deplacement aussi
    def fire(self, canvas):
        if len(self.fired_bullets) < self.max_fired_bullets:
            bullet = Bullets(self)
            self.fired_bullets.append(bullet)
            self.fired_bullets[-1].install_in(canvas)


#gere les bulle
class Bullets(object):
    def __init__(self, shooter):
        self.radius = 5
        self.speed = 30
        self.shooter = shooter
        self.jump_distance = -10
        self.id = None
        self.canvas = None
    
    def install_in(self, canvas):
        x, y, x1, y1 = canvas.coords(self.shooter.id)
        r = self.radius
        self.canvas = canvas
        self.id = canvas.create_oval(x, y, x + r, y + r,
                                     fill="red", tags="rect")

    #methode gerant la suppression de la bulle
    def move_in(self, canvas, dy):
        defense = Defender()
        canvas.move(self.id, 0, -self.speed)

        for bullet in self.shooter.fired_bullets:
            if canvas.coords(bullet.id)[1] < 0:
                self.shooter.fired_bullets.remove(bullet)
                self.canvas.delete(bullet.id)


class Alien(object):
    def __init__(self):
        self.id = None
        self.alive = True

    def install_in(self, canvas, x, y, image, tag):
        self.id = canvas.create_image(x, y, image=image, tags=tag)
    #deplacement
    def move_in(self, canvas,dx, dy):
        canvas.move(self.id, dx, dy)

    #effet qui se produit quand un alien est touche//// cette methode ne marche pas, je l'ai fait directement dans le managed touched de la la classe fleet
    
    def touched_by(self, canvas, projectile):
        self.shooter = Defender()
        self.alive = False
        canvas.delete(self.id)
        canvas.delete(projectile)
       
#classe de mon tableau aliens
class Fleet(object):
    def __init__(self):
        self.aliens_lines = 5
        self.aliens_columns = 10
        self.aliens_inner_gap = 20
        self.alien_x_delta = 5
        self.alien_y_delta = 10
        fleet_size = self.aliens_lines * self.aliens_columns
        self.aliens_fleet = [None] * fleet_size
        self.alive = True
        self.pim = tk.PhotoImage(file='alien.gif')
        self.tag = "alien"
        self.explosion = tk.PhotoImage(file='explosion.gif')
        self.alien = Alien()

    #creation de la flotte des aliens
    def install_in(self, canvas):
        self.x = 40
        self.y = 40
        k = 0

        for i in range(0, self.aliens_lines):
            for j in range(0, self.aliens_columns):
                self.alien = Alien()
                self.alien.install_in(canvas, self.x, self.y, self.pim, self.tag)
               
                if k < len(self.aliens_fleet):
                    self.aliens_fleet[k] = self.alien
                k = k + 1
                self.x += self.aliens_inner_gap + 60
            self.x = 40
            self.y += self.aliens_inner_gap + 35
    #deplacement de mon tableau daliens
    def move_in(self, canvas):
        vie=True
        maxX = int(canvas.cget("width"))
        all_rect_ids = canvas.find_withtag("alien")
        if len(self.aliens_fleet) != 0:
            x1, y1, x2, y2 = canvas.bbox("alien")
            if x2 > maxX:
                self.alien_x_delta = - self.alien_x_delta
                self.alien_y_delta = 10
            elif x1 < 0:
                self.alien_x_delta = - self.alien_x_delta
                self.alien_y_delta = 10
            else:
                self.alien_y_delta = 0
            for alien in self.aliens_fleet:
                if alien is not None:
                    alien.move_in(canvas, self.alien_x_delta, self.alien_y_delta)
               
    #gere les collision
    def manage_touched_aliens_by(self, canvas, defender):
        for bullet in (defender.fired_bullets):
            xb1,yb1,xb2,yb2=canvas.coords(bullet.id) 
            for alien in self.aliens_fleet:
                if alien is not None:
                    xa1, ya1, xa2, ya2 = canvas.bbox(alien.id)
                    if (xb1>=xa1 or xb2>=xa1) and (xb1<=xa2 or xb2<=xa2) and yb1<=ya2 and yb1>=ya1:
                    #if len(canvas.find_overlapping(xa1, ya1, xa2, ya2)) > 1:
                        print(len(canvas.find_overlapping(xa1, ya1, xa2, ya2)))
                        #try:
                        defender.fired_bullets.remove(bullet)
                        canvas.delete(bullet.id)
                        #except ValueError:
                            #pass
                        explose = canvas.create_image(xa1, ya1, image=self.explosion, tags="explosion")
                        canvas.after(120, canvas.delete, explose)
                        self.aliens_fleet.remove(alien)
                        canvas.delete(alien.id)

#classe ou s'appelle toutes les methode du programme en gros
class Game(object):

    #creer le canvas et appelle de mes classes
    def __init__(self, frame):
        width = 1000
        height = 600
        self.frame = frame

        self.canvas = tk.Canvas(self.frame, width=width, height=height, bg="black")
        self.canvas.pack(padx=5, pady=5)
        self.alien_x_delta = 5
        self.alien_y_delta = 10

        self.defender = Defender()

        self.alien = Alien()
        self.pim = tk.PhotoImage(file='alien.gif')
        self.tag = "alien"
        self.bullet = Bullets(self.defender)
        self.fleet = Fleet()

    def start(self):
        self.defender.install_in(self.canvas)
        self.frame.winfo_toplevel().bind("<Key>", self.keypress)
        self.fleet.install_in(self.canvas)
    #gère les deplacements via les touche du clavier
    def keypress(self, event):
        x = 0
        if event.keysym == 'Left':
            x = -30
            self.defender.move_in(self.canvas, x)
        elif event.keysym == 'Right':
            x = 30
            self.defender.move_in(self.canvas, x)
        elif event.keysym == 'space':
            self.defender.fire(self.canvas)

    
    def start_animation(self):
        self.start()
        self.jump_distance = -10
        self.canvas.after(0, self.animation)
    #gere l'animation de la bullet et la flotte d'alien
    def animation(self):
        for bullet in self.defender.fired_bullets:
            bullet.move_in(self.canvas, self.jump_distance)
        self.fleet.manage_touched_aliens_by(self.canvas, self.defender)
        self.fleet.move_in(self.canvas)
        self.canvas.after(300, self.animation)


class SpaceInvaders(object):
    ''' Main Game class '''
    #creer la frame
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        width = 1200
        height = 600
        self.frame = tk.Frame(self.root, width=width, height=height, bg="green")
        self.frame.pack()

        self.game = Game(self.frame)

    def play(self):
        self.game.start_animation()
        self.root.mainloop()


jeu = SpaceInvaders()
jeu.play()
# autor "kebe kadiatou"
