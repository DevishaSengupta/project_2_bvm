import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from datetime import datetime
import threading
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1200x800")
        
        # Database connection parameters
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Devisha@22',
            'database': 'inventory',
        }
        
        self.connection = None
        self.cursor = None
        
        # Initialize GUI
        self.setup_gui()
        self.connect_to_database()
        self.refresh_all_data()
    
    def connect_to_database(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            messagebox.showinfo("Success", "Connected to database successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            # For demo purposes, we'll continue without connection
            self.connection = None
            self.cursor = None
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_boxes_tab()
        self.create_items_tab()
        self.create_subcomartments_tab()
        self.create_transactions_tab()
        self.create_operations_tab()
    
    def create_boxes_tab(self):
        """Create Boxes management tab"""
        self.boxes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.boxes_frame, text="Boxes")
        
        # Controls frame
        controls_frame = ttk.Frame(self.boxes_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Add Box", command=self.add_box).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Delete Box", command=self.delete_box).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Refresh", command=self.refresh_boxes).pack(side=tk.LEFT, padx=5)
        
        # Treeview for boxes
        self.boxes_tree = ttk.Treeview(self.boxes_frame, columns=("ID", "Column", "Row"), show="headings")
        self.boxes_tree.heading("ID", text="Box ID")
        self.boxes_tree.heading("Column", text="Column Name")
        self.boxes_tree.heading("Row", text="Row Number")
        
        scrollbar_boxes = ttk.Scrollbar(self.boxes_frame, orient=tk.VERTICAL, command=self.boxes_tree.yview)
        self.boxes_tree.configure(yscrollcommand=scrollbar_boxes.set)
        
        self.boxes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_boxes.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_items_tab(self):
        """Create Items management tab"""
        self.items_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.items_frame, text="Items")
        
        # Controls frame
        controls_frame = ttk.Frame(self.items_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Add Item", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Delete Item", command=self.delete_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Refresh", command=self.refresh_items).pack(side=tk.LEFT, padx=5)
        
        # Treeview for items
        self.items_tree = ttk.Treeview(self.items_frame, columns=("ID", "Name", "Description", "Added On"), show="headings")
        self.items_tree.heading("ID", text="Item ID")
        self.items_tree.heading("Name", text="Name")
        self.items_tree.heading("Description", text="Description")
        self.items_tree.heading("Added On", text="Added On")
        
        scrollbar_items = ttk.Scrollbar(self.items_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar_items.set)
        
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_items.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_subcomartments_tab(self):
        """Create SubCompartments management tab"""
        self.subcom_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.subcom_frame, text="Sub Compartments")
        
        # Controls frame
        controls_frame = ttk.Frame(self.subcom_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Add SubCompartment", command=self.add_subcompartment).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Update Status", command=self.update_subcom_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Refresh", command=self.refresh_subcompartments).pack(side=tk.LEFT, padx=5)
        
        # Treeview for subcompartments
        self.subcom_tree = ttk.Treeview(self.subcom_frame, columns=("Place", "Box ID", "Sub ID", "Item ID", "Status"), show="headings")
        self.subcom_tree.heading("Place", text="Place")
        self.subcom_tree.heading("Box ID", text="Box ID")
        self.subcom_tree.heading("Sub ID", text="Sub ID")
        self.subcom_tree.heading("Item ID", text="Item ID")
        self.subcom_tree.heading("Status", text="Status")
        
        scrollbar_subcom = ttk.Scrollbar(self.subcom_frame, orient=tk.VERTICAL, command=self.subcom_tree.yview)
        self.subcom_tree.configure(yscrollcommand=scrollbar_subcom.set)
        
        self.subcom_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_subcom.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_transactions_tab(self):
        """Create Transactions management tab"""
        self.trans_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.trans_frame, text="Transactions")
        
        # Controls frame
        controls_frame = ttk.Frame(self.trans_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Process Purchase", command=self.process_purchase).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Process Return", command=self.process_return).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Refresh", command=self.refresh_transactions).pack(side=tk.LEFT, padx=5)
        
        # Auto-refresh checkbox
        self.auto_refresh_var = tk.BooleanVar()
        ttk.Checkbutton(controls_frame, text="Auto Refresh (5s)", 
                       variable=self.auto_refresh_var, 
                       command=self.toggle_auto_refresh).pack(side=tk.LEFT, padx=20)
        
        # Treeview for transactions (assuming basic structure)
        self.trans_tree = ttk.Treeview(self.trans_frame, columns=("ID", "Type", "Item", "Quantity", "Timestamp"), show="headings")
        self.trans_tree.heading("ID", text="Transaction ID")
        self.trans_tree.heading("Type", text="Type")
        self.trans_tree.heading("Item", text="Item")
        self.trans_tree.heading("Quantity", text="Quantity")
        self.trans_tree.heading("Timestamp", text="Timestamp")
        
        scrollbar_trans = ttk.Scrollbar(self.trans_frame, orient=tk.VERTICAL, command=self.trans_tree.yview)
        self.trans_tree.configure(yscrollcommand=scrollbar_trans.set)
        
        self.trans_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_trans.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.auto_refresh_active = False
    
    def create_operations_tab(self):
        """Create Operations tab with button-based actions"""
        self.ops_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ops_frame, text="Operations")
        
        # Main operations frame
        main_ops_frame = ttk.LabelFrame(self.ops_frame, text="Product Operations")
        main_ops_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Button frame
        button_frame = ttk.Frame(main_ops_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Product", command=self.show_add_product_options, 
                   width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Retrieve Product", command=self.show_retrieve_product_options, 
                   width=20).pack(side=tk.LEFT, padx=10)
        
        # Dynamic content frame (will show different options based on button clicked)
        self.dynamic_frame = ttk.LabelFrame(self.ops_frame, text="Options")
        self.dynamic_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results display
        self.results_frame = ttk.LabelFrame(self.ops_frame, text="Results")
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.results_text = tk.Text(self.results_frame, height=10, width=80, state=tk.DISABLED)
        scrollbar_results = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar_results.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_results.pack(side=tk.RIGHT, fill=tk.Y)

    def clear_dynamic_frame(self):
        """Clear the dynamic frame"""
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

    def show_add_product_options(self):
        """Show options for adding a product"""
        self.clear_dynamic_frame()
        self.dynamic_frame.config(text="Add Product Options")
        
        # Product type selection
        ttk.Label(self.dynamic_frame, text="Select Product Type:").pack(pady=5)
        
        self.product_type_var = tk.StringVar()
        product_types = self.get_available_product_types()
        
        if not product_types:
            ttk.Label(self.dynamic_frame, text="No products available. Add items first in Items tab.").pack(pady=10)
            return
        
        # Create radio buttons for product types
        for product_type in product_types:
            ttk.Radiobutton(self.dynamic_frame, text=f"{product_type[1]} (ID: {product_type[0]})", 
                           variable=self.product_type_var, value=product_type[0]).pack(anchor=tk.W, padx=20)
        
        # Additional options frame
        options_frame = ttk.Frame(self.dynamic_frame)
        options_frame.pack(pady=10)
        
        # Box selection
        ttk.Label(options_frame, text="Box ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.add_box_id_var = tk.StringVar()
        box_ids = self.get_available_box_ids()
        box_combo = ttk.Combobox(options_frame, textvariable=self.add_box_id_var, values=box_ids, state="readonly")
        box_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Sub compartment ID
        ttk.Label(options_frame, text="Sub Compartment ID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.sub_comp_id_var = tk.StringVar()
        ttk.Entry(options_frame, textvariable=self.sub_comp_id_var, width=20).grid(row=1, column=1, padx=5, pady=5)
        
        # Status section removed - will automatically set to 'available'
        
        # Add button
        ttk.Button(self.dynamic_frame, text="Add Product to Storage", 
                   command=self.execute_add_product).pack(pady=10)

    def show_retrieve_product_options(self):
        """Show options for retrieving a product"""
        self.clear_dynamic_frame()
        self.dynamic_frame.config(text="Retrieve Product Options")
        
        # Get available products
        available_products = self.get_available_products_for_retrieval()
        
        if not available_products:
            ttk.Label(self.dynamic_frame, text="No products available for retrieval.").pack(pady=10)
            return
        
        ttk.Label(self.dynamic_frame, text="Select Product Type to Retrieve:").pack(pady=5)
        
        self.retrieve_product_var = tk.StringVar()
        
        # Create radio buttons for available products
        for product in available_products:
            product_info = f"{product[1]} (Available: {product[2]})"
            ttk.Radiobutton(self.dynamic_frame, text=product_info, 
                           variable=self.retrieve_product_var, value=product[0]).pack(anchor=tk.W, padx=20)
        
        # Quantity frame
        qty_frame = ttk.Frame(self.dynamic_frame)
        qty_frame.pack(pady=10)
        
        ttk.Label(qty_frame, text="Quantity to Retrieve:").pack(side=tk.LEFT, padx=5)
        self.retrieve_qty_var = tk.StringVar(value="1")
        ttk.Entry(qty_frame, textvariable=self.retrieve_qty_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Retrieve button
        ttk.Button(self.dynamic_frame, text="Retrieve Product", 
                   command=self.execute_retrieve_product).pack(pady=10)

    def get_available_product_types(self):
        """Get all available product types from Items table"""
        if not self.connection:
            return []
        
        query = "SELECT item_id, name FROM Items ORDER BY name"
        results = self.execute_query(query)
        return results if results else []

    def get_available_box_ids(self):
        """Get all available box IDs"""
        if not self.connection:
            return []
        
        query = "SELECT box_id FROM Boxes ORDER BY box_id"
        results = self.execute_query(query)
        return [str(row[0]) for row in results] if results else []

    def get_available_products_for_retrieval(self):
        """Get products available for retrieval with counts"""
        if not self.connection:
            return []
        
        query = """
        SELECT i.item_id, i.name, COUNT(*) as available_count
        FROM Items i
        JOIN SubCompartments sc ON i.item_id = sc.item_id
        WHERE sc.status = 'Occupied'
        GROUP BY i.item_id, i.name
        ORDER BY i.name
        """
        results = self.execute_query(query)
        return results if results else []

    def execute_add_product(self):
        """Execute add product operation with place occupancy check"""
        if not self.product_type_var.get():
            messagebox.showwarning("Warning", "Please select a product type")
            return
        
        if not self.add_box_id_var.get() or not self.sub_comp_id_var.get():
            messagebox.showwarning("Warning", "Please fill in all required fields")
            return
        
        try:
            item_id = int(self.product_type_var.get())
            box_id = self.add_box_id_var.get().strip()
            sub_id = self.sub_comp_id_var.get().strip()
            
            # Validate that sub_id is not empty after stripping
            if not sub_id:
                messagebox.showerror("Error", "Sub Compartment ID cannot be empty")
                return
            
            # Generate subcom_place
            subcom_place = f"{box_id}{sub_id}"
            
            # Check if this place already exists (is occupied)
            check_query = "SELECT status FROM SubCompartments WHERE subcom_place = %s"
            result = self.execute_query(check_query, (subcom_place,))
            
            if result:
                current_status = result[0][0]
                if current_status == 'Occupied':
                    messagebox.showerror("Error", f"SubCompartment {subcom_place} is already OCCUPIED")
                    return
                elif current_status == 'Empty':
                    # Update the empty place to occupied with new item
                    update_query = """
                    UPDATE SubCompartments 
                    SET item_id = %s, status = 'Occupied' 
                    WHERE subcom_place = %s
                    """
                    if self.execute_query(update_query, (item_id, subcom_place)):
                        # Get item name for display
                        item_query = "SELECT name FROM Items WHERE item_id = %s"
                        item_result = self.execute_query(item_query, (item_id,))
                        item_name = item_result[0][0] if item_result else "Unknown"
                        
                        success_msg = f"Product added successfully!\n"
                        success_msg += f"Item: {item_name}\n"
                        success_msg += f"Location: {subcom_place}\n"
                        success_msg += f"Status: Occupied\n"
                        success_msg += f"Note: Updated empty place to occupied"
                        
                        self.display_results(success_msg)
                        messagebox.showinfo("Success", "Product added successfully!")
                        self.refresh_subcompartments()
                    return
            
            else:
                # Place doesn't exist, create new entry with 'Occupied' status
                query = """
                INSERT INTO SubCompartments (subcom_place, box_id, sub_id, item_id, status) 
                VALUES (%s, %s, %s, %s, 'Occupied')
                """
                
                if self.execute_query(query, (subcom_place, box_id, sub_id, item_id)):
                    # Get item name for display
                    item_query = "SELECT name FROM Items WHERE item_id = %s"
                    item_result = self.execute_query(item_query, (item_id,))
                    item_name = item_result[0][0] if item_result else "Unknown"
                    
                    success_msg = f"Product added successfully!\n"
                    success_msg += f"Item: {item_name}\n"
                    success_msg += f"Location: {subcom_place}\n"
                    success_msg += f"Status: Occupied\n"
                    success_msg += f"Note: Added to new place"
                    
                    self.display_results(success_msg)
                    messagebox.showinfo("Success", "Product added successfully!")
                    self.refresh_subcompartments()
    
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input values: {str(ve)}")
            print(f"ValueError details: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding product: {e}")
            print(f"Exception details: {e}")

    def execute_retrieve_product(self):
        """Execute retrieve product operation - column-wise priority"""
        # Mapping between radio button values and item IDs
        product_mapping = {
            "Bearing": 1,
            "Gear": 2,
            "Bolt Set": 3
        }

        # Get the selected product type
        selected_product = self.retrieve_product_var.get()
        if not selected_product:
            logging.warning("No product type selected")
            messagebox.showwarning("Warning", "Please select a product type")
            return
        print(f"Selected product type: {selected_product}")
        # Map the selected product to its corresponding item_id
        item_id = selected_product
        if not item_id:
            logging.error(f"Invalid product type selected: {selected_product}")
            messagebox.showerror("Error", "Invalid product type selected")
            return

        try:
            logging.info(f"Retrieving product with item_id: {item_id}")
            # Execute the query using the mapped item_id
            query = "SELECT * FROM Items WHERE item_id = %s"
            result = self.execute_query(query, (item_id,))
            
            # Display the result (you can customize this part)
            if result:
                logging.info(f"Product retrieved successfully: {result}")
                messagebox.showinfo("Product Retrieved", f"Product details: {result}")
            else:
                logging.info(f"No product found for item_id: {item_id}")
                messagebox.showinfo("No Product Found", "No product found for the selected type")
        except Exception as e:
            logging.error(f"Failed to retrieve product: {e}")
            messagebox.showerror("Error", f"Failed to retrieve product: {e}")

    def process_purchase(self):
        """Process a purchase transaction"""
        dialog = TransactionDialog(self.root, "Process Purchase")
        if dialog.result:
            item_id, quantity = dialog.result
            
            # Start transaction
            try:
                self.cursor.execute("START TRANSACTION")
                
                # Check item availability in subcompartments
                check_query = """
                SELECT COUNT(*) FROM SubCompartments 
                WHERE item_id = %s AND status = 'Occupied'
                """
                self.cursor.execute(check_query, (item_id,))
                available_count = self.cursor.fetchone()[0]
                
                if available_count < quantity:
                    messagebox.showerror("Error", f"Only {available_count} items available")
                    self.cursor.execute("ROLLBACK")
                    return
                
                # Update subcompartments status to Empty
                update_query = """
                UPDATE SubCompartments 
                SET status = 'Empty', item_id = NULL 
                WHERE item_id = %s AND status = 'Occupied' 
                LIMIT %s
                """
                self.cursor.execute(update_query, (item_id, quantity))
                
                # Insert transaction record
                trans_query = """
                INSERT INTO Transactions (transaction_type, item_id, quantity, timestamp) 
                VALUES ('purchase', %s, %s, %s)
                """
                self.cursor.execute(trans_query, (item_id, quantity, datetime.now()))
                
                self.connection.commit()
                messagebox.showinfo("Success", "Purchase processed successfully!")
                
                # Refresh all relevant data
                self.refresh_subcompartments()
                self.refresh_transactions()
                
            except mysql.connector.Error as err:
                self.cursor.execute("ROLLBACK")
                messagebox.showerror("Transaction Error", f"Error processing purchase: {err}")

    def process_return(self):
        """Process a return transaction"""
        dialog = TransactionDialog(self.root, "Process Return")
        if dialog.result:
            item_id, quantity = dialog.result
            
            try:
                self.cursor.execute("START TRANSACTION")
                
                # Update subcompartments status back to Occupied
                update_query = """
                UPDATE SubCompartments 
                SET status = 'Occupied', item_id = %s 
                WHERE status = 'Empty' 
                LIMIT %s
                """
                self.cursor.execute(update_query, (item_id, quantity))
                
                if self.cursor.rowcount < quantity:
                    messagebox.showwarning("Warning", f"Only {self.cursor.rowcount} items could be returned")
                
                # Insert transaction record
                trans_query = """
                INSERT INTO Transactions (transaction_type, item_id, quantity, timestamp) 
                VALUES ('return', %s, %s, %s)
                """
                self.cursor.execute(trans_query, (item_id, self.cursor.rowcount, datetime.now()))
                
                self.connection.commit()
                messagebox.showinfo("Success", "Return processed successfully!")
                
                # Refresh all relevant data
                self.refresh_subcompartments()
                self.refresh_transactions()
                
            except mysql.connector.Error as err:
                self.cursor.execute("ROLLBACK")
                messagebox.showerror("Transaction Error", f"Error processing return: {err}")
    
    def refresh_boxes(self):
        """Refresh boxes data"""
        self.boxes_tree.delete(*self.boxes_tree.get_children())
        if self.connection:
            results = self.execute_query("SELECT * FROM Boxes")
            if results:
                for row in results:
                    self.boxes_tree.insert("", tk.END, values=row)
    
    def refresh_items(self):
        """Refresh items data"""
        self.items_tree.delete(*self.items_tree.get_children())
        if self.connection:
            results = self.execute_query("SELECT * FROM Items")
            if results:
                for row in results:
                    self.items_tree.insert("", tk.END, values=row)
    
    def refresh_subcompartments(self):
        """Refresh subcompartments data"""
        self.subcom_tree.delete(*self.subcom_tree.get_children())
        if self.connection:
            results = self.execute_query("SELECT * FROM SubCompartments")
            if results:
                for row in results:
                    self.subcom_tree.insert("", tk.END, values=row)
    
    def refresh_transactions(self):
        """Refresh transactions data"""
        self.trans_tree.delete(*self.trans_tree.get_children())
        if self.connection:
            # Assuming your Transactions table has these columns
            results = self.execute_query("SELECT * FROM Transactions ORDER BY timestamp DESC LIMIT 100")
            if results:
                for row in results:
                    self.trans_tree.insert("", tk.END, values=row)
    
    def refresh_all_data(self):
        """Refresh all data in all tabs"""
        self.refresh_boxes()
        self.refresh_items()
        self.refresh_subcompartments()
        self.refresh_transactions()
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh for transactions"""
        if self.auto_refresh_var.get():
            self.auto_refresh_active = True
            self.auto_refresh_thread()
        else:
            self.auto_refresh_active = False
    
    def auto_refresh_thread(self):
        """Auto-refresh thread for real-time updates"""
        if self.auto_refresh_active:
            self.refresh_transactions()
            self.root.after(5000, self.auto_refresh_thread)
    
    def execute_custom_query(self):
        """Execute custom SQL query"""
        query = self.query_text.get("1.0", tk.END).strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a query")
            return
        
        try:
            if query.upper().startswith('SELECT'):
                results = self.execute_query(query)
                if results:
                    self.results_text.delete("1.0", tk.END)
                    for row in results:
                        self.results_text.insert(tk.END, f"{row}\n")
                else:
                    self.results_text.delete("1.0", tk.END)
                    self.results_text.insert(tk.END, "No results found or query failed")
            else:
                if self.execute_query(query):
                    self.results_text.delete("1.0", tk.END)
                    self.results_text.insert(tk.END, "Query executed successfully")
                    self.refresh_all_data()
                else:
                    self.results_text.delete("1.0", tk.END)
                    self.results_text.insert(tk.END, "Query failed")
        except Exception as e:
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(tk.END, f"Error: {e}")
    
    def add_box(self):
        """Add a new box"""
        dialog = BoxDialog(self.root, "Add Box")
        if dialog.result:
            column_name, row_number = dialog.result
            query = "INSERT INTO Boxes (column_name, row_number) VALUES (%s, %s)"
            if self.execute_query(query, (column_name, row_number)):
                messagebox.showinfo("Success", "Box added successfully!")
                self.refresh_boxes()

    def delete_box(self):
        """Delete selected box"""
        selected = self.boxes_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a box to delete")
            return
        
        item = self.boxes_tree.item(selected[0])
        box_id = item['values'][0]
        
        if messagebox.askyesno("Confirm", f"Delete box with ID {box_id}?"):
            query = "DELETE FROM Boxes WHERE box_id = %s"
            if self.execute_query(query, (box_id,)):
                messagebox.showinfo("Success", "Box deleted successfully!")
                self.refresh_boxes()

    def add_item(self):
        """Add a new item"""
        dialog = ItemDialog(self.root, "Add Item")
        if dialog.result:
            name, description = dialog.result
            query = "INSERT INTO Items (name, description, added_on) VALUES (%s, %s, %s)"
            if self.execute_query(query, (name, description, datetime.now())):
                messagebox.showinfo("Success", "Item added successfully!")
                self.refresh_items()

    def delete_item(self):
        """Delete selected item"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        item = self.items_tree.item(selected[0])
        item_id = item['values'][0]
        
        if messagebox.askyesno("Confirm", f"Delete item with ID {item_id}?"):
            query = "DELETE FROM Items WHERE item_id = %s"
            if self.execute_query(query, (item_id,)):
                messagebox.showinfo("Success", "Item deleted successfully!")
                self.refresh_items()

    def add_subcompartment(self):
        """Add a new subcompartment"""
        dialog = SubCompartmentDialog(self.root, "Add SubCompartment")
        if dialog.result:
            box_id, sub_id, item_id, status = dialog.result
            subcom_place = f"{box_id}-{sub_id}"
            
            query = "INSERT INTO SubCompartments (subcom_place, box_id, sub_id, item_id, status) VALUES (%s, %s, %s, %s, %s)"
            if self.execute_query(query, (subcom_place, box_id, sub_id, item_id, status)):
                messagebox.showinfo("Success", "SubCompartment added successfully!")
                self.refresh_subcompartments()

    def update_subcom_status(self):
        """Update status of selected subcompartment"""
        selected = self.subcom_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a subcompartment to update")
            return
        
        item = self.subcom_tree.item(selected[0])
        subcom_place = item['values'][0]
        current_status = item['values'][4]
        
        # Toggle status between Empty and Occupied
        new_status = "Empty" if current_status == "Occupied" else "Occupied"
        
        query = "UPDATE SubCompartments SET status = %s WHERE subcom_place = %s"
        if self.execute_query(query, (new_status, subcom_place)):
            messagebox.showinfo("Success", f"Status updated to {new_status}")
            self.refresh_subcompartments()

    def __del__(self):
        """Cleanup database connection"""
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        """Execute SQL query safely"""
        if not self.connection:
            messagebox.showerror("Error", "No database connection")
            return None
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                result = self.cursor.fetchall()
                return result
            else:
                self.connection.commit()
                return True
        except mysql.connector.Error as err:
            messagebox.showerror("SQL Error", f"Error executing query: {err}")
            return None

    def display_results(self, message):
        """Display results in the results text area"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", message)
        self.results_text.config(state=tk.DISABLED)

# Dialog classes for data entry
class BoxDialog:
    def __init__(self, parent, title):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Column name
        ttk.Label(self.dialog, text="Column Name:").pack(pady=5)
        self.column_entry = ttk.Entry(self.dialog, width=30)
        self.column_entry.pack(pady=5)
        
        # Row number
        ttk.Label(self.dialog, text="Row Number:").pack(pady=5)
        self.row_entry = ttk.Entry(self.dialog, width=30)
        self.row_entry.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        self.dialog.wait_window()
    
    def ok_clicked(self):
        column_name = self.column_entry.get().strip()
        row_number = self.row_entry.get().strip()
        
        if column_name and row_number:
            try:
                row_number = int(row_number)
                self.result = (column_name, row_number)
                self.dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Row number must be a valid integer")
        else:
            messagebox.showerror("Error", "Please fill all fields")

class ItemDialog:
    def __init__(self, parent, title):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Name
        ttk.Label(self.dialog, text="Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self.dialog, width=40)
        self.name_entry.pack(pady=5)
        
        # Description
        ttk.Label(self.dialog, text="Description:").pack(pady=5)
        self.desc_entry = tk.Text(self.dialog, width=40, height=4)
        self.desc_entry.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        self.dialog.wait_window()
    
    def ok_clicked(self):
        name = self.name_entry.get().strip()
        description = self.desc_entry.get("1.0", tk.END).strip()
        
        if name:
            self.result = (name, description)
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Please enter item name")

class SubCompartmentDialog:
    def __init__(self, parent, title):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Box ID
        ttk.Label(self.dialog, text="Box ID:").pack(pady=5)
        self.box_entry = ttk.Entry(self.dialog, width=30)
        self.box_entry.pack(pady=5)
        
        # Sub ID
        ttk.Label(self.dialog, text="Sub ID:").pack(pady=5)
        self.sub_entry = ttk.Entry(self.dialog, width=30)
        self.sub_entry.pack(pady=5)
        
        # Item ID
        ttk.Label(self.dialog, text="Item ID:").pack(pady=5)
        self.item_entry = ttk.Entry(self.dialog, width=30)
        self.item_entry.pack(pady=5)
        
        # Status - only Empty or Occupied
        ttk.Label(self.dialog, text="Status:").pack(pady=5)
        self.status_combo = ttk.Combobox(self.dialog, values=["Empty", "Occupied"], width=27)
        self.status_combo.set("Empty")
        self.status_combo.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        self.dialog.wait_window()
    
    def ok_clicked(self):
        box_id = self.box_entry.get().strip()
        sub_id = self.sub_entry.get().strip()
        item_id = self.item_entry.get().strip()
        status = self.status_combo.get()
        
        if box_id and sub_id and status:
            try:
                box_id = int(box_id)
                # Only require item_id if status is Occupied
                if status == "Occupied" and not item_id:
                    messagebox.showerror("Error", "Item ID is required for Occupied status")
                    return
                elif status == "Empty":
                    item_id = None
                else:
                    item_id = int(item_id)
                
                self.result = (box_id, sub_id, item_id, status)
                self.dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Box ID and Item ID must be valid integers")
        else:
            messagebox.showerror("Error", "Please fill all required fields")

class TransactionDialog:
    def __init__(self, parent, title):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Item ID
        ttk.Label(self.dialog, text="Item ID:").pack(pady=5)
        self.item_entry = ttk.Entry(self.dialog, width=30)
        self.item_entry.pack(pady=5)
        
        # Quantity
        ttk.Label(self.dialog, text="Quantity:").pack(pady=5)
        self.quantity_entry = ttk.Entry(self.dialog, width=30)
        self.quantity_entry.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        self.dialog.wait_window()
    
    def ok_clicked(self):
        item_id = self.item_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        
        if item_id and quantity:
            try:
                item_id = int(item_id)
                quantity = int(quantity)
                if quantity > 0:
                    self.result = (item_id, quantity)
                    self.dialog.destroy()
                else:
                    messagebox.showerror("Error", "Quantity must be greater than 0")
            except ValueError:
                messagebox.showerror("Error", "Item ID and Quantity must be valid integers")
        else:
            messagebox.showerror("Error", "Please fill all fields")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()