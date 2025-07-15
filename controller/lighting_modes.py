import threading
import time
import math
import random

class LightingManager:
    """
    Manager pentru animațiile dinamice de iluminare pe grid-ul APC.
    Fiecare modul este implementat ca funcție dedicată.
    """
    def __init__(self, midi_out_apc, fps=30):
        self.midi_out = midi_out_apc
        self.fps = fps
        self.current_thread = None
        self.stop_event = threading.Event()
        self.modes = {
            1: self.rainbow_breath,
            2: self.expanding_square,
            3: self.ripple,
            4: self.snake_game,
            5: self.sparkle,
            6: self.fireworks,
            7: self.theater_chase,
            8: self.off,
        }

    def set_mode(self, mode_index):
        if self.current_thread and self.current_thread.is_alive():
            self.stop_event.set()
            self.current_thread.join()
        self.stop_event.clear()
        fn = self.modes.get(mode_index, self.off)
        self.current_thread = threading.Thread(target=fn, daemon=True)
        self.current_thread.start()

    def off(self):
        for pad in range(64):
            self.midi_out.send_message([0x96, pad, 0])

    def rainbow_breath(self):
        t0 = time.time()
        while not self.stop_event.is_set():
            t = time.time() - t0
            brightness = (1 + math.sin(2 * math.pi * 0.05 * t)) / 2
            for pad in range(64):
                hue = (pad * 5 + t * 10) % 360
                vel = self.hue_to_velocity(hue, brightness)
                self.midi_out.send_message([0x96, pad, vel])
            time.sleep(1 / self.fps)

    def expanding_square(self):
        t0 = time.time()
        max_size = 4
        while not self.stop_event.is_set():
            t = time.time() - t0
            size = int((math.sin(2 * math.pi * 0.1 * t) + 1) / 2 * max_size) + 1
            hue = (t * 30) % 360
            for pad in range(64):
                y, x = divmod(pad, 8)
                center = 3.5
                vel = self.hue_to_velocity(hue) if abs(x - center) < size and abs(y - center) < size else 0
                self.midi_out.send_message([0x96, pad, vel])
            time.sleep(1 / self.fps)

    def ripple(self):
        t0 = time.time()
        center = (3.5, 3.5)
        maxd = math.hypot(3.5, 3.5)
        while not self.stop_event.is_set():
            t = time.time() - t0
            for pad in range(64):
                y, x = divmod(pad, 8)
                d = math.hypot(y - center[0], x - center[1])
                phase = ((t * 0.3 - d) % maxd) / maxd
                hue = (phase * 360) % 360
                vel = self.hue_to_velocity(hue)
                self.midi_out.send_message([0x96, pad, vel])
            time.sleep(1 / self.fps)

    def snake_game(self):
        """Modul 4: Snake fără coliziuni cu sine, verde și roșu pe măr."""
        snake = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
        apple = self.random_apple(snake)
        step_time = 0.5
        last_move = time.time()
        # Direcții posibile: sus, jos, stânga, dreapta
        dirs = [( -1,0),(1,0),(0,-1),(0,1)]
        while not self.stop_event.is_set():
            now = time.time()
            if now - last_move > step_time:
                head_y, head_x = snake[-1]
                # generează mutări sigure: nu intersectează corpul
                moves = []
                for dy,dx in dirs:
                    ny, nx = (head_y+dy)%8, (head_x+dx)%8
                    if (ny,nx) not in snake:
                        moves.append((ny,nx))
                # alege mutarea care minimizează distanța la măr, dacă există
                if moves:
                    # calculează distanța Manhattan la apple
                    best = min(moves, key=lambda p: abs(p[0]-apple[0])+abs(p[1]-apple[1]))
                    new_head = best
                else:
                    # blocat — ia orice direcție, va muri
                    dy,dx = random.choice(dirs)
                    new_head = ((head_y+dy)%8,(head_x+dx)%8)
                snake.append(new_head)
                if new_head == apple:
                    apple = self.random_apple(snake)
                else:
                    snake.pop(0)
                if len(snake)>=64:
                    snake=snake[:5]; apple=self.random_apple(snake)
                last_move = now
            # desenare
            for pad in range(64):
                y,x = divmod(pad,8)
                if (y,x) in snake:
                    vel = 21
                elif (y,x)==apple:
                    vel = 6
                else:
                    vel = 0
                self.midi_out.send_message([0x96,pad,vel])
            time.sleep(1/self.fps)

    def fireworks(self):
        bursts = []
        lifetime = 1.5
        while not self.stop_event.is_set():
            now = time.time()
            if random.random() < 0.04:
                bursts.append({'center':(random.randint(1,6),random.randint(1,6)),'hue':random.random()*360,'t0':now})
            velocities=[0]*64
            for fw in bursts[:]:
                age=now-fw['t0']
                if age>lifetime: bursts.remove(fw); continue
                radius=(age/lifetime)*4
                for pad in range(64):
                    y,x=divmod(pad,8)
                    d=math.hypot(y-fw['center'][0],x-fw['center'][1])
                    if d<radius*0.2: vel=self.hue_to_velocity(fw['hue'],1)
                    elif abs(d-radius)<0.5: vel=self.hue_to_velocity(fw['hue'],1-abs(d-radius)/0.5)
                    else: vel=0
                    velocities[pad]=max(velocities[pad],vel)
            for p,v in enumerate(velocities): self.midi_out.send_message([0x96,p,v])
            time.sleep(1/self.fps)

    def sparkle(self):
        while not self.stop_event.is_set():
            pad=random.randint(0,63)
            hue=random.random()*360
            vel=self.hue_to_velocity(hue,1)
            self.midi_out.send_message([0x96,pad,vel])
            time.sleep(1/self.fps)

    def theater_chase(self):
        t0=time.time(); length=3
        while not self.stop_event.is_set():
            t=time.time()-t0;off=int(t*5)%length;hue=(t*40)%360
            for pad in range(64): self.midi_out.send_message([0x96,pad,127 if (pad+off)%length==0 else 0])
            time.sleep(1/self.fps)

    def debug_palette(self):
        hues=list(range(0,360,30))+[0]
        print("--- Debug Palette Start: Hue -> Velocity ---")
        for hue in hues:
            vel=self.hue_to_velocity(hue,1)
            print(f"Hue:{hue:3}->Vel:{vel}")
            self.midi_out.send_message([0x96,0,vel]); time.sleep(0.5)
        self.midi_out.send_message([0x96,0,0])
        print("--- Debug Palette End ---")

    def random_apple(self,snake): return random.choice([(i//8,i%8) for i in range(64) if (i//8,i%8) not in snake])
    def hue_to_velocity(self,h,b=1.0): return max(0,min(127,int((h/360.0)*127*b)))
