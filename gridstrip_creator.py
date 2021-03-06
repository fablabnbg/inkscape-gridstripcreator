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
import simplestyle,sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex

from xml.etree import ElementTree as ET

# for printing debugging output
import gettext
_ = gettext.gettext

def printDebug(string):
	inkex.errormsg(_(string))
	

class GridStrip_Creator(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		"""
		Constructor.
		Defines options of the script.
		"""
		# Call the base class constructor.
		inkex.Effect.__init__(self)

		# Define string option "--length" with default value '0.0'.
		self.OptionParser.add_option('--length',
			action = 'store',type = 'float',
			dest = 'length',default = 230.0,
			help = 'Length of strip')
			
		# Define string option "--width" with default value '0.0'.
		self.OptionParser.add_option('--width',
			action = 'store',type = 'float',
			dest = 'width',default = 20.0,
			help = 'Width of strip')

		# Define string option "--cellheight" with default value '0.0'.
		self.OptionParser.add_option('--cellheight',
			action = 'store',type = 'float',
			dest = 'cellheight',default = 12.5,
			help = 'height of cell')
			
		# Define string option "--cellwidth" with default value '0.0'.
		self.OptionParser.add_option('--cellwidth',
			action = 'store',type = 'float',
			dest = 'cellwidth',default = 12.5,
			help = 'Width of cell')
			
		# Define string option "--scalecells" with default value False.
		self.OptionParser.add_option('--scalecells',
			action = 'store',type = 'inkbool',
			dest = 'scalecells',default = False,
			help = 'Scale cells over length')

		# Define string option "--cellnumx" with default value '0.0'.
		self.OptionParser.add_option('--cellnumx',
			action = 'store',type = 'int',
			dest = 'cellnumx',default = 11,
			help = 'Number of cells x')
			
		# Define string option "--cellnumy" with default value '0.0'.
		self.OptionParser.add_option('--cellnumy',
			action = 'store',type = 'int',
			dest = 'cellnumy',default = 10,
			help = 'Number of cells y')
			
		# Define string option "--notchdepth" with default value '0.0'.
		self.OptionParser.add_option('--notchdepth',
			action = 'store',type = 'float',
			dest = 'notchdepth',default = 1.0,
			help = 'Depth of notch')
        
		# Define string option "--notchwidth" with default value '0.0'.
		self.OptionParser.add_option('--notchwidth',
			action = 'store',type = 'float',
			dest = 'notchwidth',default = 10.0,
			help = 'Width of notch')
			
		# Define string option "--notchhorizontal" with default value False.
		self.OptionParser.add_option('--notchhorizontal',
			action = 'store',type = 'inkbool',
			dest = 'notchhorizontal',default = False,
			help = 'Make notches on horizontal strip')
 
		# Define string option "--notchvertical" with default value False.
		self.OptionParser.add_option('--notchvertical',
			action = 'store',type = 'inkbool',
			dest = 'notchvertical',default = False,
			help = 'Make notches on vertical strip')
         
		# Define string option "--notch2depth" with default value '0.0'.
		# self.OptionParser.add_option('--notch2depth',
			# action = 'store',type = 'float',
			# dest = 'notch2depth',default = 10.0,
			# help = 'Depth of notch')
        
		# Define string option "--notch2width" with default value '0.0'.
		self.OptionParser.add_option('--notch2width',
			action = 'store',type = 'float',
			dest = 'notch2width',default = 3.0,
			help = 'Width of notch')

		# Define string option "--notchxcorner" with default value False.
		self.OptionParser.add_option('--notchxcorner',
			action = 'store',type = 'inkbool',
			dest = 'notchxcorner',default = False,
			help = 'Make notches on corner of horizontal strip')
 
		# Define string option "--notchycorner" with default value False.
		self.OptionParser.add_option('--notchycorner',
			action = 'store',type = 'inkbool',
			dest = 'notchycorner',default = False,
			help = 'Make notches on corner of vertical strip')
         

			
	def effect(self):
		# Get access to main SVG document element and get its dimensions.
		svg = self.document.getroot()
		# getting the parent tag of the guide
		nv = self.document.xpath('/svg:svg/sodipodi:namedview',namespaces=inkex.NSS)[0]
		
		documentUnits = inkex.addNS('document-units', 'inkscape')
		# print  >> sys.stderr, nv.get(documentUnits)
		uunits = nv.get(documentUnits)
		message="Units="+uunits
		inkex.debug(message)

		# Get script's options value.
		stripwidth=self.unittouu(str(self.options.width)+uunits)
		striplength=self.unittouu(str(self.options.length)+uunits)

		cellheight=self.unittouu(str(self.options.cellheight)+uunits)
		cellwidth=self.unittouu(str(self.options.cellwidth)+uunits)

		scalecells=(self.options.scalecells)
		
		cellnumx=(self.options.cellnumx)
		cellnumy=(self.options.cellnumy)
		
		notchdepth=self.unittouu(str(self.options.notchdepth)+uunits)
		notchwidth=self.unittouu(str(self.options.notchwidth)+uunits)
		
		notchhorizontal=(self.options.notchhorizontal)
		notchvertical=(self.options.notchvertical)
				
#		notch2depth=self.unittouu(str(self.options.notch2depth)+uunits)
		notch2width=self.unittouu(str(self.options.notch2width)+uunits)
		
		notch2depth= stripwidth/2
		
		notchxcorner=(self.options.notchxcorner)
		notchycorner=(self.options.notchycorner)

		if scalecells:
			cellwidth=(striplength-4*notch2width)/cellnumx
			cellheight=(striplength-4*notch2width)/cellnumy
			notchxcorner=False
			notchycorner=False
		
		
		linewidth=self.unittouu(str(0.01)+uunits)

		distx=(striplength-cellnumx*cellwidth)/2	
		disty=(striplength-cellnumy*cellheight)/2
		
		celldistx=(cellwidth-notchwidth)/2
		celldisty=(cellheight-notch2width)/2

		# getting the width and height attributes of the canvas
		width  = float(self.unittouu(svg.attrib['width']))
		height = float(self.unittouu(svg.attrib['height']))

		# maxlength=max(width,height)
		# if striplength > maxlength:
			# factor=striplength/maxlength+1

		inkex.debug("document width="+str(self.uutounit(width,uunits)))
		inkex.debug("document height="+str(self.uutounit(height,uunits)))
		
		inkex.debug("strip length="+str(self.uutounit(striplength,uunits)))
		inkex.debug("strip width="+str(self.uutounit(stripwidth,uunits)))

		inkex.debug("cell width="+str(self.uutounit(cellwidth,uunits)))
		inkex.debug("cell height="+str(self.uutounit(cellheight,uunits)))

		inkex.debug("Number of cells horizontal="+str(cellnumx))
		inkex.debug("Number of cells vertical  ="+str(cellnumy))
				
		inkex.debug("Depth of extra notch="+str(self.uutounit(notchdepth,uunits)))
		inkex.debug("Width of extra notch="+str(self.uutounit(notchwidth,uunits)))

		inkex.debug("Depth of notch for grid="+str(self.uutounit(notchdepth,uunits)))
		inkex.debug("Width of notch for grid="+str(self.uutounit(notchwidth,uunits)))

		inkex.debug("distx="+str(self.uutounit(distx,uunits)))
		inkex.debug("disty="+str(self.uutounit(disty,uunits)))

		inkex.debug("celldistx="+str(self.uutounit(celldistx,uunits)))
		inkex.debug("celldisty="+str(self.uutounit(celldisty,uunits)))
		
		
		parent = self.current_layer
		layername=''
		if notchhorizontal:
			layername=layername+'VLED '
		if notchvertical:
			layername=layername+'HLED '
		
		# Create a new layer
		layer = inkex.etree.SubElement(svg,'g')
		layer.set(inkex.addNS('label', 'inkscape'),layername+'Long strips')
		layer.set(inkex.addNS('groupmode','inkscape'), 'layer')
		
		
		grp_name = 'group_horizontal_strip_long'
		grp_attribs = {inkex.addNS('label','inkscape'):grp_name}
		grp = inkex.etree.SubElement(layer, 'g', grp_attribs) #the group to put everything in

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
			strip_attribs = {'style':simplestyle.formatStyle(style),
								inkex.addNS('label','inkscape'):"strip horizontal long",
								'transform': strip_transform,
								'd':pathstring}
			inkex.etree.SubElement(grp, inkex.addNS('path','svg'), strip_attribs )
		
		
		celldisty=(cellheight-notch2width-notchwidth)/2

		grp_name = 'group_vertical_strip_long'
		grp_attribs = {inkex.addNS('label','inkscape'):grp_name}
		grp = inkex.etree.SubElement(layer, 'g', grp_attribs) #the group to put everything in
		

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
			strip_attribs = {'style':simplestyle.formatStyle(style),
								inkex.addNS('label','inkscape'):"strip vertical long",
								'transform': strip_transform,
								'd':pathstring}
			inkex.etree.SubElement(grp, inkex.addNS('path','svg'), strip_attribs )
		
		# Create a new layer
		layer = inkex.etree.SubElement(svg,'g')
		layer.set(inkex.addNS('label', 'inkscape'), layername+'Horizontal strips short')
		layer.set(inkex.addNS('groupmode','inkscape'), 'layer')

		grp_name = 'group horizontal_strip_short'
		grp_attribs = {inkex.addNS('label','inkscape'):grp_name}
		grp = inkex.etree.SubElement(layer, 'g', grp_attribs) #the group to put everything in
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
			stripname="strip horizontal short"+str(num)
			strip_attribs = {'style':simplestyle.formatStyle(style),
								inkex.addNS('label','inkscape'):stripname,
								'transform': strip_transform,
								'd':pathstring}
			inkex.etree.SubElement(grp, inkex.addNS('path','svg'), strip_attribs )

			
		# Create a new layer
		layer = inkex.etree.SubElement(svg,'g')
		layer.set(inkex.addNS('label', 'inkscape'), layername+'Vertical strips short')
		layer.set(inkex.addNS('groupmode','inkscape'), 'layer')

		grp_name = 'group vertical_strip_short'
		grp_attribs = {inkex.addNS('label','inkscape'):grp_name}
		grp = inkex.etree.SubElement(layer, 'g', grp_attribs) #the group to put everything in
		
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
			stripname="strip vertical short"+str(num)
			strip_attribs = {'style':simplestyle.formatStyle(style),
								inkex.addNS('label','inkscape'):stripname,
								'transform': strip_transform,
								'd':pathstring}
			inkex.etree.SubElement(grp, inkex.addNS('path','svg'), strip_attribs )

					
if __name__ == '__main__':   #pragma: no cover
    # Create effect instance and apply it.
    effect = GridStrip_Creator()
    effect.affect()

## end of file gridstrip_creator.py ##
