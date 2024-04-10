# A shell for running one of several apps

import microbit as M
import music

# Import app modules
import app_tilt1    # 'Tilt' test
import app_fly_up   # 'Fly up' game

# Register apps
_apps = [
    (app_tilt1.main, app_tilt1.ICON),
    (app_fly_up.main, app_fly_up.ICON),
]

#-----------------------------------------
# utils

def play_anim(frameStrings, frameDelay, repeatCount = 1):
    for i in range(repeatCount):
        for s in frameStrings:
            M.display.show(M.Image(s))
            M.sleep(frameDelay)

def reset_buttons():
    "reset buttons memory"
    M.button_a.was_pressed()
    M.button_b.was_pressed()
    

#-----------------------------------------
# main loop

def main():

    index = 0  # index of selected app

    def update_app_icon():
        icon = _apps[index][1]
        M.display.show(icon)

    
    music.play(music.POWER_UP, wait=False)
    
    update_app_icon()
    
    while True:
    
        # [A] to choose an app
        if M.button_a.was_pressed():
            index += 1
            index %= len(_apps)
            music.play(['c4:1'], wait=False)
            update_app_icon()
    
        # [B] to run the app
        if M.button_b.was_pressed():
            music.play(['g4:1','b4:3'])
            M.sleep(500)
            reset_buttons()

            # run the app and wait until exit
            run = _apps[index][0]
            run()
    
            # now the app is closed - play exit animation
            music.play(['b4:3','g4:1'], wait=False)
            play_anim([
                "90009:00000:00000:00000:90009",
                "00000:07070:00000:07070:00000",
                "00000:00000:00500:00000:00000",
            ], 500)
            reset_buttons()
            update_app_icon()
    
        
        if M.pin_logo.is_touched():  # touch logo for exit the shell
            music.play(music.POWER_DOWN, wait=False)
            play_anim([
                "90909:00000:90009:00000:90909",
                "00700:07070:70007:07070:00700",
                "00000:00500:05550:00500:00000",
                "00000:00000:00300:00000:00000",
                "00000:00000:00000:00000:00000",
            ], 200)
            break
        
        M.sleep(50)


if __name__ == '__main__':
    main()