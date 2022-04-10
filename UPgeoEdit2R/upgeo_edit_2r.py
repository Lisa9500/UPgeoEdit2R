# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UPgeoEdit2R
                                 A QGIS plugin
 This plugin edits GeoJSON file
                              -------------------
        begin                : 2016-11-22
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Urban Planning Cyber Studio
        email                : lisa9500jp@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# IMPORT MODULES
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import sys
import os
import os.path

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from upgeo_edit_2r_dialog import UPgeoEdit2RDialog
import linecache


class UPgeoEdit2R:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'UPgeoEdit2R_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = UPgeoEdit2RDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&UPgeo Editor 2R')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'UPgeoEdit2R')
        self.toolbar.setObjectName(u'UPgeoEdit2R')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('UPgeoEdit2R', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/UPgeoEdit2R/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'UPgeo Editor 2R'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&UPgeo Editor 2R'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def fileselectFunc(self):
        # ファイル選択ダイアログを表示し，テキストブラウザにファイル名を入力
        self.fil = QFileDialog.getOpenFileName(parent=None, caption='Open GeoJSONfiles', directory='.', filter='GeoJSONfiles(*.geojson)')
        filInfo = QFileInfo(self.fil)
        self.filename = filInfo.fileName()
        self.dlg.textBrowser.setText(self.filename)
        # 標高メッシュ.geojson


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

        # GeoJSONファイルの選択ボタンをクリックしてファイル選択ダイアログを表示
        self.dlg.pushButton.clicked.connect(self.fileselectFunc)

        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            # pass

            fname = self.filename
            # self.dlg.debugBrowser.setText(fname)

            num_lines = sum(1 for line in open(fname))
            # self.dlg.debugBrowser.setText(str(num_lines))

            # C:/にdataディレクトリがなければ作成する
            dirs = os.listdir("C:/")
            if 'data' not in dirs:
                os.mkdir("C:/data")

            # geojson.csvというファイル名で書き込み用のファイルを開く
            f = open('C:/data/geojson.csv','w')

            for row_no in range(6, num_lines - 1):
                line_text = linecache.getline(fname, row_no)

                # 文字列の置き換え
                line_rep_0 = line_text.replace(" ", "")
                line_rep_2 = line_rep_0.replace("{", "")
                line_rep_3 = line_rep_2.replace("}", "")
                line_rep_4 = line_rep_3.replace("[", "")
                line_rep_5 = line_rep_4.replace("]", "")
                line_rep_6 = line_rep_5.replace("\"", "")

                # コロンをコンマに置き換え
                line_rep_10 = line_rep_6.replace(":", ",")

                # ファイルに修正後の文字列を書き込む
                l_str = line_rep_10
                f.write(l_str)

            # ファイルを閉じる
            f.close
