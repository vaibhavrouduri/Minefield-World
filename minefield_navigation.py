#!/usr/bin/env python3
from Agent import *  # See the Agent.py file
from pysat.solvers import Glucose3
import random
# All your code can go here.

# You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.


def main():
    path = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    iterations = 0
    while len(path) > 12 and iterations < 25:
        ag = Agent()
        path.clear()
        knowledge_base = []
        kb = Glucose3()
        locations = []
        visited_locs = []
        path_literals = []
        actions = ['Right', 'Left', 'Up', 'Down']
        good_actions = ['Right', 'Up']
        bad_actions = ['Left', 'Down']
        unsafe = []
        cur_loc = 0

        def LocationToLiteral(loc):
            return locations.index(loc) + 1

        def FindAdjacentRooms(curLoc):
            cLoc = curLoc
            validMoves = [[0, 1], [0, -1], [-1, 0], [1, 0]]
            adjRooms = []
            for vM in validMoves:
                room = []
                valid = True
                for v, inc in zip(cLoc, vM):
                    z = v + inc
                    if z < 1 or z > 4:
                        valid = False
                        break
                    else:
                        room.append(z)
                if valid == True:
                    adjRooms.append(room)
            return adjRooms

        for i in range(1, 5):
            for j in range(1, 5):
                locations.append([i, j])

        while ag.FindCurrentLocation() != [4, 4]:

            cur_loc = LocationToLiteral(ag.FindCurrentLocation())
            path.append(ag.FindCurrentLocation())
            path_literals.append(cur_loc)

            if ag.PerceiveCurrentLocation() == '=0':
                knowledge_base.append([cur_loc])
                adjRooms = FindAdjacentRooms(locations[cur_loc - 1])
                for i in adjRooms:
                    knowledge_base.append([LocationToLiteral(i)])

            elif ag.PerceiveCurrentLocation() == '=1':
                adjRooms = FindAdjacentRooms(locations[cur_loc - 1])
                adjRooms_literals = []
                for i in adjRooms:
                    adjRooms_literals.append(LocationToLiteral(i))
                if len(adjRooms) == 2:
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1]])
                elif len(adjRooms) == 3:
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1], -adjRooms_literals[2]])
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[1]])
                    knowledge_base.append(
                        [adjRooms_literals[1], adjRooms_literals[2]])
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[2]])
                elif len(adjRooms) == 4:
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1], -adjRooms_literals[2], -adjRooms_literals[3]])
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[1]])
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[2]])
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[3]])
                    knowledge_base.append(
                        [adjRooms_literals[1], adjRooms_literals[2]])
                    knowledge_base.append(
                        [adjRooms_literals[1], adjRooms_literals[3]])
                    knowledge_base.append(
                        [adjRooms_literals[2], adjRooms_literals[3]])

            elif ag.PerceiveCurrentLocation() == '>1':
                adjRooms = FindAdjacentRooms(locations[cur_loc - 1])
                adjRooms_literals = []
                for i in adjRooms:
                    adjRooms_literals.append(LocationToLiteral(i))
                if len(adjRooms) == 2:
                    for i in adjRooms_literals:
                        knowledge_base.append([-i])
                elif len(adjRooms) == 3:
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[1], adjRooms_literals[2]])
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1]])
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[2]])
                    knowledge_base.append(
                        [-adjRooms_literals[1], -adjRooms_literals[2]])
                elif len(adjRooms) == 4:
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1], -adjRooms_literals[2]])
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1], -adjRooms_literals[3]])
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[2], -adjRooms_literals[3]])
                    knowledge_base.append(
                        [-adjRooms_literals[1], -adjRooms_literals[2], -adjRooms_literals[3]])

            for i in knowledge_base:
                kb.add_clause(i)

            if ag.PerceiveCurrentLocation() == None:
                break

            adjRooms = FindAdjacentRooms(locations[cur_loc - 1])
            safe = []
            for i in adjRooms:
                if kb.solve(assumptions=[-LocationToLiteral(i)]) == False:
                    safe.append(i)
            safe_literals = []
            for i in safe:
                safe_literals.append(LocationToLiteral(i))

            good_safe_literals = []
            bad_safe_literals = []
            for i in safe_literals:
                if i > cur_loc:
                    good_safe_literals.append(i)
                else:
                    bad_safe_literals.append(i)

            if len(good_safe_literals) == 0 and len(path) < 13:
                bad_safe_visited = []
                bad_safe_not_visited = []
                for j in bad_safe_literals:
                    if j in visited_locs:
                        bad_safe_visited.append(j)
                    else:
                        bad_safe_not_visited.append(j)

                if random.randint(1, 10) != 1 and len(bad_safe_not_visited) != 0:
                    i = random.choice(bad_safe_not_visited)
                elif random.randint(1, 10) == 1 and len(bad_safe_visited) != 0:
                    i = random.choice(bad_safe_visited)
                else:
                    i = random.choice(bad_safe_literals)
                if i == cur_loc - 4:
                    ag.TakeAction('Left')
                else:
                    ag.TakeAction('Down')
            elif len(good_safe_literals) > 0 and len(path) < 13:

                good_safe_visited = []
                good_safe_not_visited = []
                for j in good_safe_literals:
                    if j in visited_locs:
                        good_safe_visited.append(j)
                    else:
                        good_safe_not_visited.append(j)

                if random.randint(1, 10) != 1 and len(good_safe_not_visited) != 0:
                    i = random.choice(good_safe_not_visited)
                elif random.randint(1, 10) == 1 and len(good_safe_visited) != 0:
                    i = random.choice(good_safe_visited)
                else:
                    i = random.choice(good_safe_literals)
                if i == cur_loc + 4:
                    ag.TakeAction('Right')
                else:
                    ag.TakeAction('Up')
            
            else:
                i = random.choice(safe_literals)
                if i == cur_loc + 4:
                    ag.TakeAction('Right')
                elif i == cur_loc + 1:
                    ag.TakeAction('Up')
                elif i == cur_loc - 4:
                    ag.TakeAction('Left')
                elif i == cur_loc - 1:
                    ag.TakeAction('Down')


        iterations += 1
        if len(path) > 12:
            print('\nI am restarting the agent and building the knowledge base again as my path is unsatisfactory\n')

    if len(path) > 12:
        ag = Agent()

        knowledge_base = []
        kb = Glucose3()
        locations = []
        visited_locs = []
        path = []
        actions = ['Right', 'Left', 'Up', 'Down']
        good_actions = ['Right', 'Up']
        bad_actions = ['Left', 'Down']
        unsafe = []
        cur_loc = 0

        def LocationToLiteral(loc):
            return locations.index(loc) + 1

        def FindAdjacentRooms(curLoc):
            cLoc = curLoc
            validMoves = [[0, 1], [0, -1], [-1, 0], [1, 0]]
            adjRooms = []
            for vM in validMoves:
                room = []
                valid = True
                for v, inc in zip(cLoc, vM):
                    z = v + inc
                    if z < 1 or z > 4:
                        valid = False
                        break
                    else:
                        room.append(z)
                if valid == True:
                    adjRooms.append(room)
            return adjRooms

        for i in range(1, 5):
            for j in range(1, 5):
                locations.append([i, j])

        start_loc = ag.FindCurrentLocation()
        start_loc_literal = LocationToLiteral(start_loc)

        while ag.FindCurrentLocation() != [4, 4]:

            temp = ag.FindCurrentLocation()
            cur_loc = LocationToLiteral(temp)
            visited_locs.append(cur_loc)
            path.append(temp)

            if ag.PerceiveCurrentLocation() == '=0':
                knowledge_base.append([cur_loc])
                adjRooms = FindAdjacentRooms(locations[cur_loc - 1])
                for i in adjRooms:
                    knowledge_base.append([LocationToLiteral(i)])

            elif ag.PerceiveCurrentLocation() == '=1':
                adjRooms = FindAdjacentRooms(locations[cur_loc - 1])
                adjRooms_literals = []
                for i in adjRooms:
                    adjRooms_literals.append(LocationToLiteral(i))
                if len(adjRooms) == 2:
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1]])
                elif len(adjRooms) == 3:
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1], -adjRooms_literals[2]])
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[1]])
                    knowledge_base.append(
                        [adjRooms_literals[1], adjRooms_literals[2]])
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[2]])
                elif len(adjRooms) == 4:
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1], -adjRooms_literals[2], -adjRooms_literals[3]])
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[1]])
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[2]])
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[3]])
                    knowledge_base.append(
                        [adjRooms_literals[1], adjRooms_literals[2]])
                    knowledge_base.append(
                        [adjRooms_literals[1], adjRooms_literals[3]])
                    knowledge_base.append(
                        [adjRooms_literals[2], adjRooms_literals[3]])

            elif ag.PerceiveCurrentLocation() == '>1':
                adjRooms = FindAdjacentRooms(locations[cur_loc - 1])
                adjRooms_literals = []
                for i in adjRooms:
                    adjRooms_literals.append(LocationToLiteral(i))
                if len(adjRooms) == 2:
                    for i in adjRooms_literals:
                        knowledge_base.append([-i])
                elif len(adjRooms) == 3:
                    knowledge_base.append(
                        [adjRooms_literals[0], adjRooms_literals[1], adjRooms_literals[2]])
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1]])
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[2]])
                    knowledge_base.append(
                        [-adjRooms_literals[1], -adjRooms_literals[2]])
                elif len(adjRooms) == 4:
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1], -adjRooms_literals[2]])
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[1], -adjRooms_literals[3]])
                    knowledge_base.append(
                        [-adjRooms_literals[0], -adjRooms_literals[2], -adjRooms_literals[3]])
                    knowledge_base.append(
                        [-adjRooms_literals[1], -adjRooms_literals[2], -adjRooms_literals[3]])

            for i in knowledge_base:
                kb.add_clause(i)

            if ag.PerceiveCurrentLocation() == None:
                break

            adjRooms = FindAdjacentRooms(locations[cur_loc - 1])
            safe = []
            for i in adjRooms:
                if kb.solve(assumptions=[-LocationToLiteral(i)]) == False:
                    safe.append(i)
            safe_literals = []
            for i in safe:
                safe_literals.append(LocationToLiteral(i))

            good_safe_literals = []
            bad_safe_literals = []
            for i in safe_literals:
                if i > cur_loc:
                    good_safe_literals.append(i)
                else:
                    bad_safe_literals.append(i)

            if len(good_safe_literals) == 0 and len(path) < 16:
                bad_safe_visited = []
                bad_safe_not_visited = []
                for j in bad_safe_literals:
                    if j in visited_locs:
                        bad_safe_visited.append(j)
                    else:
                        bad_safe_not_visited.append(j)

                if random.randint(1, 10) != 1 and len(bad_safe_not_visited) != 0:
                    i = random.choice(bad_safe_not_visited)
                elif random.randint(1, 10) == 1 and len(bad_safe_visited) != 0:
                    i = random.choice(bad_safe_visited)
                else:
                    i = random.choice(bad_safe_literals)
                if i == cur_loc - 4:
                    ag.TakeAction('Left')
                else:
                    ag.TakeAction('Down')
            elif len(good_safe_literals) > 0 and len(path) < 16:

                good_safe_visited = []
                good_safe_not_visited = []
                for j in good_safe_literals:
                    if j in visited_locs:
                        good_safe_visited.append(j)
                    else:
                        good_safe_not_visited.append(j)

                if random.randint(1, 10) != 1 and len(good_safe_not_visited) != 0:
                    i = random.choice(good_safe_not_visited)
                elif random.randint(1, 10) == 1 and len(good_safe_visited) != 0:
                    i = random.choice(good_safe_visited)
                else:
                    i = random.choice(good_safe_literals)
                if i == cur_loc + 4:
                    ag.TakeAction('Right')
                else:
                    ag.TakeAction('Up')
            elif len(path) < 20:
                i = random.choice(safe_literals)
                if i == cur_loc + 4:
                    ag.TakeAction('Right')
                elif i == cur_loc + 1:
                    ag.TakeAction('Up')
                elif i == cur_loc - 4:
                    ag.TakeAction('Left')
                elif i == cur_loc - 1:
                    ag.TakeAction('Down')        

            elif len(path) < 25:
                i = random.choice(safe_literals)
                if i == cur_loc + 4:
                    ag.TakeAction('Right')
                elif i == cur_loc + 1:
                    ag.TakeAction('Up')
                elif i == cur_loc - 4:
                    ag.TakeAction('Left')
                elif i == cur_loc - 1:
                    ag.TakeAction('Down') 
            
            else:
                i = random.choice(safe_literals)
                if i == cur_loc + 4:
                    ag.TakeAction('Right')
                elif i == cur_loc + 1:
                    ag.TakeAction('Up')
                elif i == cur_loc - 4:
                    ag.TakeAction('Left')
                elif i == cur_loc - 1:
                    ag.TakeAction('Down')       


    path.append([4, 4])
    for i in range(len(path)-1):
        print(path[i], end="")
        print("=>", end="")
    print(path[len(path)-1])

if __name__ == '__main__':
    main()
