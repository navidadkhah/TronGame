[ECommandDirection]
_def = enum <byte>
    {
        Up,
        Right,
        Down,
        Left
    }


[ChangeDirection]
_def = class
direction = ECommandDirection


[ActivateWallBreaker]
_def = class
