# -*- coding: utf-8 -*-

# python imports
import sys
import struct
from enum import Enum

PY3 = sys.version_info > (3,)


class ECommandDirection(Enum):
	Up = 0
	Right = 1
	Down = 2
	Left = 3


class ChangeDirection(object):

	@staticmethod
	def name():
		return 'ChangeDirection'


	def __init__(self, direction=None):
		self.initialize(direction)
	

	def initialize(self, direction=None):
		self.direction = direction
	

	def serialize(self):
		s = b''
		
		# serialize self.direction
		s += b'\x00' if self.direction is None else b'\x01'
		if self.direction is not None:
			s += struct.pack('b', self.direction.value)
		
		return s
	

	def deserialize(self, s, offset=0):
		# deserialize self.direction
		tmp0 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		if tmp0:
			tmp1 = struct.unpack('b', s[offset:offset + 1])[0]
			offset += 1
			self.direction = ECommandDirection(tmp1)
		else:
			self.direction = None
		
		return offset


class ActivateWallBreaker(object):

	@staticmethod
	def name():
		return 'ActivateWallBreaker'


	def __init__(self):
		self.initialize()
	

	def initialize(self):
		pass
	

	def serialize(self):
		s = b''
		
		return s
	

	def deserialize(self, s, offset=0):
		return offset
