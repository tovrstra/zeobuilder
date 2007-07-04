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


from zeobuilder.actions.abstract import AddBase
from zeobuilder.actions.collections.menu import MenuInfo
from zeobuilder.nodes.meta import Property
from zeobuilder.nodes.model_object import ModelObject, ModelObjectInfo
from zeobuilder.gui.fields_dialogs import DialogFieldInfo
import zeobuilder.gui.fields as fields
import zeobuilder.authors as authors

import StringIO


class Notes(ModelObject):
    info = ModelObjectInfo("plugins/basic/notes.svg")
    authors = [authors.toon_verstraelen]

    #
    # Properties
    #

    def set_notes(self, notes):
        self.notes = notes

    properties = [
        Property("notes", StringIO.StringIO(), lambda self: self.notes, set_notes)
    ]

    #
    # Dialog fields (see action EditProperties)
    #

    dialog_fields = set([
        DialogFieldInfo("Basic", (0, 10), fields.edit.TextView(
            label_text="Notes",
            attribute_name="notes",
        ))
    ])


class AddNotes(AddBase):
    description = "Add notes"
    menu_info = MenuInfo("default/_Object:tools/_Add:non3d", "_Notes", image_name="plugins/basic/notes.svg", order=(0, 4, 1, 0, 1, 1))
    authors = [authors.toon_verstraelen]

    @staticmethod
    def analyze_selection():
        return AddBase.analyze_selection(Notes)

    def do(self):
        AddBase.do(self, Notes)


nodes = {
    "Notes": Notes
}

actions = {
    "AddNotes": AddNotes,
}
