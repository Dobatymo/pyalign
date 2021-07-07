from pyalign.tests import TestCase

import pyalign.utils
import pyalign.solve
import pyalign.gaps


class TestWatermanSmithBeyer(TestCase):
	def test_cg_ccga(self):
		# test case is taken from default settings (for logarithmic gap settings) at
		# http://rna.informatik.uni-freiburg.de/Teaching/index.jsp?toolName=Waterman-Smith-Beyer

		pf = pyalign.utils.SimilarityProblemFactory(
			pyalign.utils.Binary(eq=1, ne=-1))
		problem = pf.new_problem("CG", "CCGA")

		solver = pyalign.solve.GlobalSolver(
			gap_cost=pyalign.gaps.LogarithmicGapCost(3, 1),
			direction="maximize",
			generate="alignment[all, optimal]")

		alignments = list(solver.solve(problem))

		self._check_alignments(
			alignments,
			-3.7,
			[[0, 0], [1, 1]],
			[[0, 0], [1, 3]],
			places=1)