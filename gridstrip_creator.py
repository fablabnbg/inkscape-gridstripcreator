#!/usr/bin/env python
'''
Grid Strip Creator  v1.0 (30/11/2014)


Copyright (C) 2014 Thomas Gebert - tsgebert **AT** web.de

## This basic extension allows you to automatically draw guides in inkscape for hexagons.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

# Making an .INX file : http://wiki.inkscape.org/wiki/index.php/MakingAnINX
# see also http://codespeak.net/lxml/dev/tutorial.html#namespaces for XML namespaces manipulation
 

# # # extension's begining # # #

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
from inkex import Effect, PathElement, Group, TextElement, Style, Layer

from xml.etree import ElementTree as ET

# for printing debugging output
import gettext
_ = gettext.gettext

def printDebug(string):
	inkex.errormsg(_(string))
	

class GridStrip_Creator(inkex.GenerateExtension):
	container_label = 'GridstripCreator'
	container_layer = True

	def add_arguments(self,pars):
		# inkex.Effect.__init__(self)
		# """
		# Constructor.
		# Defines options of the script.
		# """
		# # Call the base class constructor.
		# inkex.Effect.__init__(self)
		# Define string option "--length" with default value '0.0'.
		pars.add_argument('--length',
			type = float,
			dest = 'length',default = 230.0,
			help = 'Length of strip')
			
		# Define string option "--width" with default value '0.0'.
		pars.add_argument('--width',
			type = float,
			dest = 'width',default = 20.0,
			help = 'Width of strip')

		# Define string option "--cellheight" with default value '0.0'.
		pars.add_argument('--cellheight',
			type = float,
			dest = 'cellheight',default = 12.5,
			help = 'height of cell')
			
		# Define string option "--cellwidth" with default value '0.0'.
		pars.add_argument('--cellwidth',
			type = float,
			dest = 'cellwidth',default = 12.5,
			help = 'Width of cell')
			
		# Define string option "--scalecells" with default value False.
		pars.add_argument('--scalecells',
			type = inkex.Boolean,
			dest = 'scalecells',default = False,
			help = 'Scale cells over length')

		# Define string option "--cellnumx" with default value '0.0'.
		pars.add_argument('--cellnumx',
			type = int,
			dest = 'cellnumx',default = 11,
			help = 'Number of cells x')
			
		# Define string option "--cellnumy" with default value '0.0'.
		pars.add_argument('--cellnumy',
			type = int,
			dest = 'cellnumy',default = 10,
			help = 'Number of cells y')
			
		# Define string option "--notchdepth" with default value '0.0'.
		pars.add_argument('--notchdepth',
			type = float,
			dest = 'notchdepth',default = 1.0,
			help = 'Depth of notch')
        
		# Define string option "--notchwidth" with default value '0.0'.
		pars.add_argument('--notchwidth',
			type = float,
			dest = 'notchwidth',default = 10.0,
			help = 'Width of notch')
			
		# Define string option "--notchhorizontal" with default value False.
		pars.add_argument('--notchhorizontal',
			type = inkex.Boolean,
			dest = 'notchhorizontal',default = False,
			help = 'Make notches on horizontal strip')
 
		# Define string option "--notchvertical" with default value False.
		pars.add_argument('--notchvertical',
			type = inkex.Boolean,
			dest = 'notchvertical',default = False,
			help = 'Make notches on vertical strip')
         
		# Define string option "--notch2depth" with default value '0.0'.
		# pars.add_argument('--notch2depth',
			# type = float,
			# dest = 'notch2depth',default = 10.0,
			# help = 'Depth of notch')
        
		# Define string option "--notch2width" with default value '0.0'.
		pars.add_argument('--notch2width',
			type = float,
			dest = 'notch2width',default = 3.0,
			help = 'Width of notch')

		# Define string option "--notchxcorner" with default value False.
		pars.add_argument('--notchxcorner',
			type = inkex.Boolean,
			dest = 'notchxcorner',default = False,
			help = 'Make notches on corner of horizontal strip')
 
		# Define string option "--notchycorner" with default value False.
		pars.add_argument('--notchycorner',
			type = inkex.Boolean,
			dest = 'notchycorner',default = False,
			help = 'Make notches on corner of vertical strip')
         

			
	def generate(self):
		# Get access to main SVG document element and get its dimensions.
		svg = self.svg


		# Get access to the current layer.
		# svg.current_layer() returns the current layer of the document.
		#parent = self.svg.current_layer()


		# getting the parent tag of the guide
		nv = self.document.xpath('/svg:svg/sodipodi:namedview',namespaces=inkex.NSS)[0]
		
		documentUnits = inkex.addNS('document-units', 'inkscape')
		# print  >> sys.stderr, nv.get(documentUnits)
		# uunits = nv.get(documentUnits)
		# message="Units="+uunits
		# inkex.utils.debug(message)

		message="Option width="+str(self.options.width)
		inkex.utils.debug(message)
		message="Option length="+str(self.options.length)
		inkex.utils.debug(message)
		# Get script's options value.
		stripwidth=svg.unit_to_viewport(str(self.options.width)+"mm","px")
		striplength=svg.unit_to_viewport(str(self.options.length)+"mm","px")
		message="strip width="+str(stripwidth)
		inkex.utils.debug(message)
		message="strip length="+str(striplength)
		inkex.utils.debug(message)
		cellheight=svg.unit_to_viewport(str(self.options.cellheight)+"mm","px")
		cellwidth=svg.unit_to_viewport(str(self.options.cellwidth)+"mm","px")

		scalecells=(self.options.scalecells)
		
		cellnumx=(self.options.cellnumx)
		cellnumy=(self.options.cellnumy)
		
		notchdepth=svg.unit_to_viewport(str(self.options.notchdepth)+"mm","px")
		notchwidth=svg.unit_to_viewport(str(self.options.notchwidth)+"mm","px")
		
		notchhorizontal=(self.options.notchhorizontal)
		notchvertical=(self.options.notchvertical)
				
#		notch2depth=svg.to_dimensionless(str(self.options.notch2depth)+uunits)
		notch2width=svg.unit_to_viewport(str(self.options.notch2width)+"mm","px")
		
		notch2depth= stripwidth/2
		
		notchxcorner=(self.options.notchxcorner)
		notchycorner=(self.options.notchycorner)

		if scalecells:
			cellwidth=(striplength-4*notch2width)/cellnumx
			cellheight=(striplength-4*notch2width)/cellnumy
			notchxcorner=False
			notchycorner=False
		
		
		linewidth=svg.to_dimensionless(str(1))
		distx=(striplength-cellnumx*cellwidth)/2	
		disty=(striplength-cellnumy*cellheight)/2
		
		celldistx=(cellwidth-notchwidth)/2
		celldisty=(cellheight-notch2width)/2

		# getting the width and height attributes of the canvas
		width  = float(svg.to_dimensionless(svg.attrib['width']))
		height = float(svg.to_dimensionless(svg.attrib['height']))
		# maxlength=max(width,height)
		# if striplength > maxlength:
			# factor=striplength/maxlength+1

		inkex.utils.debug("document width="+str(width))
		inkex.utils.debug("document height="+str(height))
		
		inkex.utils.debug("strip length="+str(striplength))
		inkex.utils.debug("strip width="+str(stripwidth))

		inkex.utils.debug("cell width="+str(cellwidth))
		inkex.utils.debug("cell height="+str(cellheight))

		inkex.utils.debug("Number of cells horizontal="+str(cellnumx))
		inkex.utils.debug("Number of cells vertical  ="+str(cellnumy))
				
		inkex.utils.debug("Depth of extra notch="+str(notchdepth))
		inkex.utils.debug("Width of extra notch="+str(notchwidth))

		inkex.utils.debug("Depth of notch for grid="+str(notchdepth))
		inkex.utils.debug("Width of notch for grid="+str(notchwidth))

		inkex.utils.debug("distx="+str(distx))
		inkex.utils.debug("disty="+str(disty))

		inkex.utils.debug("celldistx="+str(celldistx))
		inkex.utils.debug("celldisty="+str(celldisty))
		
		parent = self.svg.get_current_layer()



		layername=''
		if notchhorizontal:
			layername=layername+'VLED '
		if notchvertical:
			layername=layername+'HLED '
		

		layer = parent.add(inkex.Layer.new(layername+'Long strips'))

		grp = inkex.Group()
		grp.set('inkscape:label','group horizontal strip long')
		layer.add(grp)
		
		

		style = { 'stroke': '#000000', 'stroke-width':str(linewidth), 'fill': 'none' }

		for num in range(0,2):		
			pathstring='M '+str(1)+','+str(1)+' L '
			if notchxcorner:
				pathstring+=str(stripwidth-2*notchdepth)+','+str(1)		# Obere Querkante
				pathstring+=' L '+str(stripwidth-2*notchdepth)+','+str(notchwidth)		# Erste Kerbe aussen
				pathstring+=' L '+str(stripwidth)+','+str(notchwidth)		# Ausrueckung
			else:
				pathstring+=str(stripwidth)+','+str(1)
			if notchhorizontal:
				pathstring+=' L '+str(stripwidth)+','+str(distx)					# Distance to corner
				y=distx
				for i in range(0,cellnumx):
					pathstring+=' L '+str(stripwidth)+','+str(y+celldistx)					# Abstand
					pathstring+=' L '+str(stripwidth-notchdepth)+','+str(y+celldistx)		# Einrueckung
					pathstring+=' L '+str(stripwidth-notchdepth)+','+str(y+celldistx+notchwidth)	# Kerbe
					pathstring+=' L '+str(stripwidth)+','+str(y+celldistx+notchwidth)				# Ausrueckung
					pathstring+=' L '+str(stripwidth)+','+str(y+2*celldistx+notchwidth)				# Abstand
					y=y+2*celldistx+notchwidth
			if notchxcorner:
				pathstring+=' L '+str(stripwidth)+','+str(striplength-notchwidth)					# Untere rechte Ecke
				pathstring+=' L '+str(stripwidth-2*notchdepth)+','+str(striplength-notchwidth)					# Untere rechte Ecke
				pathstring+=' L '+str(stripwidth-2*notchdepth)+','+str(striplength)					# Untere rechte Ecke
			else:
				pathstring+=' L '+str(stripwidth)+','+str(striplength)
			pathstring+=' L '+str(1)+','+str(striplength)							# Linke untere Ecke

			y=striplength-distx+notch2width/2
			
			pathstring+=' L '+str(1)+','+str(y)					# Distance to corner
			pathstring+=' L '+str(notch2depth)+','+str(y)		# Einrueckung

			
			for i in range(0,cellnumx):
				pathstring+=' L '+str(notch2depth)+','+str(y-notch2width)					# Kerbe
				pathstring+=' L '+str(1)+','+str(y-notch2width)		# Ausrueckung
				pathstring+=' L '+str(1)+','+str(y-notch2width-cellwidth+notch2width)	# Abstand
				pathstring+=' L '+str(notch2depth)+','+str(y-notch2width-cellwidth+notch2width)				# Einrueckung
				y=y-notch2width-cellwidth+notch2width
			
			pathstring+=' L '+str(notch2depth)+','+str(y-notch2width)					# Kerbe 
			pathstring+=' L '+str(1)+','+str(y-notch2width)		# Ausrueckung
			
			pathstring+=' L '+str(1)+','+str(1)+' z'

			strip_transform= 'rotate(' + str(90)+')'
			strip_transform+=' translate('+str(stripwidth*num)+','+str(1)+')'

			pathstring = inkex.PathElement(d=pathstring)
			pathstring.set('style',style)
			pathstring.set('inkscape:label',"strip horizontal long"+str(num))
			pathstring.set('transform', strip_transform)
			# strip_attribs = {'style':mystyle,
			# 					inkex.addNS('label','inkscape'):"strip horizontal long",
			# 					'transform': strip_transform,
			# 					'd':pathstring}
			

			grp.add(pathstring)
		
		
		celldisty=(cellheight-notch2width-notchwidth)/2

		grp_name = 'group_vertical_strip_long'

		grp = inkex.Group()
		grp.set('inkscape:label',grp_name)
		layer.add(grp)

		for num in range(0,2):
			y=disty-notch2width/2
			pathstring='M '+str(1)+','+str(1)
			if notchycorner:
				pathstring+=' L '+str(stripwidth-2*notchdepth)+','+str(1)		# Obere Querkante
				pathstring+=' L '+str(stripwidth-2*notchdepth)+','+str(notchwidth)
				pathstring+=' L '+str(stripwidth)+','+str(notchwidth)
			else:
				pathstring+=' L '+str(stripwidth)+','+str(1)
			pathstring+=' L '+str(stripwidth)+','+str(y)					# Distance to corner

			for i in range(0,cellnumy):
				pathstring+=' L '+str(stripwidth-notch2depth)+','+str(y)		# Einrueckung
				pathstring+=' L '+str(stripwidth-notch2depth)+','+str(y+notch2width)	# Kerbe
				pathstring+=' L '+str(stripwidth)+','+str(y+notch2width)				# Ausrueckung
				if notchvertical:
					pathstring+=' L '+str(stripwidth)+','+str(y+notch2width+celldisty)					# Abstand
					pathstring+=' L '+str(stripwidth-notchdepth)+','+str(y+notch2width+celldisty)		# Einrueckung
					pathstring+=' L '+str(stripwidth-notchdepth)+','+str(y+notch2width+celldisty+notchwidth)	# Kerbe
					pathstring+=' L '+str(stripwidth)+','+str(y+notch2width+celldisty+notchwidth)				# Ausrueckung
				pathstring+=' L '+str(stripwidth)+','+str(y+notch2width+2*celldisty+notchwidth)				# Abstand
				y=y+notch2width+2*celldisty+notchwidth

					
			pathstring+=' L '+str(stripwidth-notch2depth)+','+str(y)		# Einrueckung
			pathstring+=' L '+str(stripwidth-notch2depth)+','+str(y+notch2width)	# Kerbe
			pathstring+=' L '+str(stripwidth)+','+str(y+notch2width)				# Ausrueckung

			if notchycorner:
				pathstring+=' L '+str(stripwidth)+','+str(striplength-notchwidth)					# Untere rechte Ecke
				pathstring+=' L '+str(stripwidth-2*notchdepth)+','+str(striplength-notchwidth)					# Untere rechte Ecke
				pathstring+=' L '+str(stripwidth-2*notchdepth)+','+str(striplength)					# Untere rechte Ecke
			else:
				pathstring+=' L '+str(stripwidth)+','+str(striplength)
			pathstring+=' L '+str(1)+','+str(striplength)							# Linke untere Ecke
			pathstring+=' L '+str(1)+','+str(1)+' z'
			
			strip_transform= 'translate('+str(num*stripwidth)+','+str(1)+')'
			pathstring = inkex.PathElement(d=pathstring)
			pathstring.set('style',style)
			pathstring.set('inkscape:label',"strip vertical long "+str(num))
			pathstring.set('transform', strip_transform)
			grp.add(pathstring)
		yield layer


		layer = parent.add(inkex.Layer.new(layername+'Horizontal strips short'))

		grp_name = 'group horizontal_strip_short'
		grp = inkex.Group()
		grp.set('inkscape:label',grp_name)
		layer.add(grp)
		
		striplength=cellnumx*cellwidth+4*notch2width
		distx=(striplength-cellnumx*cellwidth)/2	
		disty=(striplength-cellnumy*cellheight)/2

		style = { 'stroke': '#000000', 'stroke-width':str(linewidth), 'fill': 'none' }
		
		for num in range(1,cellnumy):
		
			pathstring='M '+str(1)+','+str(1)+' L '
			pathstring+=str(stripwidth)+','+str(1)
			if notchhorizontal:
				pathstring+=' L '+str(stripwidth)+','+str(distx)					# Distance to corner
				y=distx
				for i in range(0,cellnumx):
					pathstring+=' L '+str(stripwidth)+','+str(y+celldistx)					# Abstand
					pathstring+=' L '+str(stripwidth-notchdepth)+','+str(y+celldistx)		# Einrueckung
					pathstring+=' L '+str(stripwidth-notchdepth)+','+str(y+celldistx+notchwidth)	# Kerbe
					pathstring+=' L '+str(stripwidth)+','+str(y+celldistx+notchwidth)				# Ausrueckung
					pathstring+=' L '+str(stripwidth)+','+str(y+2*celldistx+notchwidth)				# Abstand
					y=y+2*celldistx+notchwidth
			pathstring+=' L '+str(stripwidth)+','+str(striplength)
			pathstring+=' L '+str(1)+','+str(striplength)							# Linke untere Ecke
							
			y=striplength-distx+notch2width/2
			
			pathstring+=' L '+str(1)+','+str(y)					# Distance to corner
			pathstring+=' L '+str(notch2depth)+','+str(y)		# Einrueckung
			
			for i in range(0,cellnumx):
				pathstring+=' L '+str(notch2depth)+','+str(y-notch2width)					# Kerbe
				pathstring+=' L '+str(1)+','+str(y-notch2width)		# Ausrueckung
				pathstring+=' L '+str(1)+','+str(y-notch2width-cellwidth+notch2width)	# Abstand
				pathstring+=' L '+str(notch2depth)+','+str(y-notch2width-cellwidth+notch2width)				# Einrueckung
				y=y-notch2width-cellwidth+notch2width
			
			pathstring+=' L '+str(notch2depth)+','+str(y-notch2width)					# Kerbe 
			pathstring+=' L '+str(1)+','+str(y-notch2width)		# Ausrueckung
			
			pathstring+=' L '+str(1)+','+str(1)+' z'

			strip_transform='rotate(' + str(90)+')'
			strip_transform+=' translate('+str((num+1)*stripwidth+2)+','+str(1)+')'

			stripname="strip horizontal short "+str(num)
			pathstring = inkex.PathElement(d=pathstring)
			pathstring.set('style',style)
			pathstring.set('inkscape:label',stripname)
			pathstring.set('transform', strip_transform)
			grp.add(pathstring)
		yield layer	
			
		layer = parent.add(inkex.Layer.new(layername+'Vertical strips short'))

		grp_name = 'group vertical_strip_short'
		grp = inkex.Group()
		grp.set('inkscape:label',grp_name)
		layer.add(grp)
		
		striplength=cellnumx*cellwidth+4*notch2width
		distx=(striplength-cellnumx*cellwidth)/2	
		disty=(striplength-cellnumy*cellheight)/2

		striplength=cellnumy*cellheight+4*notch2width
		distx=(striplength-cellnumx*cellwidth)/2	
		disty=(striplength-cellnumy*cellheight)/2

		celldisty=(cellheight-notch2width-notchwidth)/2
		
		for num in range(1,cellnumx):
			y=disty-notch2width/2
			pathstring='M '+str(1)+','+str(1)
			pathstring+=' L '+str(stripwidth)+','+str(1)
			pathstring+=' L '+str(stripwidth)+','+str(y)					# Distance to corner

			for i in range(0,cellnumy):
				pathstring+=' L '+str(stripwidth-notch2depth)+','+str(y)		# Einrueckung
				pathstring+=' L '+str(stripwidth-notch2depth)+','+str(y+notch2width)	# Kerbe
				pathstring+=' L '+str(stripwidth)+','+str(y+notch2width)				# Ausrueckung
				if notchvertical:
					pathstring+=' L '+str(stripwidth)+','+str(y+notch2width+celldisty)					# Abstand
					pathstring+=' L '+str(stripwidth-notchdepth)+','+str(y+notch2width+celldisty)		# Einrueckung
					pathstring+=' L '+str(stripwidth-notchdepth)+','+str(y+notch2width+celldisty+notchwidth)	# Kerbe
					pathstring+=' L '+str(stripwidth)+','+str(y+notch2width+celldisty+notchwidth)				# Ausrueckung
				pathstring+=' L '+str(stripwidth)+','+str(y+notch2width+2*celldisty+notchwidth)				# Abstand
				y=y+notch2width+2*celldisty+notchwidth

					
			pathstring+=' L '+str(stripwidth-notch2depth)+','+str(y)		# Einrueckung
			pathstring+=' L '+str(stripwidth-notch2depth)+','+str(y+notch2width)	# Kerbe
			pathstring+=' L '+str(stripwidth)+','+str(y+notch2width)				# Ausrueckung

			pathstring+=' L '+str(stripwidth)+','+str(striplength)
			pathstring+=' L '+str(1)+','+str(striplength)							# Linke untere Ecke
			pathstring+=' L '+str(1)+','+str(1)+' z'
			
			
			strip_transform= 'translate('+str((num+1)*stripwidth+10)+','+str(1)+')'
			stripname="strip vertical short "+str(num)
			pathstring = inkex.PathElement(d=pathstring)
			pathstring.set('style',style)
			pathstring.set('inkscape:label',stripname)
			pathstring.set('transform', strip_transform)
			grp.add(pathstring)
		yield layer	

					
if __name__ == '__main__':   #pragma: no cover
    # Create effect instance and apply it.
    GridStrip_Creator().run()
    

## end of file gridstrip_creator.py ##
