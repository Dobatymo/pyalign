def to_html(x):
	pass





class Formatter:
	def __init__(self, alignment):
		self._alignment = alignment

	def _rows(self, s, t):
		upper = []
		edges = []
		lower = []
		last_x = -1

		is_elastic = self._alignment.solver.options["solver"] == "dtw"

		for i, x in enumerate(self._alignment.s_to_t):
			if x < 0:
				if not is_elastic:
					upper.append(s[i])
					edges.append(" ")
					lower.append(" ")
				else:
					upper.append(s[i])
					edges.append(" ")
					lower.append(t[max(last_x, 0)])
			else:
				for j in range(last_x + 1, x):
					if not is_elastic:
						upper.append(" ")
						edges.append(" ")
						lower.append(t[j])
					else:
						upper.append(s[i])
						edges.append(" ")
						lower.append(t[j])
				upper.append(s[i])
				edges.append("|")
				lower.append(t[x])
				last_x = x

		for j in range(last_x + 1, len(t)):
			if not is_elastic:
				upper.append(" ")
				edges.append(" ")
				lower.append(t[j])
			else:
				upper.append(s[-1])
				edges.append(" ")
				lower.append(t[j])

		return upper, edges, lower

	@property
	def html(self):
		s = self._alignment.problem.s
		t = self._alignment.problem.t

		if s is None or t is None:
			return None

		# if not all(isinstance(x, str) for x in (s, t)):

		if all(isinstance(x, str) for x in s) and all(isinstance(x, str) for x in t):
			upper, edges, lower = self._rows(s, t)
		else:
			upper, edges, lower = self._rows(
				[x._repr_html_() for x in s],
				[x._repr_html_() for x in t])

		upper = "".join([f"<td>{x}</td>" for x in upper])
		edges = "".join([f'<td style="text-align: center;">{x}</td>' for x in edges])
		lower = "".join([f"<td>{x}</td>" for x in lower])

		return f"""
			<table>
			<tr>{upper}</tr>
			<tr>{edges}</tr>
			<tr>{lower}</tr>
			</table>
			"""

	@property
	def text(self):
		s = self._alignment.problem.s
		t = self._alignment.problem.t

		if s is None or t is None:
			return None

		if not all(isinstance(x, str) for x in (s, t)):
			return None

		upper, edges, lower = self._rows(s, t)

		return "\n".join([
			"".join(upper),
			"".join(edges),
			"".join(lower)
		])
