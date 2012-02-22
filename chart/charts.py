# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# Author: Eugene Kin Chee Yip
# Date:   16 January 2010
from random import randrange
import json
import copy    

class GoogleChart(object):
    def __init__(self, title, chartType):
        self.title = title
        self.type = chartType
        self.technology = 'javascript'
        
        self.rows = []
        self.cols = []
        self.options = {}
        self.json = {}
        
        self.width = 920
        self.height = 340
        
    def addColumn(self, name, type, id):
        self.cols.append({
            'id': id,
            'label': name,
            'type': type,
        })
        
    def addRow(self, values):
        data = []
        
        index = 0
        for v in values:
            if self.cols[index]['type'] == 'date':
                dateSplit = v.split('.')
                
                v = "new Date(%s,%s,%s)" % (dateSplit[2], dateSplit[1], dateSplit[0])
            
            data.append(v)
                 
            index += 1
        
        self.rows.append(data)
    
    def addOption(self, name, value):
        self.options[name] = value

class Chart(dict):
    # Dictionary for replacing attribute names
    replaceKeyDictionary =    {
        "on_show": "on-show",            "on_click": "on-click",
        "start_angle": "start-angle",    "javascript_function": "javascript-function",
        
        "threeD": "3d",                    "tick_height": "tick-height",
        "grid_colour": "grid-colour",    "tick_length": "tick-length",
        "spoke_labels": "spoke-labels",    "barb_length": "barb-length",
    
        "dot_style": "dot-style",        "dot_size": "dot-size",
        "halo_size": "halo-size",
            
        "line_style": "line-style",        "outline_colour": "outline-colour",
        "fill_alpha": "fill-alpha",        "gradient_fill": "gradient-fill",
        
        "negative_colour": "negative-colour",
    }

    # Redefine to allow for nested attributes.
    # E.g. when calling the leaf attribute, text, in chart.title.text
    #      without previously defining the branch attribute, title.
    def __getattribute__(self, key):
        try:
            return dict.__getattribute__(self, key)
        except AttributeError:
            self.__dict__[key] = Chart()
            return dict.__getattribute__(self, key)

    # This copy function is called when we want to get all the attributes of the 
    # chart instance so we can pass it off to cjson to create the JSON string.
    # Recursive trick to get leaf attributes.  Have to be careful of list types.
    # Also, replace certain underscored keys.
    # E.g. getting the leaf attribute, text, from the parent Chart instance where a  
    #      previous assignment was to chart.title.text
    def __copy__(self):
        attributes = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                attributes[self.replaceKey(key)] = [copy.copy(item) for item in value]
            else:
                attributes[self.replaceKey(key)] = copy.copy(value)
        return attributes

    # If key has an underscore, replace with a dash.
    # Python does not allow dash in object names.
    def replaceKey(self, key):
        if (key in self.replaceKeyDictionary):
            return self.replaceKeyDictionary[key]
        else:
            return key

    # Encode the chart attributes as JSON
    def create(self):
        attributes = copy.copy(self)
        
        return json.dumps(attributes)
    
MIN_MAX_OVER = 1.25
MAX_X_LABELS = 30
MAX_Y_LABELS = 6

# Docs avaible at: http://teethgrinder.co.uk/open-flash-chart-2/json-format.php
class ChartExt(Chart):
    def __init__(self, title, chartType):
        self.title.text = title
        self.elements = []
        self.type = chartType
        self.technology = 'flash'
        
        self.width = 920
        self.height = 340
        
        # X-axis
        self.x_axis = {
            'stroke': 1,
            'tick_height': 10,
            'colour': '#d000d0',
            'grid_colour': '#00ff00',
            'labels': {
                'labels': [],
                'rotate': 60,
            }
        }
        
        # Y-axis
        self.y_axis = {
            'stroke': 1,
            'tick_height': 10,
            'step': 3,
            'colour': '#d000d0',
            'grid_colour': '#00ff00',
            'min': None,
            'max': None
        }
        
    def _buildElementData(self, dict):
        data = {
            'type': self.type,
            'alpha': 0.8,
            'colour': '#%s' % '' . join([hex(randrange(0, 255))[2:] for i in range(3)]),
            'font-size': 10,
            'values': [],
            'text': ''
        }
        
        for key, value in dict.items():
            data[key] = value
        
        return data
    
    def _updateAxisY(self, value):
        if self.y_axis['min'] > value or self.y_axis['min'] is None:
            self.y_axis['min'] = float(value)
            
        if self.y_axis['max'] < value or self.y_axis['max'] is None:
            self.y_axis['max'] = float(value)
        
    # value can be integer or dict (in candle charts)
    def addElement(self, text, value, label, **kwargs):
        element = None
        
        for e in self.elements:
            if e['text'] == text:
                element = e
                self.elements.remove(e)
                break
        
        if element is None:
            dict = kwargs
            dict['text'] = text
            
            element = self._buildElementData(dict)
            
        element['values'].append(value)
            
        self.elements.append(element)
        
        # Update Axis (x & y)
        try:
            float(value)
        except (ValueError, TypeError):
            for key, value in value.items():
                self._updateAxisY(value)
        else:
            self._updateAxisY(value)
            
        self.x_axis['labels']['labels'].append(label)
            
    def changeTitle(self, title, style):
        self.title.text = title
        self.title.style = style
        
    # Do last calculations
    def prepare(self):
        # Calculate min & max for Y-axis (add some %)
        self.y_axis['min'] /= MIN_MAX_OVER
        self.y_axis['max'] *= MIN_MAX_OVER
        
        # Y-axis step
        mini = self.y_axis['min']
        maxi = self.y_axis['max']
        
        if mini and maxi:
            self.y_axis['steps'] = (maxi-mini) / MAX_Y_LABELS
            
        # Tooltip
        if self.type == 'candle':
            self.elements[0]['tip'] = "\nHigh: #high#\nOpen: #open#\nClose: #close#\nLow: #low#"
            
        # X-axis labels
        labels = self.x_axis['labels']['labels']
        
        if len(labels) > MAX_X_LABELS:
            self.x_axis['labels']['steps'] = len(labels) / MAX_X_LABELS