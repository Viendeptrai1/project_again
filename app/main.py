# main.py
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from pathlib import Path

class SalesAnalysisApp:
    def __init__(self):
        # Setup main window
        self.root = ctk.CTk()
        self.root.title("Sales Analysis Dashboard")
        self.root.geometry("1200x800")
        
        # Load and process data
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        
    def load_data(self):
        """Load and preprocess the sales data"""
        self.df = pd.read_csv("data/raw/supermarket_sales - Sheet1.csv")
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['Month'] = self.df['Date'].dt.month
        
    def setup_ui(self):
        """Setup the main UI components"""
        # Create main containers
        self.control_frame = ctk.CTkFrame(self.root, width=250)
        self.control_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        self.graph_frame = ctk.CTkFrame(self.root)
        self.graph_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Add controls
        self.create_controls()
        
        # Create initial plot
        self.current_plot = "sales_by_category"
        self.update_plot()
        
    def create_controls(self):
        """Create control panel elements"""
        # Title
        title = ctk.CTkLabel(
            self.control_frame, 
            text="Analysis Controls",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=10, padx=10)
        
        # Plot Type Selection
        plot_label = ctk.CTkLabel(self.control_frame, text="Select Analysis:")
        plot_label.pack(pady=(10,5))
        
        self.plot_var = ctk.StringVar(value="sales_by_category")
        plot_types = {
            "Sales by Category": "sales_by_category",
            "Monthly Sales": "monthly_sales",
            "Branch Distribution": "branch_distribution",
            "Customer Analysis": "customer_analysis"
        }
        
        for text, value in plot_types.items():
            btn = ctk.CTkRadioButton(
                self.control_frame,
                text=text,
                variable=self.plot_var,
                value=value,
                command=self.update_plot
            )
            btn.pack(pady=5, padx=20, anchor="w")
        
        # Branch Filter
        branch_label = ctk.CTkLabel(self.control_frame, text="Select Branch:")
        branch_label.pack(pady=(20,5))
        
        self.branch_var = ctk.StringVar(value="All")
        branches = ["All"] + list(self.df['Branch'].unique())
        branch_dropdown = ctk.CTkOptionMenu(
            self.control_frame,
            values=branches,
            variable=self.branch_var,
            command=self.update_plot
        )
        branch_dropdown.pack(pady=5)
        
        # Update Button
        update_btn = ctk.CTkButton(
            self.control_frame,
            text="Refresh Analysis",
            command=self.update_plot
        )
        update_btn.pack(pady=20)
        
        # Stats Display
        self.stats_label = ctk.CTkLabel(
            self.control_frame,
            text="",
            wraplength=200
        )
        self.stats_label.pack(pady=20)
        
    def update_plot(self, *args):
        """Update the current plot based on selection"""
        # Clear previous plot
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        # Filter data if branch is selected
        plot_data = self.df
        if self.branch_var.get() != "All":
            plot_data = self.df[self.df['Branch'] == self.branch_var.get()]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create plot based on selection
        plot_type = self.plot_var.get()
        
        if plot_type == "sales_by_category":
            sales_by_cat = plot_data.groupby('Product line')['Total'].sum().sort_values(ascending=True)
            sales_by_cat.plot(kind='barh', ax=ax)
            ax.set_title('Sales by Product Category')
            ax.set_xlabel('Total Sales ($)')
            
            # Update stats
            top_category = sales_by_cat.index[-1]
            top_sales = sales_by_cat.iloc[-1]
            self.stats_label.configure(text=f"Top Category: {top_category}\nTotal Sales: ${top_sales:,.2f}")
            
        elif plot_type == "monthly_sales":
            monthly_sales = plot_data.groupby('Month')['Total'].sum()
            monthly_sales.plot(kind='line', marker='o', ax=ax)
            ax.set_title('Monthly Sales Trend')
            ax.set_xlabel('Month')
            ax.set_ylabel('Total Sales ($)')
            
            # Update stats
            peak_month = monthly_sales.idxmax()
            peak_sales = monthly_sales.max()
            self.stats_label.configure(text=f"Peak Month: {peak_month}\nPeak Sales: ${peak_sales:,.2f}")
            
        elif plot_type == "branch_distribution":
            plot_data.groupby('Branch')['Total'].sum().plot(kind='pie', ax=ax, autopct='%1.1f%%')
            ax.set_title('Sales Distribution by Branch')
            
            # Update stats
            branch_stats = plot_data.groupby('Branch')['Total'].agg(['sum', 'count'])
            top_branch = branch_stats['sum'].idxmax()
            self.stats_label.configure(text=f"Top Branch: {top_branch}\nTotal Sales: ${branch_stats.loc[top_branch, 'sum']:,.2f}")
            
        elif plot_type == "customer_analysis":
            sns.boxplot(data=plot_data, x='Customer type', y='Total', ax=ax)
            ax.set_title('Sales Distribution by Customer Type')
            ax.set_ylabel('Total Sales ($)')
            
            # Update stats
            cust_stats = plot_data.groupby('Customer type')['Total'].agg(['mean', 'count'])
            self.stats_label.configure(text=f"Customer Stats:\nNormal: {cust_stats.loc['Normal', 'count']}\nMember: {cust_stats.loc['Member', 'count']}")
        
        # Adjust layout
        plt.tight_layout()
        
        # Add plot to GUI
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SalesAnalysisApp()
    app.run()