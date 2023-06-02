[ECell]
_def = enum <byte>
    {
        Empty,
        AreaWall,
        BlueWall,
        YellowWall
    }


[EDirection]
_def = enum <byte>
    {
        Up,
        Right,
        Down,
        Left
    }


[Constants]
_def = class
max_cycles = int
init_health = int
wall_breaker_cooldown = int
wall_breaker_duration = int
wall_score_coefficient = int
area_wall_crash_score = int
my_wall_crash_score = int
enemy_wall_crash_score = int


[Position]
_def = class
x = int
y = int


[Agent]
_def = class
health = int
position = Position
direction = EDirection
wall_breaker_cooldown = int
wall_breaker_rem_time = int


[World]
_def = class
board = list<list<ECell>>
agents = map<string, Agent>
scores = map<string, int>
constants = Constants
