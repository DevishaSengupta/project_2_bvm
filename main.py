import tkinter as tk
from tkinter import ttk, messagebox

class RoomDialog:
    def __init__(self, parent, title, floor="", quantity=""):
        self.result = None
        dlg = tk.Toplevel(parent, bg="#d0e7ff")
        dlg.title(title)
        dlg.grab_set()

        ttk.Label(dlg, text="Floor:").pack(pady=5)
        self.floor = ttk.Entry(dlg)
        self.floor.pack()
        self.floor.insert(0, floor)

        ttk.Label(dlg, text="Quantity:").pack(pady=5)
        self.cap = ttk.Entry(dlg)
        self.cap.pack()
        self.cap.insert(0, quantity)

        frame = ttk.Frame(dlg)
        frame.pack(pady=10)
        ttk.Button(frame, text="OK", command=lambda: self.ok(dlg)).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Cancel", command=dlg.destroy).pack(side=tk.LEFT, padx=5)

        dlg.wait_window()

    def ok(self, dlg):
        f = self.floor.get().strip()
        c = self.cap.get().strip()
        if f and c.isdigit():
            self.result = (f, int(c))
            dlg.destroy()
        else:
            messagebox.showerror("Error", "Valid data required")

class RoomManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management")
        self.root.configure(bg="#d0e7ff")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.create_rooms_tab()

    def execute_query(self, query, params=()):
        print("Executing query:", query, params)
        return [("1", "A", 1), ("2", "B", 2), ("3", "C", 3)]

    def create_rooms_tab(self):
        self.rooms_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.rooms_frame, text="Inventory Management")

        topbar = ttk.Frame(self.rooms_frame)
        topbar.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(topbar, text="Inventory Management", font=("Helvetica", 16, "bold")).pack(side=tk.LEFT)
        ttk.Button(topbar, text="Add Item", command=self.add_room).pack(side=tk.RIGHT)

        canvas = tk.Canvas(self.rooms_frame, bg="#d0e7ff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.rooms_frame, orient="vertical", command=canvas.yview)
        self.cards_container = ttk.Frame(canvas)

        self.cards_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.cards_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh_rooms()

    def refresh_rooms(self):
        for widget in self.cards_container.winfo_children():
            widget.destroy()

        rooms = self.execute_query("SELECT box_id, column_name, row_number FROM Boxes")
        if not rooms:
            return

        name_map = {"1": "Bearing", "2": "Gear", "3": "Bolt"}

        for idx, (room_id, col, rownum) in enumerate(rooms):
            frame = ttk.Frame(self.cards_container, relief="ridge", borderwidth=2, padding=10)
            frame.grid(row=idx // 3, column=idx % 3, padx=10, pady=10, sticky="nsew")

            item_name = name_map.get(room_id, f"Item {room_id}")
            ttk.Label(frame, text=item_name, font=("Helvetica", 14, "bold")).pack(anchor="w")

            floor = f"Rack {col}"
            quantity = self.get_quantity(room_id)
            occ = self.get_occupants_count(room_id)

            ttk.Label(frame, text=f"\U0001F5FA {floor}").pack(anchor="w", pady=(5, 0))
            ttk.Label(frame, text=f"\U0001F465 Quantity: {quantity}").pack(anchor="w")
            ttk.Label(frame, text=f"\U0001F464 In Use: {occ}/{quantity}").pack(anchor="w", pady=(5, 0))

            btn_frame = ttk.Frame(frame)
            btn_frame.pack(anchor="e", pady=(10, 0))
            ttk.Button(btn_frame, text="Add", command=lambda rid=room_id: self.add_to_room(rid)).pack(side=tk.LEFT, padx=2)
            ttk.Button(btn_frame, text="Edit", command=lambda rid=room_id: self.edit_room(rid)).pack(side=tk.LEFT, padx=2)
            ttk.Button(btn_frame, text="Delete", command=lambda rid=room_id: self.delete_room(rid)).pack(side=tk.LEFT, padx=2)

    def get_quantity(self, room_id):
        return 4  # Simulate DB value

    def get_occupants_count(self, room_id):
        return 2  # Simulate DB value

    def add_room(self):
        dialog = RoomDialog(self.root, "Add Item")
        if dialog.result:
            floor, quantity = dialog.result
            self.execute_query("INSERT INTO Rooms (floor, quantity) VALUES (%s, %s)", (floor, quantity))
            self.refresh_rooms()

    def edit_room(self, room_id):
        dialog = RoomDialog(self.root, "Edit Item", "A", "4")
        if dialog.result:
            floor, quantity = dialog.result
            self.execute_query("UPDATE Rooms SET floor=%s, quantity=%s WHERE room_id=%s", (floor, quantity, room_id))
            self.refresh_rooms()

    def delete_room(self, room_id):
        if messagebox.askyesno("Confirm", "Delete this item?"):
            self.execute_query("DELETE FROM Rooms WHERE room_id=%s", (room_id,))
            self.refresh_rooms()

    def add_to_room(self, room_id):
        messagebox.showinfo("Add", f"Add item to {room_id}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RoomManagerApp(root)
    root.mainloop()


