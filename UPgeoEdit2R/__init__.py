# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UPgeoEdit2R
                                 A QGIS plugin
 This plugin edits GeoJSON file
                             -------------------
        begin                : 2016-11-22
        copyright            : (C) 2016 by Urban Planning Cyber Studio
        email                : lisa9500jp@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load UPgeoEdit2R class from file UPgeoEdit2R.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .upgeo_edit_2r import UPgeoEdit2R
    return UPgeoEdit2R(iface)
