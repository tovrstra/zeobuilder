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
from zeobuilder.nodes.parent_mixin import ContainerMixin

from molmod.data import periodic
from molmod.graphs import Graph


def yield_atoms(nodes):
    Atom = context.application.plugins.get_node("Atom")
    for node in nodes:
        if isinstance(node, Atom):
            yield node
        elif isinstance(node, ContainerMixin):
            for atom in yield_atoms(node.children):
                yield atom


def yield_bonds(nodes):
    Bond = context.application.plugins.get_node("Bond")
    for node in nodes:
        if isinstance(node, Bond):
            yield node
        elif isinstance(node, ContainerMixin):
            for bond in yield_bonds(node.children):
                yield bond


def chemical_formula(atoms, markup=False):
    atom_counts = {}
    for atom in atoms:
        if atom.number in atom_counts:
            atom_counts[atom.number] += 1
        else:
            atom_counts[atom.number] = 1
    total = 0
    formula = ""
    items = atom_counts.items()
    items.sort()
    items.reverse()
    for atom_number, count in items:
        if markup:
            formula += "%s<sub>%i</sub>" % (periodic[atom_number].symbol, count)
        else:
            formula += "%s%i " % (periodic[atom_number].symbol, count)
        total += count
    return total, formula


def create_graph_bonds(selected_nodes):
    nodes = list(yield_atoms(selected_nodes))
    bonds_by_pair = dict(
        (frozenset([bond.children[0].target, bond.children[1].target]), bond)
        for bond in yield_bonds(selected_nodes)
        if bond.children[0].target in nodes and
            bond.children[1].target in nodes
    )
    # uncommented these lines to make sure that the order of the list nodes
    # is respected.
    #tmp = set([])
    #for a, b in bonds_by_pair.iterkeys():
    #    tmp.add(a), tmp.add(b)
    #nodes = [node for node in nodes if node in tmp]

    graph = Graph(bonds_by_pair.keys(), nodes)
    return graph, bonds_by_pair