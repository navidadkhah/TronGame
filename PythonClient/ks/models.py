# -*- coding: utf-8 -*-

# python imports
import sys
import struct
from enum import Enum

PY3 = sys.version_info > (3,)


class ECell(Enum):
	Empty = 0
	AreaWall = 1
	BlueWall = 2
	YellowWall = 3


class EDirection(Enum):
	Up = 0
	Right = 1
	Down = 2
	Left = 3


class Constants(object):

	@staticmethod
	def name():
		return 'Constants'


	def __init__(self, max_cycles=None, init_health=None, wall_breaker_cooldown=None, wall_breaker_duration=None, wall_score_coefficient=None, area_wall_crash_score=None, my_wall_crash_score=None, enemy_wall_crash_score=None):
		self.initialize(max_cycles, init_health, wall_breaker_cooldown, wall_breaker_duration, wall_score_coefficient, area_wall_crash_score, my_wall_crash_score, enemy_wall_crash_score)
	

	def initialize(self, max_cycles=None, init_health=None, wall_breaker_cooldown=None, wall_breaker_duration=None, wall_score_coefficient=None, area_wall_crash_score=None, my_wall_crash_score=None, enemy_wall_crash_score=None):
		self.max_cycles = max_cycles
		self.init_health = init_health
		self.wall_breaker_cooldown = wall_breaker_cooldown
		self.wall_breaker_duration = wall_breaker_duration
		self.wall_score_coefficient = wall_score_coefficient
		self.area_wall_crash_score = area_wall_crash_score
		self.my_wall_crash_score = my_wall_crash_score
		self.enemy_wall_crash_score = enemy_wall_crash_score
	

	def serialize(self):
		s = b''
		
		# serialize self.max_cycles
		s += b'\x00' if self.max_cycles is None else b'\x01'
		if self.max_cycles is not None:
			s += struct.pack('i', self.max_cycles)
		
		# serialize self.init_health
		s += b'\x00' if self.init_health is None else b'\x01'
		if self.init_health is not None:
			s += struct.pack('i', self.init_health)
		
		# serialize self.wall_breaker_cooldown
		s += b'\x00' if self.wall_breaker_cooldown is None else b'\x01'
		if self.wall_breaker_cooldown is not None:
			s += struct.pack('i', self.wall_breaker_cooldown)
		
		# serialize self.wall_breaker_duration
		s += b'\x00' if self.wall_breaker_duration is None else b'\x01'
		if self.wall_breaker_duration is not None:
			s += struct.pack('i', self.wall_breaker_duration)
		
		# serialize self.wall_score_coefficient
		s += b'\x00' if self.wall_score_coefficient is None else b'\x01'
		if self.wall_score_coefficient is not None:
			s += struct.pack('i', self.wall_score_coefficient)
		
		# serialize self.area_wall_crash_score
		s += b'\x00' if self.area_wall_crash_score is None else b'\x01'
		if self.area_wall_crash_score is not None:
			s += struct.pack('i', self.area_wall_crash_score)
		
		# serialize self.my_wall_crash_score
		s += b'\x00' if self.my_wall_crash_score is None else b'\x01'
		if self.my_wall_crash_score is not None:
			s += struct.pack('i', self.my_wall_crash_score)
		
		# serialize self.enemy_wall_crash_score
		s += b'\x00' if self.enemy_wall_crash_score is None else b'\x01'
		if self.enemy_wall_crash_score is not None:
			s += struct.pack('i', self.enemy_wall_crash_score)
		
		return s
	

	def deserialize(self, s, offset=0):
		# deserialize self.max_cycles
		tmp0 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp0:
			self.max_cycles = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.max_cycles = None
		
		# deserialize self.init_health
		tmp1 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp1:
			self.init_health = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.init_health = None
		
		# deserialize self.wall_breaker_cooldown
		tmp2 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp2:
			self.wall_breaker_cooldown = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.wall_breaker_cooldown = None
		
		# deserialize self.wall_breaker_duration
		tmp3 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp3:
			self.wall_breaker_duration = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.wall_breaker_duration = None
		
		# deserialize self.wall_score_coefficient
		tmp4 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp4:
			self.wall_score_coefficient = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.wall_score_coefficient = None
		
		# deserialize self.area_wall_crash_score
		tmp5 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp5:
			self.area_wall_crash_score = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.area_wall_crash_score = None
		
		# deserialize self.my_wall_crash_score
		tmp6 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp6:
			self.my_wall_crash_score = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.my_wall_crash_score = None
		
		# deserialize self.enemy_wall_crash_score
		tmp7 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp7:
			self.enemy_wall_crash_score = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.enemy_wall_crash_score = None
		
		return offset


class Position(object):

	@staticmethod
	def name():
		return 'Position'


	def __init__(self, x=None, y=None):
		self.initialize(x, y)
	

	def initialize(self, x=None, y=None):
		self.x = x
		self.y = y
	

	def serialize(self):
		s = b''
		
		# serialize self.x
		s += b'\x00' if self.x is None else b'\x01'
		if self.x is not None:
			s += struct.pack('i', self.x)
		
		# serialize self.y
		s += b'\x00' if self.y is None else b'\x01'
		if self.y is not None:
			s += struct.pack('i', self.y)
		
		return s
	

	def deserialize(self, s, offset=0):
		# deserialize self.x
		tmp8 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp8:
			self.x = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.x = None
		
		# deserialize self.y
		tmp9 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp9:
			self.y = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.y = None
		
		return offset


class Agent(object):

	@staticmethod
	def name():
		return 'Agent'


	def __init__(self, health=None, position=None, direction=None, wall_breaker_cooldown=None, wall_breaker_rem_time=None):
		self.initialize(health, position, direction, wall_breaker_cooldown, wall_breaker_rem_time)
	

	def initialize(self, health=None, position=None, direction=None, wall_breaker_cooldown=None, wall_breaker_rem_time=None):
		self.health = health
		self.position = position
		self.direction = direction
		self.wall_breaker_cooldown = wall_breaker_cooldown
		self.wall_breaker_rem_time = wall_breaker_rem_time
	

	def serialize(self):
		s = b''
		
		# serialize self.health
		s += b'\x00' if self.health is None else b'\x01'
		if self.health is not None:
			s += struct.pack('i', self.health)
		
		# serialize self.position
		s += b'\x00' if self.position is None else b'\x01'
		if self.position is not None:
			s += self.position.serialize()
		
		# serialize self.direction
		s += b'\x00' if self.direction is None else b'\x01'
		if self.direction is not None:
			s += struct.pack('b', self.direction.value)
		
		# serialize self.wall_breaker_cooldown
		s += b'\x00' if self.wall_breaker_cooldown is None else b'\x01'
		if self.wall_breaker_cooldown is not None:
			s += struct.pack('i', self.wall_breaker_cooldown)
		
		# serialize self.wall_breaker_rem_time
		s += b'\x00' if self.wall_breaker_rem_time is None else b'\x01'
		if self.wall_breaker_rem_time is not None:
			s += struct.pack('i', self.wall_breaker_rem_time)
		
		return s
	

	def deserialize(self, s, offset=0):
		# deserialize self.health
		tmp10 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp10:
			self.health = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.health = None
		
		# deserialize self.position
		tmp11 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp11:
			self.position = Position()
			offset = self.position.deserialize(s, offset)
		else:
			self.position = None
		
		# deserialize self.direction
		tmp12 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp12:
			tmp13 = struct.unpack('b', s[offset:offset + 1])[0]
			offset += 1
			self.direction = EDirection(tmp13)
		else:
			self.direction = None
		
		# deserialize self.wall_breaker_cooldown
		tmp14 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp14:
			self.wall_breaker_cooldown = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.wall_breaker_cooldown = None
		
		# deserialize self.wall_breaker_rem_time
		tmp15 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp15:
			self.wall_breaker_rem_time = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
		else:
			self.wall_breaker_rem_time = None
		
		return offset


class World(object):

	@staticmethod
	def name():
		return 'World'


	def __init__(self, board=None, agents=None, scores=None, constants=None):
		self.initialize(board, agents, scores, constants)
	

	def initialize(self, board=None, agents=None, scores=None, constants=None):
		self.board = board
		self.agents = agents
		self.scores = scores
		self.constants = constants
	

	def serialize(self):
		s = b''
		
		# serialize self.board
		s += b'\x00' if self.board is None else b'\x01'
		if self.board is not None:
			tmp16 = b''
			tmp16 += struct.pack('I', len(self.board))
			while len(tmp16) and tmp16[-1] == b'\x00'[0]:
				tmp16 = tmp16[:-1]
			s += struct.pack('B', len(tmp16))
			s += tmp16
			
			for tmp17 in self.board:
				s += b'\x00' if tmp17 is None else b'\x01'
				if tmp17 is not None:
					tmp18 = b''
					tmp18 += struct.pack('I', len(tmp17))
					while len(tmp18) and tmp18[-1] == b'\x00'[0]:
						tmp18 = tmp18[:-1]
					s += struct.pack('B', len(tmp18))
					s += tmp18
					
					for tmp19 in tmp17:
						s += b'\x00' if tmp19 is None else b'\x01'
						if tmp19 is not None:
							s += struct.pack('b', tmp19.value)
		
		# serialize self.agents
		s += b'\x00' if self.agents is None else b'\x01'
		if self.agents is not None:
			tmp20 = b''
			tmp20 += struct.pack('I', len(self.agents))
			while len(tmp20) and tmp20[-1] == b'\x00'[0]:
				tmp20 = tmp20[:-1]
			s += struct.pack('B', len(tmp20))
			s += tmp20
			
			for tmp21 in self.agents:
				s += b'\x00' if tmp21 is None else b'\x01'
				if tmp21 is not None:
					tmp22 = b''
					tmp22 += struct.pack('I', len(tmp21))
					while len(tmp22) and tmp22[-1] == b'\x00'[0]:
						tmp22 = tmp22[:-1]
					s += struct.pack('B', len(tmp22))
					s += tmp22
					
					s += tmp21.encode('ISO-8859-1') if PY3 else tmp21
				s += b'\x00' if self.agents[tmp21] is None else b'\x01'
				if self.agents[tmp21] is not None:
					s += self.agents[tmp21].serialize()
		
		# serialize self.scores
		s += b'\x00' if self.scores is None else b'\x01'
		if self.scores is not None:
			tmp23 = b''
			tmp23 += struct.pack('I', len(self.scores))
			while len(tmp23) and tmp23[-1] == b'\x00'[0]:
				tmp23 = tmp23[:-1]
			s += struct.pack('B', len(tmp23))
			s += tmp23
			
			for tmp24 in self.scores:
				s += b'\x00' if tmp24 is None else b'\x01'
				if tmp24 is not None:
					tmp25 = b''
					tmp25 += struct.pack('I', len(tmp24))
					while len(tmp25) and tmp25[-1] == b'\x00'[0]:
						tmp25 = tmp25[:-1]
					s += struct.pack('B', len(tmp25))
					s += tmp25
					
					s += tmp24.encode('ISO-8859-1') if PY3 else tmp24
				s += b'\x00' if self.scores[tmp24] is None else b'\x01'
				if self.scores[tmp24] is not None:
					s += struct.pack('i', self.scores[tmp24])
		
		# serialize self.constants
		s += b'\x00' if self.constants is None else b'\x01'
		if self.constants is not None:
			s += self.constants.serialize()
		
		return s
	

	def deserialize(self, s, offset=0):
		# deserialize self.board
		tmp26 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp26:
			tmp27 = struct.unpack('B', s[offset:offset + 1])[0]
			offset += 1
			tmp28 = s[offset:offset + tmp27]
			offset += tmp27
			tmp28 += b'\x00' * (4 - tmp27)
			tmp29 = struct.unpack('I', tmp28)[0]
			
			self.board = []
			for tmp30 in range(tmp29):
				tmp32 = struct.unpack('B', s[offset:offset + 1])[0]
				offset += 1
				if tmp32:
					tmp33 = struct.unpack('B', s[offset:offset + 1])[0]
					offset += 1
					tmp34 = s[offset:offset + tmp33]
					offset += tmp33
					tmp34 += b'\x00' * (4 - tmp33)
					tmp35 = struct.unpack('I', tmp34)[0]
					
					tmp31 = []
					for tmp36 in range(tmp35):
						tmp38 = struct.unpack('B', s[offset:offset + 1])[0]
						offset += 1
						if tmp38:
							tmp39 = struct.unpack('b', s[offset:offset + 1])[0]
							offset += 1
							tmp37 = ECell(tmp39)
						else:
							tmp37 = None
						tmp31.append(tmp37)
				else:
					tmp31 = None
				self.board.append(tmp31)
		else:
			self.board = None
		
		# deserialize self.agents
		tmp40 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp40:
			tmp41 = struct.unpack('B', s[offset:offset + 1])[0]
			offset += 1
			tmp42 = s[offset:offset + tmp41]
			offset += tmp41
			tmp42 += b'\x00' * (4 - tmp41)
			tmp43 = struct.unpack('I', tmp42)[0]
			
			self.agents = {}
			for tmp44 in range(tmp43):
				tmp47 = struct.unpack('B', s[offset:offset + 1])[0]
				offset += 1
				if tmp47:
					tmp48 = struct.unpack('B', s[offset:offset + 1])[0]
					offset += 1
					tmp49 = s[offset:offset + tmp48]
					offset += tmp48
					tmp49 += b'\x00' * (4 - tmp48)
					tmp50 = struct.unpack('I', tmp49)[0]
					
					tmp45 = s[offset:offset + tmp50].decode('ISO-8859-1') if PY3 else s[offset:offset + tmp50]
					offset += tmp50
				else:
					tmp45 = None
				tmp51 = struct.unpack('B', s[offset:offset + 1])[0]
				offset += 1
				if tmp51:
					tmp46 = Agent()
					offset = tmp46.deserialize(s, offset)
				else:
					tmp46 = None
				self.agents[tmp45] = tmp46
		else:
			self.agents = None
		
		# deserialize self.scores
		tmp52 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp52:
			tmp53 = struct.unpack('B', s[offset:offset + 1])[0]
			offset += 1
			tmp54 = s[offset:offset + tmp53]
			offset += tmp53
			tmp54 += b'\x00' * (4 - tmp53)
			tmp55 = struct.unpack('I', tmp54)[0]
			
			self.scores = {}
			for tmp56 in range(tmp55):
				tmp59 = struct.unpack('B', s[offset:offset + 1])[0]
				offset += 1
				if tmp59:
					tmp60 = struct.unpack('B', s[offset:offset + 1])[0]
					offset += 1
					tmp61 = s[offset:offset + tmp60]
					offset += tmp60
					tmp61 += b'\x00' * (4 - tmp60)
					tmp62 = struct.unpack('I', tmp61)[0]
					
					tmp57 = s[offset:offset + tmp62].decode('ISO-8859-1') if PY3 else s[offset:offset + tmp62]
					offset += tmp62
				else:
					tmp57 = None
				tmp63 = struct.unpack('B', s[offset:offset + 1])[0]
				offset += 1
				if tmp63:
					tmp58 = struct.unpack('i', s[offset:offset + 4])[0]
					offset += 4
				else:
					tmp58 = None
				self.scores[tmp57] = tmp58
		else:
			self.scores = None
		
		# deserialize self.constants
		tmp64 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp64:
			self.constants = Constants()
			offset = self.constants.deserialize(s, offset)
		else:
			self.constants = None
		
		return offset
