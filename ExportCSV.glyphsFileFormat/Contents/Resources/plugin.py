# encoding: utf-8

###########################################################################################################
#
#
#	File Format Plugin
#	Implementation for exporting fonts through the Export dialog
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/File%20Format
#
#	For help on the use of Xcode:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *


class ExportCSV(FileFormatPlugin):
	allMasters = 'com.mekkablue.csvexport.allMasters'
	
	# Definitions of IBOutlets
	
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()
	
	# Example variables. You may delete them
	allMastersCheckBox = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.name = "CSV"
		self.icon = 'ExportIcon'
		self.toolbarPosition = 100
		
		# Load .nib dialog (with .extension)
		self.loadNib('IBdialog', __file__)


	@objc.python_method
	def start(self):
		
		# Init user preferences if not existent and set default value
		Glyphs.registerDefault(self.allMasters, True)
		
		# Set initial state of checkboxes according to user variables
		self.allMastersCheckBox.setState_(Glyphs.defaults[self.allMasters])


	# Example function. You may delete it
	@objc.IBAction
	def setAllMasters_(self, sender):
		Glyphs.defaults[self.allMasters] = bool(sender.intValue())


	@objc.python_method
	def export(self, font):
		# Ask for export destination and write the file:
		title = "Choose export destination"
		proposedFilename = f"Glyph info for {font.familyName}"
		fileTypes = ['csv']
		filepath = GetSaveFile(title, proposedFilename, fileTypes)


		if filepath:
			import csv, os

			processAllMasters = bool(Glyphs.defaults[self.allMasters])
			if processAllMasters:
				masterIDs = tuple([m.id for m in font.masters])
			else:
				masterIDs = (font.selectedFontMaster.id,)
			
			for masterID in masterIDs:
				master = font.fontMasterForId_(masterID)
				fullFilepath = f"{filepath.stringByDeletingDotSuffix()}, {master.name}{filepath.dotSuffix()}"

				with open(fullFilepath, 'w') as csvFile:
					fieldnames = ['ID', 'Name', 'Export', 'Unicode', 'Script', 'Category', 'Subcategory', 'Case', 'Width', 'LSB', 'RSB', 'Left Group', 'Right Group', 'Last Changed', 'Vertical Width', 'TSB', 'BSB', 'Note', 'Components', 'Character']
					writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
					writer.writeheader()
					for g in font.glyphs:
						l = g.layers[masterID]
						writeDict = {}
						writeDict['ID'] = g.glyphId()
						writeDict['Name'] = g.name
						writeDict['Export'] = g.export
						writeDict['Unicode'] = g.unicode
						writeDict['Script'] = g.script
						writeDict['Category'] = g.category
						writeDict['Subcategory'] = g.subCategory
						writeDict['Case'] = ('none', 'upper', 'lower', 'smallcap', 'minor')[g.case]
						writeDict['Width'] = l.width
						writeDict['LSB'] = l.LSB
						writeDict['RSB'] = l.RSB
						writeDict['Left Group'] = g.leftKerningGroup
						writeDict['Right Group'] = g.rightKerningGroup
						writeDict['Last Changed'] = g.lastChange
						writeDict['Vertical Width'] = l.vertWidth
						writeDict['TSB'] = l.TSB
						writeDict['BSB'] = l.BSB
						writeDict['Note'] = g.note
						writeDict['Components'] = ', '.join(c.name for c in l.components)
						writeDict['Character'] = g.charString()
						writer.writerow(writeDict)
			
			return (True, f'The export of ‘{os.path.basename(filepath)}’ was successful.')
		
		else:
			return (False, 'No file chosen')


	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
