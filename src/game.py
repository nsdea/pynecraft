import time
import ursina
import threading

from ursina.prefabs.first_person_controller import FirstPersonController

def main():
    app = ursina.Ursina(
        # fullscreen=True,
        # borderless=True,
        show_ursina_splash=False,
        # editor_ui_enabled=True
    )

    def load_texture(texture: str):
        return ursina.load_texture(f'assets/{texture}.png')
    
    def load_sound(sound: str):
        return ursina.Audio(f'assets/sounds/{sound}', loop=False, autoplay=False)

    globals()['block_pick'] = 1

    ursina.window.vsync = False
    ursina.window.title = 'PyneCraft - Alpaha'
    ursina.window.fps_counter.enabled = True
    ursina.window.exit_button.visible = False

    triangley = None

    def slot():
        if ursina.held_keys['left mouse'] or ursina.held_keys['right mouse']:
            hand.active()
        else:
            hand.passive()

        for key in range(1, 9):
            if ursina.held_keys[str(key)]:
                globals()['block_pick'] = key
                
    class Voxel(ursina.Button):
        def __init__(
            self,
            position=(0, 0, 0),
            texture=load_texture('blocks/grass')
        ):

            super().__init__(
                parent=ursina.scene,
                position=position,
                model='assets/models/block',
                origin_y=0.5,
                texture=texture,
                color=ursina.color.color(0,0, ursina.random.uniform(0.9,1)),
                scale=0.5
            )

        def input(self, key):
            if self.hovered:
                slot()

                if key == 'right mouse down':
                    block_setup = []
                    for b in ['bricks', 'dirt', 'grass', 'stone']:
                        block_setup.append(load_texture('blocks/' + b))

                    Voxel(position=self.position + ursina.mouse.normal, texture=block_setup[globals()['block_pick']-1])

                if key == 'left mouse down':
                    load_sound('break').play()
                    ursina.destroy(self)

                if key == 'c':
                    ursina.camera.fov = 50

                if key == 'c up':
                    ursina.camera.fov = 90

                print(ursina.camera.x, ursina.camera.y)
                            

    class Sky(ursina.Entity):
        def __init__(self):
            super().__init__(
                parent=ursina.scene,
                model='sphere',
                texture=load_texture('textures/sky'),
                scale=150,
                double_sided=True
            )

    class Hand(ursina.Entity):
        def __init__(self):
            super().__init__(
                parent=ursina.camera.ui,
                model='assets/models/arm',
                texture=load_texture('textures/arm'),
                scale=0.2,
                rotation=ursina.Vec3(150,-10,0),
                position=ursina.Vec2(0.4,-0.6)
            )

        def active(self):
            self.position = ursina.Vec2(0.3, -0.5)

        def passive(self):
            self.position = ursina.Vec2(0.4, -0.6)

    for z in range(20):
        for x in range(20):
            Voxel(position=(x, 0, z))

    globals()['triangley'] = ursina.Entity(
        model='cube',
        texture='assets/blocks/dirt.png',
        # scale=0.2,
    )

    FirstPersonController()
    Sky()
    hand = Hand()

    def runner():
        while True:
            globals()['triangley'].color = ursina.color.random_color()
            time.sleep(0.1)

    threading.Thread(target=runner).start()

    app.run()