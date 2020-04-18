import sys 
import pygame
import pygame_gui
import run
import threading
from battlehack20 import CodeContainer, Game, BasicViewer, GameConstants


def runGUI():
    pygame.init()
    pygame.display.set_caption('BattleHacks Zepharch')
    window_surface = pygame.display.set_mode((800, 700))

    background = pygame.Surface((800, 700))
    background.fill(pygame.Color('#66AD40'))

    manager = pygame_gui.UIManager((800, 700))

    stepButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 610), (700, 80)),
                                                text='Step Turn',
                                                manager=manager)

    clock = pygame.time.Clock()
    is_running = True
    # run.play_all(delay = 0.1, keep_history = True, real_time = True)
    run.viewer = BasicViewer(GameConstants.BOARD_SIZE, run.game.board_states, colors=False)
    run.viewer_poison_pill = threading.Event()
    run.viewer_thread = threading.Thread(target=run.viewer.play_synchronized, args=(run.viewer_poison_pill,), kwargs={'delay': 0.1, 'keep_history': True})
    run.viewer_thread.daemon = True
    run.viewer_thread.start()


    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == stepButton:
                        run.step()

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()
    # run.viewer_thread.stop()
    run.viewer_poison_pill.set()
    sys.exit()
    # run.viewer_thread.join()
    

if __name__ == "__main__":
    args = sys.argv
    print(args)

    code_container1 = CodeContainer.from_directory(args[1])
    code_container2 = CodeContainer.from_directory(args[2])

    run.game = Game([code_container1, code_container2], board_size=GameConstants.BOARD_SIZE, max_rounds=GameConstants.MAX_ROUNDS, 
                seed=GameConstants.DEFAULT_SEED, debug=True, colored_logs=True)
    runGUI()