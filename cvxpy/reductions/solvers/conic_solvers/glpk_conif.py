"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

import cvxpy.settings as s
from cvxpy.constraints import NonPos, Zero
from cvxpy.reductions.solvers.conic_solvers import CVXOPT
from cvxpy.problems.problem_data.problem_data import ProblemData


class GLPK(CVXOPT):
    """An interface for the GLPK solver.
    """

    # Solver capabilities.
    LP_CAPABLE = True
    SOCP_CAPABLE = False
    SDP_CAPABLE = False
    EXP_CAPABLE = False
    MIP_CAPABLE = False

    def name(self):
        """The name of the solver.
        """
        return s.GLPK

    def import_solver(self):
        """Imports the solver.
        """
        from cvxopt import glpk
        glpk  # For flake8

    def accepts(self, problem):
        """Can CVXOPT solve the problem?
        """
        # TODO check if is matrix stuffed.
        if not problem.objective.args[0].is_affine():
            return False
        for constr in problem.constraints:
            if type(constr) not in [Zero, NonPos]:
                return False
            for arg in constr.args:
                if not arg.is_affine():
                    return False
        return True

    def solve_via_data(self, data, warm_start, verbose, solver_opts):
        from cvxpy.problems.solvers.glpk_intf import GLPK as GLPK_OLD
        solver = GLPK_OLD()
        return solver.solve(
            data["objective"],
            data["constraints"],
            {self.name(): ProblemData()},
            warm_start,
            verbose,
            solver_opts)
