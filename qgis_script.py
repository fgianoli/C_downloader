# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
from qgis import processing
import os
import urllib.request
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterString


class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    # INPUT = 'INPUT'
    # OUTPUT = 'OUTPUT'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ExampleProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'copernicuslandcover'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Copernicus Land Cover Download')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Copernicus Global Land Tools')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Copernicus Global Land Tools'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Example algorithm short description")

    def initAlgorithm(self, config=None):
        self.services = ['Bare-CoverFraction-layer', 'BuiltUp-CoverFraction-layer', 'Crops-CoverFraction-layer',
                         'DataDensityIndicator', 'Discrete-Classification-map', 'Discrete-Classification-proba',
                         'Forest-Type-layer', 'Grass-CoverFraction-layer', 'MossLichen-CoverFraction-layer',
                         'PermanentWater-CoverFraction-layer', 'SeasonalWater-CoverFraction-layer',
                         'Shrub-CoverFraction-layer', 'Snow-CoverFraction-layer', 'Tree-CoverFraction-layer']
        self.yearlist = ['2015', '2016', '2017', '2018', '2019']

        self.addParameter(QgsProcessingParameterEnum('prodotto', 'Product', options=self.services, defaultValue=None))
        self.addParameter(QgsProcessingParameterEnum('anno', 'Year', options=self.yearlist, defaultValue=None))
        #self.addParameter(QgsProcessingParameterString('anno', 'Year', defaultValue=None))
        self.addParameter(QgsProcessingParameterString('nome_tile', 'Tile Name', defaultValue='W180S40'))
        #self.addParameter(QgsProcessingParameterString('prodotto', 'prodotto', defaultValue='Bare-CoverFraction-layer'))
        self.addParameter(QgsProcessingParameterFile('Download directory', 'Download directory',
                                                     behavior=QgsProcessingParameterFile.Folder, optional=True,
                                                     defaultValue=None))



    def processAlgorithm(self, parameters, context, feedback):
        anno = self.parameterAsSource(parameters, 'anno', context)
        nome_tile = self.parameterAsSource(parameters, 'nome_tile', context)
        prodotto = self.parameterAsSource(parameters, 'prodotto', context)

        list_file = 'C:\\Users\\giano\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\copernicus\\processing\\scripts\\list2.txt'

        # read list of files
        f = open(list_file, 'r')
        data = f.readlines()
        files = [f.rstrip() for f in data]
        f.close()

        base_URL = 'https://s3-eu-west-1.amazonaws.com/vito.landcover.global/v3.0.1/'

        urls = []

        for file in files:
            filename = file.split('/')[2]
            year = file.split('/')[0]
            tile = file.split('/')[1]
            if prodotto is not None and prodotto in file:
                if anno is not None and anno in file:
                    if nome_tile is not None and nome_tile in file:
                        urls.append(base_URL + year + '/' + tile + '/' + filename)
                    if nome_tile is None:
                        urls.append(base_URL + year + '/' + tile + '/' + filename)
                if anno is None:
                    if nome_tile is not None and nome_tile in file:
                        urls.append(base_URL + year + '/' + tile + '/' + filename)
                    if nome_tile is None:
                        urls.append(base_URL + year + '/' + tile + '/' + filename)
            if prodotto is None:
                if anno is not None and anno in file:
                    if nome_tile is not None and nome_tile in file:
                        urls.append(base_URL + year + '/' + tile + '/' + filename)
                    if nome_tile is None:
                        urls.append(base_URL + year + '/' + tile + '/' + filename)
                if anno is None:
                    if nome_tile is not None and nome_tile in file:
                        urls.append(base_URL + year + '/' + tile + '/' + filename)
                    if nome_tile is None:
                        urls.append(base_URL + year + '/' + tile + '/' + filename)

        # for u in urls:
        # print(u)

        return urls

        
        download = processAlgorithm(prodotto=prodotto, anno=anno, nome_tile=nome_tile)

        for d in download:
            output = self.services[parameters['Download directory']] + os.path.basename(d)
            urllib.request.urlretrieve(d, output)



