# -*- coding: utf-8 -*-

# python imports
import random
import copy
from ks.models import *

# chillin imports
from chillin_client import RealtimeAI

# project imports
from ks.models import ECell, EDirection, Position
from ks.commands import ChangeDirection, ActivateWallBreaker

class AI(RealtimeAI):

    def __init__(self, world):
        super(AI, self).__init__(world)

    def initialize(self):
        print('initialize')

    def decide(self):
        print('decide')
        self.client1()
        # self.send_command(ChangeDirection(random.choice(list(EDirection))))
        # if self.world.agents[self.my_side].wall_breaker_cooldown == 0:
        #     self.send_command(ActivateWallBreaker())

    MN = -10000, MX = +10000

    def get_next_nodes(self, cur_ai, neighbors, move_list, depth):
        best_answer = cur_ai.MN, []

        for move in neighbors:
            new_ai = copy.deepcopy(cur_ai)

            # Change Direction
            ChangeDirection(move)
            if new_ai.my_side == "Yellow":
                new_ai.my_side = "Blue"
                new_ai.other_side = "Yellow"
            else:
                new_ai.my_side = "Yellow"
                new_ai.other_side = "Blue"
            new_move_list = copy.deepcopy(move_list)
            ret = self.minimax(self, new_ai, depth + 1, new_move_list)
            if ret[0] > best_answer[0]:
                best_answer = ret
        return best_answer

    def evaluate_score(self, world):

        if self.color == "Blue":
            my_side = ECell.BlueWall
            other_side = ECell.YellowWall
            other_side_color = "Yellow"
            my_color = "Blue"

        else:
            my_side = ECell.YellowWall
            other_side = ECell.BlueWall
            other_side_color = "Blue"
            my_color = "Yellow"
        if self.act is None:
            if self.first_color == "Yellow":
                return (world.agents[self.my_color].health * 200 + world.scores[self.my_color]) - \
                       (world.agents["Blue"].health * 200 +
                        world.scores["Blue"]), world
            else:
                return (world.agents[self.my_color].health * 200 + world.scores[self.my_color]) - \
                       (world.agents["Yellow"].health * 200 +
                        world.scores["Yellow"]), world

        world.board[world.agents[other_side_color].position.y][world.agents[other_side_color].position.x] = my_side
        world.scores[other_side_color] += world.constants.wall_score_coefficient

        if self.act == EDirection.Right:

            self.change(my_side, other_side, other_side_color, world, 1, 0, EDirection.Right)
        elif self.act == EDirection.Left:
            self.change(my_side, other_side, other_side_color, world, -1, 0, EDirection.Left)
        elif self.act == EDirection.Up:
            self.change(my_side, other_side, other_side_color, world, 0, -1, EDirection.Up)
        elif self.act == EDirection.Down:
            self.change(my_side, other_side, other_side_color, world, 0, 1, EDirection.Down)
        else:
            direction = world.agents[other_side_color].direction
            world.agents[other_side_color].wall_breaker_rem_time = world.constants.wall_breaker_duration
            if direction == EDirection.Right:
                self.change(my_side, other_side, other_side_color, world, 1, 0, direction)
            elif direction == EDirection.Left:
                self.change(my_side, other_side, other_side_color, world, -1, 0, direction)
            elif direction == EDirection.Up:
                self.change(my_side, other_side, other_side_color, world, 0, -1, direction)
            else:
                self.change(my_side, other_side, other_side_color, world, 0, 1, direction)

        if world.agents[other_side_color].health == -1:
            self.isterminal = True
        # return (world.agents[other_side_color].health * 20 + world.scores[other_side_color]) - \
        #        (world.agents[my_color].health * 20 +
        #         world.scores[my_color]), world

        if self.first_color == "Yellow":
            return (world.agents[self.first_color].health * 200 + world.scores[self.first_color]) - \
                   (world.agents["Blue"].health * 200 +
                    world.scores["Blue"]), world
        else:
            return (world.agents[self.first_color].health * 200 + world.scores[self.first_color]) - \
                   (world.agents["Yellow"].health * 200 +
                    world.scores["Yellow"]), world

    def change_direction(self, cur_ai, direction):


    def activate_wall_breaker(self, cur_ai):
        cur_ai.world.agents[self.my_side].wall_breaker_rem_time = Constants.wall_breaker_duration

    def minimax(self, cur_ai, depth, move_list):
        if depth == 6:
            return cur_ai.world.scores[cur_ai.my_side] - cur_ai.world.scores[cur_ai.other_side], move_list[:-1]

        my_team = cur_ai.my_side
        empty_neighbors = cur_ai._get_our_agent_empty_neighbors()
        blue_walls = cur_ai._get_our_agent_blue_wall_neighbors()
        yellow_walls = cur_ai._get_our_agent_yellow_wall_neighbors()
        area_walls = cur_ai._get_our_agent_Area_wall_neighbors()

        best_answer = cur_ai.MN, []

        if cur_ai.world.agents[cur_ai.my_side].wall_breaker_rem_time > 1:
            # wall breaker is on
            cur_ai.world.agents[cur_ai.my_side].wall_breaker_rem_time -= 1

            if my_team == "Yellow":
                if blue_walls:
                    best_answer = self.get_next_nodes(self, cur_ai, blue_walls, move_list, depth)
                elif empty_neighbors:
                    best_answer = self.get_next_nodes(self, cur_ai, empty_neighbors, move_list, depth)
                elif yellow_walls:
                    best_answer = self.get_next_nodes(self, cur_ai, yellow_walls, move_list, depth)
                else:
                    self.send_command(ChangeDirection(random.choice(list(EDirection))))
            else:
                if yellow_walls:
                    best_answer = self.get_next_nodes(self, cur_ai, yellow_walls, move_list, depth)
                elif empty_neighbors:
                    best_answer = self.get_next_nodes(self, cur_ai, empty_neighbors, move_list, depth)
                elif blue_walls:
                    best_answer = self.get_next_nodes(self, cur_ai, blue_walls, move_list, depth)
                else:
                    self.send_command(ChangeDirection(random.choice(list(EDirection))))

        else:
            # wall breaker is off
            cur_ai.world.agents[cur_ai.my_side].wall_breaker_cooldown -= 1
            if empty_neighbors:
                best_answer = self.get_next_nodes(self, cur_ai, empty_neighbors, move_list, depth)
            else:
                if cur_ai.world.agents[my_team].wall_breaker_cooldown == 0 and not (
                        cur_ai.world.agents[my_team].direction in area_walls):
                    self.activate_wall_breaker(self, cur_ai)
                else:
                    if my_team == "Yellow":
                        if blue_walls:
                            self.send_command(ChangeDirection(random.choice(blue_walls)))
                        elif yellow_walls:
                            self.send_command(ChangeDirection(random.choice(yellow_walls)))
                        else:
                            self.send_command(ChangeDirection(random.choice(list(EDirection))))
                    else:
                        if yellow_walls:
                            self.send_command(ChangeDirection(random.choice(yellow_walls)))
                        elif blue_walls:
                            self.send_command(ChangeDirection(random.choice(blue_walls)))
                        else:
                            self.send_command(ChangeDirection(random.choice(list(EDirection))))




    def client1(self):
        my_team = self.my_side
        empty_neighbors = self._get_our_agent_empty_neighbors()
        blue_walls = self._get_our_agent_blue_wall_neighbors()
        yellow_walls = self._get_our_agent_yellow_wall_neighbors()
        area_walls = self._get_our_agent_Area_wall_neighbors()
        # print(f"empty_neighbors : {empty_neighbors}")
        # print(f"blue_walls : {blue_walls}")
        # print(f"yellow_walls : {yellow_walls}")

        new_AI = copy.deepcopy(self)
        next_move = self.minimax(self, new_AI, 0, "Max")[1]

        if self.world.agents[self.my_side].wall_breaker_rem_time > 1:
            # wall breaker is on
            if my_team == "Yellow":
                if blue_walls:
                    self.send_command(ChangeDirection(random.choice(blue_walls)))
                elif empty_neighbors:
                    self.send_command(ChangeDirection(random.choice(empty_neighbors)))
                elif yellow_walls:
                    self.send_command(ChangeDirection(random.choice(yellow_walls)))
                else:
                    self.send_command(ChangeDirection(random.choice(list(EDirection))))
            else:
                if yellow_walls:
                    self.send_command(ChangeDirection(random.choice(yellow_walls)))
                elif empty_neighbors:
                    self.send_command(ChangeDirection(random.choice(empty_neighbors)))
                elif blue_walls:
                    self.send_command(ChangeDirection(random.choice(blue_walls)))
                else:
                    self.send_command(ChangeDirection(random.choice(list(EDirection))))

        else:
            # wall breaker is off
            if empty_neighbors:
                self.send_command(ChangeDirection(random.choice(empty_neighbors)))
            else:

                if self.world.agents[my_team].wall_breaker_cooldown == 0 and not (
                        self.world.agents[my_team].direction in area_walls):
                    self.send_command(ActivateWallBreaker())
                else:
                    if my_team == "Yellow":
                        if blue_walls:
                            self.send_command(ChangeDirection(random.choice(blue_walls)))
                        elif yellow_walls:
                            self.send_command(ChangeDirection(random.choice(yellow_walls)))
                        else:
                            self.send_command(ChangeDirection(random.choice(list(EDirection))))
                    else:
                        if yellow_walls:
                            self.send_command(ChangeDirection(random.choice(yellow_walls)))
                        elif blue_walls:
                            self.send_command(ChangeDirection(random.choice(blue_walls)))
                        else:
                            self.send_command(ChangeDirection(random.choice(list(EDirection))))

    def _get_our_agent_empty_neighbors(self):
        empty_neighbors = []

        our_position = self._get_our_agent_position()

        their_position = self._get_their_agent_position()

        if our_position.x + 1 < len(self.world.board):
            if self.world.board[our_position.y][our_position.x + 1] == ECell.Empty and \
                    not (our_position.x + 1 == their_position.x and our_position.y == their_position.y):
                empty_neighbors.append(EDirection.Right)
        if our_position.x - 1 >= 0:
            if self.world.board[our_position.y][our_position.x - 1] == ECell.Empty and \
                    not (our_position.x - 1 == their_position.x and our_position.y == their_position.y):
                empty_neighbors.append(EDirection.Left)
        if our_position.y + 1 < len(self.world.board):
            if self.world.board[our_position.y + 1][our_position.x] == ECell.Empty and \
                    not (our_position.x == their_position.x and our_position.y + 1 == their_position.y):
                empty_neighbors.append(EDirection.Down)
        if our_position.y - 1 >= 0:
            if self.world.board[our_position.y - 1][our_position.x] == ECell.Empty and \
                    not (our_position.x == their_position.x and our_position.y - 1 == their_position.y):
                empty_neighbors.append(EDirection.Up)
        return empty_neighbors

    def _get_our_agent_blue_wall_neighbors(self):
        blue_walls = []
        our_position = self._get_our_agent_position()
        their_position = self._get_their_agent_position()
        if our_position.x + 1 < len(self.world.board):
            if self.world.board[our_position.y][our_position.x + 1] == ECell.BlueWall and \
                    not (our_position.x + 1 == their_position.x and our_position.y == their_position.y):
                blue_walls.append(EDirection.Right)
        if our_position.x - 1 >= 0:
            if self.world.board[our_position.y][our_position.x - 1] == ECell.BlueWall and \
                    not (our_position.x - 1 == their_position.x and our_position.y == their_position.y):
                blue_walls.append(EDirection.Left)
        if our_position.y + 1 < len(self.world.board):
            if self.world.board[our_position.y + 1][our_position.x] == ECell.BlueWall and \
                    not (our_position.x == their_position.x and our_position.y + 1 == their_position.y):
                blue_walls.append(EDirection.Down)
        if our_position.y - 1 >= 0:
            if self.world.board[our_position.y - 1][our_position.x] == ECell.BlueWall and \
                    not (our_position.x == their_position.x and our_position.y - 1 == their_position.y):
                blue_walls.append(EDirection.Up)
        return blue_walls

    def _get_our_agent_yellow_wall_neighbors(self):
        yellow_walls = []
        our_position = self._get_our_agent_position()
        their_position = self._get_their_agent_position()
        if our_position.x + 1 < len(self.world.board[0]):
            if self.world.board[our_position.y][our_position.x + 1] == ECell.YellowWall and \
                    not (our_position.x + 1 == their_position.x and our_position.y == their_position.y):
                yellow_walls.append(EDirection.Right)
        if our_position.x - 1 >= 0:
            if self.world.board[our_position.y][our_position.x - 1] == ECell.YellowWall and \
                    not (our_position.x - 1 == their_position.x and our_position.y == their_position.y):
                yellow_walls.append(EDirection.Left)
        if our_position.y + 1 < len(self.world.board):
            if self.world.board[our_position.y + 1][our_position.x] == ECell.YellowWall and \
                    not (our_position.x == their_position.x and our_position.y + 1 == their_position.y):
                yellow_walls.append(EDirection.Down)
        if our_position.y - 1 >= 0:
            if self.world.board[our_position.y - 1][our_position.x] == ECell.YellowWall and \
                    not (our_position.x == their_position.x and our_position.y - 1 == their_position.y):
                yellow_walls.append(EDirection.Up)
        return yellow_walls

    def _get_our_agent_Area_wall_neighbors(self):
        area_walls = []
        our_position = self._get_our_agent_position()
        their_position = self._get_their_agent_position()
        if our_position.x + 1 < len(self.world.board[0]):
            if self.world.board[our_position.y][our_position.x + 1] == ECell.AreaWall and \
                    not (our_position.x + 1 == their_position.x and our_position.y == their_position.y):
                area_walls.append(EDirection.Right)
        if our_position.x - 1 >= 0:
            if self.world.board[our_position.y][our_position.x - 1] == ECell.AreaWall and \
                    not (our_position.x - 1 == their_position.x and our_position.y == their_position.y):
                area_walls.append(EDirection.Left)
        if our_position.y + 1 < len(self.world.board):
            if self.world.board[our_position.y + 1][our_position.x] == ECell.AreaWall and \
                    not (our_position.x == their_position.x and our_position.y + 1 == their_position.y):
                area_walls.append(EDirection.Down)
        if our_position.y - 1 >= 0:
            if self.world.board[our_position.y - 1][our_position.x] == ECell.AreaWall and \
                    not (our_position.x == their_position.x and our_position.y - 1 == their_position.y):
                area_walls.append(EDirection.Up)
        return area_walls

    def _get_our_agent_position(self):
        return self.world.agents[self.my_side].position

    def _get_their_agent_position(self):
        return self.world.agents[self.other_side].position