#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2011                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from plugins.Plugin import Plugin


class TagWatchMultipleTags(Plugin):

    only_for = ["fr"]

    err_3032    = 3032
    err_3032_en = u"Watch multiple tags"

    def init(self, logger):
        import re
        self.Eglise = re.compile(u"(.glise|chapelle|basilique|cath.drale) de .*", re.IGNORECASE)
        self.EgliseNot1 = re.compile(u"(.glise|chapelle|basilique|cath.drale) de la .*", re.IGNORECASE)
        self.EgliseNot2 = re.compile(u"(.glise|chapelle|basilique|cath.drale) de l'.*", re.IGNORECASE)
        self.MonumentAuxMorts = re.compile(u"monument aux morts.*", re.IGNORECASE)
        self.SalleDesFetes = re.compile(u".*salle des f.tes.*", re.IGNORECASE)
        self.MaisonDeQuartier = re.compile(u".*maison de quartier.*", re.IGNORECASE)

    def node(self, data, tags):
        if not "name" in tags:
            return

        err = []
        if "amenity" in tags:
            if tags["amenity"] == "place_of_worship":
                if self.Eglise.match(tags["name"]) and not self.EgliseNot1.match(tags["name"]) and not self.EgliseNot2.match(tags["name"]):
                    err.append((3032, 1, {"fr": u"name=%s est la localisation mais pas le nom" % (tags["name"])}))
        if "historic" in tags:
            if tags["historic"] == "monument":
                if self.MonumentAuxMorts.match(tags["name"]):
                    err.append((3032, 2, {"fr": u"Un monuments aux Morts est un historic=memorial"}))

        if (not "highway" in tags) and (self.SalleDesFetes.match(tags["name"]) or self.MaisonDeQuartier.match(tags["name"])) and not ("amenity" in tags and tags["amenity"] == "community_centre"):
            err.append((3032, 3, {"fr": u"Le tag pour une salle des fêtes ou une maison de quartier est amenity=community_centre"}))

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)