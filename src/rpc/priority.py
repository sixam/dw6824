class Priority:
	"""Implements a priority object.
	Must be computed upon issuing an operation.
	Exposes < > <= >= == !=.

	Assumes that caller holds the lock on the state.
	"""
	def __init__(self, rq, state):
		self.pd = []
		for qrq in state.queue:
			if qrq.op.opos == op.opos:
				if Priority.compareLists(self.pd, qrq.priority.pd) == 2:
					self.pd = qrq.priority.pd[:]
		self.pd.append(self.state.id);

	@staticmethod
	def compareLists(a, b):
		# 0 a == b
		# 1 a > b
		# 2 a < b
		c = 0
		if not a and not b:
			return 0
		if not b:
			return 1
		if not a:
			return 2
		if len(a) == len(b):
			m = len(a)
		elif len(a) < len(b):
			m = len(a)
			c = 1
		else:
			m = len(b)
			c = 2

		for k in range(m):
			if a[k] > b[k]:
				return 1
			if a[k] < b[k]:
				return 2
		if c == 0:
			return 0 # the two strings are identical
		if c == 1:
			return 2 # b is a substring of a
		else:
			return 1
