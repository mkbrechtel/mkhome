#!/usr/bin/python

import colorsys

class FilterModule(object):
    def filters(self):
        return {'hsv2rgb': self.hsv2rgb}

    def hsv2rgb(self, hue, saturation, value):
        rgb = colorsys.hsv_to_rgb(hue/360., saturation/100., value/100.)
        rgb = tuple(map(lambda x: round(x*255), rgb))
        return '#%02x%02x%02x' % rgb
