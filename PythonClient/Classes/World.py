from PythonClient.ks.models import Constants, EDirection, ECell
from PythonClient.Classes import Agent


class World:
    def __init__(self, my_side, other_side, board, agents, scores, constants):
        self.my_side = my_side
        self.other_side = other_side
        self.board = board
        self.agents = agents
        self.scores = scores
        self.constants = constants

    def change_sides(self):
        temp_side = self.my_side
        self.my_side = self.other_side
        self.other_side = temp_side

    def get_d_cords(self, dir):
        if dir == EDirection.Left:
            return -1, 0
        if dir == EDirection.Right:
            return 1, 0
        if dir == EDirection.Up:
            return 0, -1
        if dir == EDirection.Down:
            return 0, 1

    def change_board(self, our_agent_side, enemy_agent_side, move):
        cur_agent = self.agents[our_agent_side]
        enemy_agent = self.agents[enemy_agent_side]
        if move is not None:
            cur_agent.direction = move
            if move in [EDirection.Up, EDirection.Down, EDirection.Left, EDirection.Right]:
                next_dir = self.get_d_cords(move)
                cur_agent.change_position(next_dir)
            else:
                cur_agent.activate_wall_breaker()
                cur_agent.change_position(cur_agent.direction)
        if self.board[cur_agent.position.y][cur_agent.position.x] == ECell.Empty:
            cur_agent.score += self.constants.wall_score_coefficient
            if cur_agent.color == "Blue":
                self.board[cur_agent.position.y][cur_agent.position.x] = ECell.BlueWall
            else:
                self.board[cur_agent.position.y][cur_agent.position.x] = ECell.YellowWall
        elif self.board[cur_agent.position.y][cur_agent.position.x] == ECell.AreaWall:
            cur_agent.health = 0
            cur_agent.score -= self.constants.area_wall_crash_score
        elif self.board[cur_agent.position.y][cur_agent.position.x] == ECell.BlueWall:
            if cur_agent.color == "Blue":
                cur_agent.score += self.constants.wall_score_coefficient - self.constants.my_wall_crash_score
                if not cur_agent.wall_breaker_is_on():
                    cur_agent.health -= 1
            else:
                if cur_agent.wall_breaker_is_on():
                    enemy_agent.score -= self.constants.wall_score_coefficient
                    cur_agent.score += self.constants.wall_score_coefficient
                else:
                    cur_agent.health -= 1
                    enemy_agent.score -= self.constants.wall_score_coefficient
                    cur_agent.score += self.constants.wall_score_coefficient
                    if cur_agent.health == 0:
                        cur_agent.score -= self.constants.enemy_wall_crash_score
                self.board[cur_agent.position.y][cur_agent.position.x] = ECell.YellowWall
        else:
            if cur_agent.color == "Yellow":
                cur_agent.score += self.constants.wall_score_coefficient - self.constants.my_wall_crash_score
                if not cur_agent.wall_breaker_is_on():
                    cur_agent.health -= 1
            else:
                if cur_agent.wall_breaker_is_on():
                    enemy_agent.score -= self.constants.wall_score_coefficient
                    cur_agent.score += self.constants.wall_score_coefficient
                else:
                    cur_agent.health -= 1
                    enemy_agent.score -= self.constants.wall_score_coefficient
                    cur_agent.score += self.constants.wall_score_coefficient
                    if cur_agent.health == 0:
                        cur_agent.score -= self.constants.enemy_wall_crash_score
                self.board[cur_agent.position.y][cur_agent.position.x] = ECell.BlueWall
        self.scores[our_agent_side] = cur_agent.score
        self.scores[enemy_agent_side] = enemy_agent.score
        cur_agent.tick_wall_breaker()
