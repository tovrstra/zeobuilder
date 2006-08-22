# Zeobuilder is an extensible GUI-toolkit for molecular model construction.
# Copyright (C) 2005 Toon Verstraelen
#
# This file is part of Zeobuilder.
#
# Zeobuilder is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# --


from zeobuilder import context



class Expression(object):
    l = {}

    def __init__(self, code="True"):
        self.compiled = compile(code, "<string>", 'eval')
        self.code = code
        self.variables = ("node",)

    def compile_as(self, name):
        self.compiled = compile(self.code, name, 'eval')

    def __call__(self, *variables):
        g = {"__builtins__": __builtins__}
        g.update(self.l)
        for name, variable in zip(self.variables, variables):
            g[name] = variable
        return eval(self.compiled, g)


def init_locals(nodes):
    from molmod.data import periodic, bonds, BOND_SINGLE, BOND_DOUBLE, BOND_TRIPLE
    l = {
        "periodic": periodic,
        "bonds": bonds,
        "BOND_SINGLE": BOND_SINGLE,
        "BOND_DOUBLE": BOND_DOUBLE,
        "BOND_TRIPLE": BOND_TRIPLE,
    }

    l.update(nodes)

    import molmod.units
    for key, val in molmod.units.__dict__.iteritems():
        if isinstance(val, float):
            l[key] = val
    Expression.l = l