class Priority:
	"""Implements a priority object.
	Must be computed upon issuing an operation.
	Exposes < > <= >= == !=.

	Assumes that caller holds the lock on the state.
	"""
	def __init__(self, rq=None, state=None, pd=[]):
		if pd:
			self.pd = pd
			return
		self.pd = []
		for qrq in state.queue:
			if qrq.op.opos == rq.op.opos:
				if Priority.compareLists(self.pd, qrq.priority.pd) < 0:
					self.pd = qrq.priority.pd[:]
		self.pd.append(self.state.id);

	def __cmp__(self,other):
		return Priority.compareLists(self.pd, other.pd)
		

	@staticmethod
	def compareLists(a, b):
		# 0 a == b
		# 1 a > b
		# -1 a < b
		c = 0
		if not a and not b:
			return 0
		if not b:
			return 1
		if not a:
			return -1
		if len(a) == len(b):
			m = len(a)
		elif len(a) < len(b):
			m = len(a)
			c = -1
		else:
			m = len(b)
			c = 1

		for k in range(m):
			if a[k] > b[k]:
				return 1
			if a[k] < b[k]:
				return -1
		if c == 0:
			return 0 # the two strings are identical
		if c == -1:
			return -1 # b is a substring of a
		else:
			return 1
