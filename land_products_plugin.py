from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterString
import processing
import os
import urllib.request
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterEnum
from processing.gui.wrappers import WidgetWrapper
from qgis.PyQt.QtCore import Qt, QCoreApplication


class Copernicus(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.services = ['Bare-CoverFraction-layer', 'BuiltUp-CoverFraction-layer', 'Crops-CoverFraction-layer',
                         'DataDensityIndicator', 'Discrete-Classification-map', 'Discrete-Classification-proba',
                         'Forest-Type-layer', 'Grass-CoverFraction-layer', 'MossLichen-CoverFraction-layer',
                         'PermanentWater-CoverFraction-layer', 'SeasonalWater-CoverFraction-layer',
                         'Shrub-CoverFraction-layer', 'Snow-CoverFraction-layer', 'Tree-CoverFraction-layer']
        self.yearlist = ['2015', '2016', '2017', '2018', '2019']

        self.addParameter(QgsProcessingParameterEnum('prodotto', 'Product', options=self.services, defaultValue=None))
        self.addParameter(QgsProcessingParameterEnum('anno', 'Year', options=self.yearlist, defaultValue=None))
        # self.addParameter(QgsProcessingParameterString('anno', 'Year', defaultValue=None))
        self.addParameter(QgsProcessingParameterString('nome_tile', 'Tile Name', defaultValue=None))
        # self.addParameter(QgsProcessingParameterString('prodotto', 'prodotto', defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('Download directory', 'Download directory',
                                                     behavior=QgsProcessingParameterFile.Folder, optional=True,
                                                     defaultValue=None))

    def search_Data(self, anno=None, nome_tile=None, prodotto=None):
        list_file = 'list2.txt'

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

        if self.services[parameters['nome_tile']] == 'None':
            nome_tile = None
        else:
            nome_tile = self.services[parameters['nome_tile']]

        anno = self.services[parameters['anno']]
        # nome_tile = self.services[parameters['nome_tile']]
        prodotto = self.services[parameters['prodotto']]

        download = search_Data(prodotto=prodotto, anno=anno, nome_tile=nome_tile)

        for d in download:
            output = self.services[parameters['prodotto']] + os.path.basename(d)
            urllib.request.urlretrieve(d, output)

    def name(self):
        return 'Copernicus Land Cover Download'

    def displayName(self):
        return 'Copernicus Land Cover Download'

    def group(self):
        return 'Copernicus Global Land Tools'

    def groupId(self):
        return 'Copernicus Global Land Tools'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return "Download Copernicus Land Cover products" \

                return Copernicus()
