# -*- coding: utf-8 -*-
# Zeobuilder is an extensible GUI-toolkit for molecular model construction.
# Copyright (C) 2007 - 2012 Toon Verstraelen <Toon.Verstraelen@UGent.be>, Center
# for Molecular Modeling (CMM), Ghent University, Ghent, Belgium; all rights
# reserved unless otherwise stated.
#
# This file is part of Zeobuilder.
#
# Zeobuilder is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# In addition to the regulations of the GNU General Public License,
# publications and communications based in parts on this program or on
# parts of this program are required to cite the following article:
#
# "ZEOBUILDER: a GUI toolkit for the construction of complex molecules on the
# nanoscale with building blocks", Toon Verstraelen, Veronique Van Speybroeck
# and Michel Waroquier, Journal of Chemical Information and Modeling, Vol. 48
# (7), 1530-1541, 2008
# DOI:10.1021/ci8000748
#
# Zeobuilder is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
#--


from zeobuilder import context
from zeobuilder.gui import load_image

import gtk


def init_nodes(nodes):
    from reference import Reference, SpatialReference
    from zeobuilder.gui.edit_properties import EditProperties
    from zeobuilder.gui.fields_dialogs import create_tabbed_main_field
    from zeobuilder.gui.fields.mixin import ReadMixin

    dialog_fields = []

    for node in nodes.itervalues():
        node.icon = load_image(node.info.icon_name, (18, 18))
        node.reference_icon = node.icon.copy()
        Reference.overlay_icon.composite(
            node.reference_icon, 0, 0, 18, 18, 0, 0, 1.0, 1.0,
            gtk.gdk.INTERP_BILINEAR, 255
        )
        dialog_fields.extend(node.dialog_fields)

    main_field = create_tabbed_main_field(dialog_fields)
    attribute_names = set([
        dfi.field.attribute_name for dfi in dialog_fields
        if isinstance(dfi.field, ReadMixin)
    ])
    context.application.edit_properties = EditProperties(main_field, attribute_names)


