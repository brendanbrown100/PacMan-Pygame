import os


class GameEngine(object):

    def __init__(self):

        self.levelObjects = [[levelObject("empty") for j in range(32)] for i in range(28)]   # generate 28x32 empty objects
        self.movingObjectPacman = movingObject("Pacman")
        self.movingObjectGhosts = [movingObject("Ghost") for n in range(4)]

        self.levelObjectNamesBlocker = ["wall", "cage"]
        self.levelObjectNamesPassable = ["empty", "pellet", "powerup"]


    def levelGenerate(self, level):
        # set a directory for the resource file
        pathCurrentDir = os.path.dirname(__file__)  # current script directory
        pathRelDir = "../resource/level{}.txt".format(level)
        pathAbsDir = os.path.join(pathCurrentDir, pathRelDir)

        levelFile = open(pathAbsDir, encoding="utf-8")
        levelLineNo = 0

        # read line by line with readlines(), 'levelLine' temporarily save the string
        for levelLine in levelFile.readlines():

            levelLineSplit = list(levelLine) # split levelLine into characters

            # generate level objects
            for i in range(28):

                if levelLineSplit[i] == "_":    # passage
                    self.levelObjects[i][levelLineNo].name = "empty"
                elif levelLineSplit[i] == "#":  # wall
                    self.levelObjects[i][levelLineNo].name = "wall"
                elif levelLineSplit[i] == "$":  # ghost spawn point
                    self.levelObjects[i][levelLineNo].name = "cage"
                elif levelLineSplit[i] == ".":  # score pellet
                    self.levelObjects[i][levelLineNo].name = "pellet"
                elif levelLineSplit[i] == "*":  # power pellet
                    self.levelObjects[i][levelLineNo].name = "powerup"

                elif levelLineSplit[i] == "@":  # pacman
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # give the starting coordinate
                    self.movingObjectPacman.coordinateRel[0] = i
                    self.movingObjectPacman.coordinateRel[1] = levelLineNo
                    self.movingObjectPacman.coordinateAbs[0] = i * 3
                    self.movingObjectPacman.coordinateAbs[1] = levelLineNo * 3


                elif levelLineSplit[i] == "&":  # ghost
                    self.levelObjects[i][levelLineNo].name = "empty"

                    # find an inactive ghost and give the starting coordinate
                    for n in range(4):
                        if self.movingObjectGhosts[n].isActive == False:
                            self.movingObjectGhosts[n].isActive = True
                            self.movingObjectGhosts[n].coordinateRel[0] = i
                            self.movingObjectGhosts[n].coordinateRel[1] = levelLineNo
                            self.movingObjectGhosts[n].coordinateAbs[0] = i * 3
                            self.movingObjectGhosts[n].coordinateAbs[1] = levelLineNo * 3
                            break   # break current loop (with generator 'n')

            levelLineNo += 1 # indicate which line we are

        levelFile.close()


    def loopFunction(self):
        self.movingObjectPacman.MoveNext(self)
        self.movingObjectPacman.MoveCurrent(self)

        #for i in range(4):
        #    self.movingObjectGhosts[i].MoveNext(self)
        #    self.movingObjectGhosts[i].MoveCurrent(self)




# treading Timer
    # 주인공은 지정된 방향으로 좌표 이동, moveRequest를 해당 방향으로
    # 만약 주인공 좌표가 (x,y)이고 방향이 right라면 (x,y+1)에 해당하는 오브젝트의 moveRequest를 불러온다
    # moveRequest의 return을 받아보고 갈 수 있는지 여부를 판단하고 실제 이동에 해당하는 function을 불러온다
    # 실제 이동에 해당하는 function은 좌표계를 3개로 쪼개서 이동하면서 스프라이트를 바꿔준다

    # if문을 이용하여 wall, pellet은 pass하고 팩맨, 고스트 등 움직이는 오브젝트만 place로 좌표를 재지정한다


    # 귀신들은 ai 만들기 힘드니까 지정된 구역 순찰해놓고 v1.1.0에서 알고리즘 develop해서 릴리즈
    # 한칸씩 움직임






class levelObject(object):

    def __init__(self, name):
        self.name = name
        self.isDestroyed = False

    def moveRequest(self):
        return self.name



class movingObject(object):

    def __init__(self, name):
        self.name = name
        self.isActive = False   # check this object is an active ghost (not used for pacman)
        self.dirCurrent = "Left" # current direction, if cannot move w/ dirNext, the object will proceed this direction
        self.dirNext = "Left"   # the object will move this direction if it can
        self.coordinateRel = [0, 0]   # Relative Coordinate, check can the object move given direction
        self.coordinateAbs = [0, 0]   # Absolute Coordinate, use for widget(image) and object encounters

    def MoveNext(self, GameEngine):
        ## this function will determine the object can move with given direction or not

        if self.dirNext == self.dirCurrent: # in this case, no action is required
            pass
        
        else:
            if self.dirNext == "Left":  # check the direction first
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]-1][self.coordinateRel[1]] # levelObject placed left of this object

                # check the levelObject and allow movingObject to change its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.dirCurrent = "Left"
                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    pass
                

            elif self.dirNext == "Right":
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]+1][self.coordinateRel[1]] # levelObject placed right of this object

                # check the levelObject and allow movingObject to change its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.dirCurrent = "Right"
                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    pass


            elif self.dirNext == "Down":
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]+1] # levelObject placed down of this object

                # check the levelObject and allow movingObject to change its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.dirCurrent = "Down"
                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    pass


            elif self.dirNext == "Up":
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]-1] # levelObject placed up of this object

                # check the levelObject and allow movingObject to change its current direction
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.dirCurrent = "Up"
                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    pass
        
    
    def MoveCurrent(self, GameEngine):

        if self.dirCurrent == "Left":
            nextObject = GameEngine.levelObjects[self.coordinateRel[0]-1][self.coordinateRel[1]] # levelObject placed left of this object
            print("coordRel(X): ", self.coordinateRel[0], "coordRel(Y): ", self.coordinateRel[1], "Left Called")
            print("coordAbs(X): ", self.coordinateAbs[0], "coordAbs(Y): ", self.coordinateAbs[1], "Left Called")

            # check the levelObject and allow movingObject to move its current direction
            if nextObject.name in GameEngine.levelObjectNamesPassable:
                if self.coordinateAbs[0] == 0:  # at left edge, move to right edge
                    self.coordinateAbs[0] = 27*3 + 2
                    print("coordRel(X): ", self.coordinateRel[0], "coordRel(Y): ", self.coordinateRel[1], "Left edge")
                    print("coordAbs(X): ", self.coordinateAbs[0], "coordAbs(Y): ", self.coordinateAbs[1], "Left edge")

                else:
                    self.coordinateAbs[0] -= 1  # adjust current coordinate
                    print("coordRel(X): ", self.coordinateRel[0], "coordRel(Y): ", self.coordinateRel[1], "Left going")
                    print("coordAbs(X): ", self.coordinateAbs[0], "coordAbs(Y): ", self.coordinateAbs[1], "Left going")

                    if self.coordinateAbs[0] % 3 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[0] -= 1
                        print("coordRel(X): ", self.coordinateRel[0], "coordRel(Y): ", self.coordinateRel[1], "Left grid pt")
                        print("coordAbs(X): ", self.coordinateAbs[0], "coordAbs(Y): ", self.coordinateAbs[1], "Left grid pt")

            elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                self.dirCurrent = "Stop"
                print("coordRel(X): ", self.coordinateRel[0], "coordRel(Y): ", self.coordinateRel[1], "Left stop")
                print("coordAbs(X): ", self.coordinateAbs[0], "coordAbs(Y): ", self.coordinateAbs[1], "Left stop")


        elif self.dirCurrent == "Right":
            nextObject = GameEngine.levelObjects[self.coordinateRel[0]+1][self.coordinateRel[1]] # levelObject placed right of this object

            # check the levelObject and allow movingObject to move its current direction
            if nextObject.name in GameEngine.levelObjectNamesPassable:
                if self.coordinateAbs[0] == 27*3 + 2:  # at right edge, move to left edge
                    self.coordinateAbs[0] = 0
                    self.coordinateRel[0] = 0
                else:
                    self.coordinateAbs[0] += 1  # adjust current coordinate
                    if self.coordinateAbs[0] % 3 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[0] += 1

            elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                self.dirCurrent = "Stop"


        elif self.dirCurrent == "Down":
            nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]+1] # levelObject placed down of this object

            # check the levelObject and allow movingObject to move its current direction
            if nextObject.name in GameEngine.levelObjectNamesPassable:
                if self.coordinateAbs[1] == 0:  # at top edge, move to bottom edge
                    self.coordinateAbs[1] = 31*3 + 2
                else:
                    self.coordinateAbs[1] += 1  # adjust current coordinate
                    if self.coordinateAbs[1] % 3 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[1] += 1

            elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                self.dirCurrent = "Stop"


        elif self.dirCurrent == "Up":
            nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]-1] # levelObject placed up of this object

            # check the levelObject and allow movingObject to move its current direction
            if nextObject.name in GameEngine.levelObjectNamesPassable:
                if self.coordinateAbs[1] == 31*3 + 2:  # at bottom edge, move to top edge
                    self.coordinateAbs[1] = 0
                    self.coordinateRel[1] = 0
                else:
                    self.coordinateAbs[1] -= 1  # adjust current coordinate
                    if self.coordinateAbs[1] % 3 == 0: # check the object reaches a grid coordinate (coordinateRel)
                        self.coordinateRel[1] -= 1

            elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                self.dirCurrent = "Stop"


        elif self.dirCurrent == "Stop":
            pass


gameEngine = GameEngine()