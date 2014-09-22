from abc import abstractmethod

class GamePacket:
	_me = False

	@classmethod
	def parsePacket(cls, data):
		from Packets import RequestGameStatePacket, RequestGameStatePacket, PlayerInfoPacket, PlayerGunPacket, BulletInfoPacket
		if RequestGameStatePacket.isPacket(data):
			return RequestGameStatePacket.deserializeData(data)
		elif PlayerInfoPacket.isPacket(data):
			return PlayerInfoPacket.deserializeData(data)
		elif PlayerGunPacket.isPacket(data):
			return PlayerGunPacket.deserializeData(data)
		elif BulletInfoPacket.isPacket(data):
			return BulletInfoPacket.deserializeData(data)
		return None

	def setMe(self, me):
		self._me = me

	def isMe(self):
		return self._me

	@classmethod
	def getPacketId(cls):
		return 0

	@classmethod
	def fromString(cls, data):
		return cls()

	@abstractmethod
	def toString(self):
		return ""

	@classmethod
	def isPacket(cls, data):
		if isinstance(data, cls):
			return data.getPacketId() == cls.getPacketId()
		else:
			if len(data) >= 2:
				return int(data[:2]) == cls.getPacketId()
			else:
				return False

	def serializeData(self):
		return "%2d%1d%s" % (self.getPacketId(), self._me, self.toString())

	@classmethod
	def deserializeData(cls, data):
		if cls.isPacket(data):
			packet = cls.fromString(data[3:])
			if isinstance(packet, GamePacket):
				packet.setMe(bool(int(data[2])))
			return packet
		else:
			return None
