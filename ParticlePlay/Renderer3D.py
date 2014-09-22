class Renderer3D:
	class Position:
		x = None
		y = None

	_renderer = None
	_perspective = [100, 100, 0.5, 0.5]
	_preOffset = [0, 0, 0]
	_postOffset = [0, 0]

	def __init__(self, renderer):
		self._renderer = renderer

	def _isOutside(self, zOrder):
		return self._perspective[0]-zOrder <= 0 or self._perspective[1]-zOrder <= 0

	def _getPerspectiveZ(self, zOrder):
		x = self._perspective[0]
		y = self._perspective[1]
		if zOrder <= 0.1:
			zOrder = 0.1
		return [((self._perspective[0]* 1.0) / zOrder) * self._perspective[2], ((self._perspective[1] * 1.0) / zOrder) * self._perspective[3]]

	def _getPosition(self, position):
		if len(position) < 3:
			return position
		perspective = self._getPerspectiveZ(position[2]+self._preOffset[2])
		return (self._postOffset[0] + ((position[0]+self._preOffset[0]) * perspective[0]), self._postOffset[1] + ((position[1]+self._preOffset[1]) * perspective[1]))
