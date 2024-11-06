import customtkinter as ctk
from .control_panel import ControlPanel
from .display_panel import DisplayPanel

class GUIManager:
    def __init__(self, root):
        self.root = root
        self.control_panel = None
        self.display_panel = None
        
    def setup_gui(self):
        """Setup main GUI layout"""
        self.root.title("Sales Analysis Dashboard")
        self.root.geometry("1200x800")
        self._create_panels()
        self._setup_bindings()
        
    def _create_panels(self):
        """Create control and display panels"""
        self.control_panel = ControlPanel(self.root)
        self.display_panel = DisplayPanel(self.root)
        
    def _setup_bindings(self):
        """Setup event bindings"""
        pass