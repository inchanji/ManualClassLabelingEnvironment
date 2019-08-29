from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

BTN_MIN_WIDTH = 120


class ActionTabs(QTabWidget):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		
		self.extab = exTab(self)
		#self.adjustment_tab = AdjustingTab(self)
		#self.modification_tab = ModificationTab(self)
		#self.rotation_tab = RotationTab(self)
		
		self.addTab(self.extab, "ex tab")
		#self.addTab(self.adjustment_tab, "Adjusting")
		#self.addTab(self.modification_tab, "Modification")
		#self.addTab(self.rotation_tab, "Rotation")

		self.setMaximumHeight(190)		







class exTab(QWidget):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		
		self.main_layout = QHBoxLayout()
		self.main_layout.setAlignment(Qt.AlignCenter)
		self.setLayout(self.main_layout)
