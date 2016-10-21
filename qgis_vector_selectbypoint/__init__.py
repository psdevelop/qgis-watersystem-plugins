# -*- coding: utf-8 -*-
"""
/***************************************************************************
 vector_selectbypoint
                                 A QGIS plugin
 Select vector features, point and click.
                             -------------------
        begin                : 2014-04-07
        copyright            : (C) 2014 by Brylie Oxley
        email                : brylie@geolibre.org
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

def classFactory(iface):
    # load vector_selectbypoint class from file vector_selectbypoint
    from vector_selectbypoint import vector_selectbypoint
    return vector_selectbypoint(iface)
