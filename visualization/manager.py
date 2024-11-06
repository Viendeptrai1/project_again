import matplotlib.pyplot as plt
from .plotters import Plotter
from .exporters import Exporter

class VisualizationManager:
    def __init__(self, data):
        self.data = data
        self.plotter = Plotter(data)
        self.exporter = Exporter()
        
    def create_plot(self, plot_type):
        """Create plot based on type"""
        return self.plotter.create_plot(plot_type)
        
    def export_plot(self, figure, format="png"):
        """Export plot to file"""
        self.exporter.export_plot(figure, format)
