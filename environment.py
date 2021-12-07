import sys
import random
from copy import copy
import os
import melee
import numpy as np
from getThread import GetThread
from moveset import Moveset
from postThread import PostThread
from reward import Reward
from agent import Agent


def actSpecific(agentData, agent):
    if np.random.rand() < agent.epsilon:
        return random.sample(agent.possible_actions, 1)[0]

    else:
        x = agent.model.predict(agentData)
        return agent.possible_actions[np.argmax(x, axis=1)[0]]


def getState(playerData, gameDone):
    return [playerData.stock, playerData.percent, playerData.off_stage, playerData.on_ground,
            playerData.shield_strength, playerData.speed_air_x_self, playerData.speed_ground_x_self,
            playerData.speed_x_attack, playerData.speed_y_attack, playerData.speed_y_self, playerData.position.x,
            playerData.position.y, playerData.facing]


def combineStates(player1Data, player2Data):
    player1DataCopy = copy(player1Data)
    player1DataCopy.extend(player2Data)
    return player1DataCopy


if __name__ == "__main__":
    DOLPHIN_PATH = 'C:/Users/sonor/AppData/Roaming/Slippi Launcher/netplay'

    PORT = 2
    OPPONENT_PORT = 1
    console = melee.Console(path=DOLPHIN_PATH)
    controller = melee.Controller(console=console, port=2, type=melee.ControllerType.STANDARD)
    controller_opponent = melee.Controller(console=console, port=1, type=melee.ControllerType.STANDARD)

    agent = Agent()
    # agent.model.predict(np.asarray([0 for _ in range(44)]))

    console.run(iso_path="C:/Users/sonor/Desktop/supersmash/Super Smash Bros. Melee (USA) (En,Ja) (v1.02).iso")

    # Connect to the console
    print("Connecting to console...")
    if not console.connect():
        print("ERROR: Failed to connect to the console.")
        sys.exit(-1)
    print("Console connected")

    # Plug our controller in
    #   Due to how named pipes work, this has to come AFTER running dolphin
    #   NOTE: If you're loading a movie file, don't connect the controller,
    #   dolphin will hang waiting for input and never receive it
    print("Connecting controller to console...")
    if not controller.connect():
        print("ERROR: Failed to connect the controller.")
        sys.exit(-1)
    print("Controller connected")

    print("Connecting controller to console...")
    if not controller_opponent.connect():
        print("ERROR: Failed to connect the controller.")
        sys.exit(-1)
    print("Controller Opponent connected")

    costume = 0
    i = 0

    getThread = GetThread()
    getThread.start()
    getThread.join()

    if os.path.exists('recentweights.hdf5'):
        print("Loading Weights!")
        agent.model.load_weights('recentweights.hdf5')

    moveset = Moveset(controller)
    moveset1 = Moveset(controller_opponent)

    ACTIONS = [moveset.moveLeft, moveset.moveRight, moveset.crouch, moveset.sprintLeft,
               moveset.sprintRight, moveset.jumpLeft, moveset.jumpRight, moveset.jump, moveset.BDown, moveset.BLeft,
               moveset.BRight, moveset.BUp, moveset.tiltLeftA, moveset.tiltRightA, moveset.tiltDownA,
               moveset.tiltUpA, moveset.cUp, moveset.cDown, moveset.cLeft, moveset.cRight,
               moveset.shield, moveset.dodgeLeft, moveset.dodgeRight, moveset.spotDodge,
               moveset.doNothing, moveset.A, moveset.B, moveset.grab, moveset.forwardARight, moveset.forwardALeft]

    FRAMES = {'moveLeft': 4, 'moveRight': 4, 'crouch': 4, 'shield': 8, 'jab0': 21, 'jab1': 19, 'jab2': 29,
              'forwardTilt': 29,
              'upTilt': 39, 'downTilt': 35, 'dashAttack': 39, 'forwardSmash': 64, 'upSmash': 51, 'downSmash': 49,
              'neutralAir': 44, 'forwardAir': 39, 'backAir': 35, 'upAir': 33, 'downAir': 44, 'neutralB': 99,
              'sideB': 70, 'upB': 64, 'downB': 64, 'airDownB': 57, 'spotDodge': 32, 'backRoll': 31, 'forwardRoll': 31,
              'airDodge': 49, 'grab': 29, 'forwardThrow': 39, 'backThrow': 49, 'downThrow': 39, 'upThrow': 43,
              'forwardALeft': 39,
              'forwardARight': 39}

    # Manually map each of the components to its frame data
    actionToName = {'0': 'moveLeft', '1': 'moveRight', '2': 'crouch', '3': 'moveLeft',
                    '4': 'moveRight', '5': 'moveLeft', '6': 'moveRight', '7': 'moveLeft',
                    '8': 'downB', '9': 'sideB', '10': 'sideB', '11': 'upB', '12': 'forwardTilt',
                    '13': 'forwardTilt', '14': 'downTilt', '15': 'upTilt', '16': 'upSmash',
                    '17': 'downSmash', '18': 'forwardSmash', '19': 'forwardSmash', '20': 'shield',
                    '21': 'backRoll', '22': 'forwardRoll', '23': 'spotDodge', '24': 'shield',
                    '25': 'jab0', '26': 'neutralB', '27': 'grab', '28': 'forwardSmash',
                    '29': 'forwardSmash'}

    # This is for captain falcon's jab. Changes frame data depending on which one he is on
    jabCount = 0

    rewardPlayer = Reward()
    rewardOpponent = Reward()

    gameDone = False
    allp1States = []
    allp1Rewards = []
    allp1NextStates = []
    allp1Actions = []
    allp1Dones = []
    allp1PreviousActions = []

    postThreads = []
    getThreads = []
    previousMove = 0
    moveCount = 0
    firstRun = True
    agentAction = 0
    firstMove = True
    previousAction = 0

    while True:
        gamestate = console.step()

        if gamestate is None:
            continue
        # The console object keeps track of how long your bot is taking to process frames
        #   And can warn you if it's taking too long
        # if console.processingtime * 1000 > 12:
        #     print("WARNING: Last frame took " + str(console.processingtime * 1000) + "ms to process.")

        if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:

            # Slippi Online matches assign you a random port once you're in game that's different
            #   than the one you're physically plugged into. This helper will autodiscover what
            #   port we actually are.
            discovered_port = PORT

            player1Data = gamestate.players[controller.port]

            player2Data = gamestate.players[controller_opponent.port]

            if discovered_port > 0:
                if i / (previousMove + 1) == 1:
                    controller.release_all()
                    i = 0
                    moveCount += 1

                    # Get the states
                    playerOneState = np.array(
                        combineStates(getState(player1Data, gameDone), getState(player2Data, gameDone)))

                    if firstMove:
                        action = [0.0 for _ in range(30)]
                        playerOneState = np.append(playerOneState, action)
                    else:
                        action = [0.0 for _ in range(30)]
                        action[previousAction] = 1.0
                        playerOneState = np.append(playerOneState, action)

                    if np.random.rand() < agent.epsilon:
                        agentAction = random.sample(agent.possible_actions, 1)[0]
                        previousAction = agentAction
                        actionName = actionToName[f'{agentAction}']

                        if not player1Data.on_ground:
                            if actionName == 'downB':
                                previousMove = FRAMES['airDownB']
                                actionName = 'airDownB'
                            if actionName == 'forwardTilt' or actionName == 'upSmash' or actionName == 'forwardALeft' or actionName == 'forwardARight':
                                previousMove = FRAMES['forwardAir']
                                actionName = 'forwardAir'
                            if actionName == 'upTilt':
                                previousMove = FRAMES['upAir']
                                actionName = 'upAir'
                            if actionName == 'forwardTilt' or actionName == 'forwardARight' or actionName == 'forwardSmash' and player1Data.facing == 1:
                                previousMove = FRAMES['forwardAir']
                                actionName = 'forwardAir'
                            if actionName == 'forwardTilt' or actionName == 'forwardARight' or actionName == 'forwardSmash' and player1Data.facing != 1:
                                previousMove = FRAMES['backAir']
                                actionName = 'backAir'
                            if actionName == 'forwardTilt' or actionName == 'forwardALeft' or actionName == 'forwardSmash' and player1Data.facing == 1:
                                previousMove = FRAMES['backAir']
                                actionName = 'backAir'
                            if actionName == 'forwardTilt' or actionName == 'forwardALeft' or actionName == 'forwardSmash' and player1Data.facing != 1:
                                previousMove = FRAMES['forwardAir']
                                actionName = 'forwardAir'
                            if actionName == 'downTilt':
                                previousMove = FRAMES['downTilt']
                                actionName = 'downTilt'
                            if actionName == 'shield' or actionName == 'spotDodge' or actionName == 'forwardRoll' or actionName == 'backRoll':
                                previousMove = FRAMES['spotDodge']
                                actionName = 'spotDodge'
                            if actionName == 'jab0':
                                if jabCount > 2:
                                    jabCount = 0
                                previousMove = FRAMES[f'jab{jabCount}']


                        else:
                            previousMove = FRAMES[actionName]
                    else:
                        playerOneStateReshape = np.array(playerOneState).reshape(1, -1)
                        x = agent.model.predict(playerOneStateReshape)[0]
                        agentAction = agent.possible_actions[np.argmax(x)]
                        previousAction = agentAction

                        actionName = actionToName[f'{agentAction}']

                        if not player1Data.on_ground:
                            if actionName == 'downB':
                                previousMove = FRAMES['airDownB']
                                actionName = 'airDownB'
                            if actionName == 'forwardTilt' or actionName == 'upSmash' or actionName == 'forwardALeft' or actionName == 'forwardARight':
                                previousMove = FRAMES['forwardAir']
                                actionName = 'forwardAir'
                            if actionName == 'upTilt':
                                previousMove = FRAMES['upAir']
                                actionName = 'upAir'
                            if actionName == 'forwardTilt' or actionName == 'forwardARight' or actionName == 'forwardSmash' and player1Data.facing == 1:
                                previousMove = FRAMES['forwardAir']
                                actionName = 'forwardAir'
                            if actionName == 'forwardTilt' or actionName == 'forwardARight' or actionName == 'forwardSmash' and player1Data.facing != 1:
                                previousMove = FRAMES['backAir']
                                actionName = 'backAir'
                            if actionName == 'forwardTilt' or actionName == 'forwardALeft' or actionName == 'forwardSmash' and player1Data.facing == 1:
                                previousMove = FRAMES['backAir']
                                actionName = 'backAir'
                            if actionName == 'forwardTilt' or actionName == 'forwardALeft' or actionName == 'forwardSmash' and player1Data.facing != 1:
                                previousMove = FRAMES['forwardAir']
                                actionName = 'forwardAir'
                            if actionName == 'downTilt':
                                previousMove = FRAMES['downTilt']
                                actionName = 'downTilt'
                            if actionName == 'shield' or actionName == 'spotDodge' or actionName == 'forwardRoll' or actionName == 'backRoll':
                                previousMove = FRAMES['spotDodge']
                                actionName = 'spotDodge'
                            if actionName == 'jab0':
                                if jabCount > 2:
                                    jabCount = 0
                                previousMove = FRAMES[f'jab{jabCount}']
                                jabCount += 1
                        else:
                            previousMove = FRAMES[actionName]

                    # Perform the action
                    ACTIONS[agentAction]()

                    agentReward = rewardPlayer.understandState(player1Data, player2Data)

                    allp1States.append(playerOneState)
                    allp1Actions.append(agentAction)
                    allp1Rewards.append(agentReward)
                    allp1NextStates.append(np.asarray(
                        combineStates(getState(gamestate.players[controller.port], gameDone),
                                      getState(gamestate.players[controller_opponent.port], gameDone))).astype(
                        'float32').tolist())
                    allp1PreviousActions.append(agentAction)

                    previousAction = action
                    # allp1NextStates.append(state)
                else:
                    ACTIONS[agentAction]()

                i += 1
                # if moveLag == 0:
                #     i += 1

                # Get the rewards for its actions and such

                if player2Data.stock == 0:
                    firstMove = True

                    gameDone = True

                    agentReward = 1000
                    allp1Dones.append(gameDone)
                    agentReward += rewardPlayer.understandState(player1Data, player2Data)

                    allp1Rewards.append(agentReward)

                    if not firstRun:
                        for thread in postThreads:
                            thread.join()
                        postThreads = []
                        for thread in getThreads:
                            thread.join()
                        getThreads = []
                    postThread = PostThread(allp1States, allp1NextStates, allp1Actions, allp1Rewards, allp1Dones,
                                            controller.port, allp1PreviousActions)
                    postThreads.append(postThread)
                    postThread.start()

                    agent.adaptiveEGreedy()

                    with open('epsilon.txt', 'w') as f:
                        f.write(str(agent.epsilon))

                    rewardPlayer.reset()
                    rewardOpponent.reset()

                    getThread = GetThread()
                    getThreads.append(getThread)
                    getThread.start()

                    allp1States = []
                    allp1Rewards = []
                    allp1NextStates = []
                    allp1Actions = []
                    allp1Dones = []


                elif player1Data.stock == 0:
                    firstMove = True
                    gameDone = True
                    agentReward = -1000

                    allp1Dones.append(gameDone)

                    agentReward += rewardPlayer.understandState(player1Data, player2Data)
                    allp1Rewards.append(agentReward)

                    if not firstRun:
                        for thread in postThreads:
                            thread.join()
                        postThreads = []
                        for thread in getThreads:
                            thread.join()
                        getThreads = []

                    postThread = PostThread(allp1States, allp1NextStates, allp1Actions, allp1Rewards, allp1Dones,
                                            controller.port, allp1PreviousActions)
                    postThreads.append(postThread)

                    postThread.start()

                    agent.adaptiveEGreedy()
                    with open('epsilon.txt', 'w') as f:
                        f.write(str(agent.epsilon))

                    rewardPlayer.reset()

                    allp1States = []
                    allp1Rewards = []
                    allp1NextStates = []
                    allp1Actions = []
                    allp1Dones = []

                    getThread = GetThread()
                    getThreads.append(getThread)
                    getThread.start()


                else:
                    allp1Dones.append(gameDone)


            else:
                # If the discovered port was unsure, reroll our costume for next time
                costume = random.randint(0, 4)

            if gamestate.ready_to_start == 0 and gameDone:
                gameDone = False
                controller.press_button(melee.enums.Button.BUTTON_START)
                controller_opponent.press_button(melee.enums.Button.BUTTON_START)

            if gamestate.menu_state in [melee.Menu.STAGE_SELECT]:
                melee.MenuHelper.choose_stage(melee.Stage.FINAL_DESTINATION, gamestate, controller)

        elif gamestate.menu_state in [melee.Menu.STAGE_SELECT]:
            melee.MenuHelper.choose_stage(melee.Stage.FINAL_DESTINATION, gamestate, controller)

        else:

            melee.MenuHelper.choose_character(melee.Character.CPTFALCON,
                                              gamestate,
                                              controller,
                                              cpu_level=0,
                                              start=False
                                              )

            melee.MenuHelper.menu_helper_simple(gamestate,
                                                controller_opponent,
                                                melee.Character.CPTFALCON,
                                                melee.Stage.FINAL_DESTINATION,
                                                "",
                                                costume=0,
                                                cpu_level=1,
                                                autostart=True,
                                                swag=False)

            if gamestate.ready_to_start == 0 and gameDone:
                gameDone = False
                controller.press_button(melee.enums.Button.BUTTON_START)
                controller_opponent.press_button(melee.enums.Button.BUTTON_START)

            if gamestate.menu_state in [melee.Menu.STAGE_SELECT]:
                melee.MenuHelper.choose_stage(melee.Stage.FINAL_DESTINATION, gamestate, controller)
