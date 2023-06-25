from PythonClient.ks.models import Constants


class Agent:
    def __init__(self, health, position, direction, wall_breaker_cooldown, wall_breaker_rem_time, score, color):
        self.health = health
        self.position = position
        self.direction = direction
        self.wall_breaker_cooldown = wall_breaker_cooldown
        self.wall_breaker_rem_time = wall_breaker_rem_time
        self.score = score
        self.color = color

    def decrease_health(self):
        self.health -= 1

    def change_position(self, d_x, d_y):
        self.position.x += d_x
        self.position.y += d_y

    def activate_wall_breaker(self):
        if not self.wall_breaker_is_on() and self.wall_breaker_cooldown == 0:
            self.wall_breaker_rem_time = Constants.wall_breaker_duration

    def change_direction(self, new_direction):
        self.direction = new_direction

    def tick_wall_breaker(self):
        if self.wall_breaker_rem_time > 0:
            self.wall_breaker_rem_time -= 1

        if self.wall_breaker_cooldown > 0:
            self.wall_breaker_cooldown -= 1

    def change_score(self, new_score):
        self.score = new_score

    def wall_breaker_is_on(self):
        if self.wall_breaker_rem_time != 0:
            return True
        return False