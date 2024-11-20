import sqlite3
import tkinter as tk

from tkinter import messagebox
from tkinter import ttk

class DatabaseApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Database App")

		self.db_name = tk.StringVar(value='test.db')
		self.table_name = tk.StringVar(value='records')

		self.create_widgets()

	def create_widgets(self):
		connection_frame = tk.Frame(self.root)
		connection_frame.pack(pady=10)

		tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
		tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

		tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=1, columnspan=2, pady=10)

		query_frame = tk.Frame(self.root)
		query_frame.pack(pady=10)

		tk.Label(query_frame, text="Table Name:").grid(row=0, column=0, padx=5, pady=5)
		tk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

		tk.Button(query_frame, text="Load Data", command=self.load_data).grid(row=1, columnspan=2, pady=10)

		self.tree = ttk.Treeview(self.root, columns=("MaSV", "HoTen"), show='headings')
		self.tree.heading("MaSV", text="MaSV")
		self.tree.heading("HoTen", text="Họ tên")
		self.tree.pack(pady=10)

		insert_frame = tk.Frame(self.root)
		insert_frame.pack(pady=10)

		self.column1 = tk.StringVar()
		self.column2 = tk.StringVar()

		tk.Label(insert_frame, text="MaSV:").grid(row=0, column=0, padx=5, pady=5)
		tk.Entry(insert_frame, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)

		tk.Label(insert_frame, text="Họ tên:").grid(row=1, column=0, padx=5, pady=5)
		tk.Entry(insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)

		tk.Button(insert_frame, text="Insert Data", command=self.insert_data).grid(row=2, columnspan=2, pady=10)

		update_delete_frame = tk.Frame(self.root)
		update_delete_frame.pack(pady=10)

		tk.Button(update_delete_frame, text="Delete Data", command=self.delete_data).grid(row=0, column=0, padx=5, pady=5)
		tk.Button(update_delete_frame, text="Update Data", command=self.update_data).grid(row=0, column=1, padx=5, pady=5)

	def connect_db(self):
		try:
			self.conn = sqlite3.connect(self.db_name.get())
			self.cur = self.conn.cursor()
			messagebox.showinfo("Success", "Connected to the database successfully!")
		except Exception as e:
			messagebox.showerror("Error", f"Error connecting to the database: {e}")

	def load_data(self):
		try:
			for item in self.tree.get_children():
				self.tree.delete(item)
			
			self.cur.execute(f"SELECT * FROM {self.table_name.get()}")
			rows = self.cur.fetchall()

			for row in rows:
				self.tree.insert("", tk.END, values=row)
		except Exception as e:
			messagebox.showerror("Error", f"Error loading data: {e}")

	def insert_data(self):
		try:
			masv = self.column1.get()
			hoten = self.column2.get()

			if len(masv) != 13 or not masv.isdigit():
				messagebox.showerror("Error", "MaSV phải có đúng 13 số!")
				return
			
			if len(hoten) > 255:
				messagebox.showerror("Error", "Họ tên không được vượt quá 255 ký tự!")
				return

			insert_query = f"INSERT INTO {self.table_name.get()} (MaSV, HoTen) VALUES (?, ?)"
			data_to_insert = (masv, hoten)
			self.cur.execute(insert_query, data_to_insert)
			self.conn.commit()
			messagebox.showinfo("Success", "Data inserted successfully!")
		except Exception as e:
			messagebox.showerror("Error", f"Error inserting data: {e}")

	def delete_data(self):
		try:
			selected_item = self.tree.selection()[0]
			selected_data = self.tree.item(selected_item, 'values')
			masv_to_delete = selected_data[0]

			delete_query = f"DELETE FROM {self.table_name.get()} WHERE MaSV = ?"
			self.cur.execute(delete_query, (masv_to_delete,))
			self.conn.commit()
			self.tree.delete(selected_item)

			messagebox.showinfo("Success", "Data deleted successfully!")
		except Exception as e:
			messagebox.showerror("Error", f"Error deleting data: {e}")

	def update_data(self):
		try:
			selected_item = self.tree.selection()[0]
			selected_data = self.tree.item(selected_item, 'values')
			old_masv = selected_data[0]

			new_masv = self.column1.get()
			new_hoten = self.column2.get()

			if len(new_masv) != 13 or not new_masv.isdigit():
				messagebox.showerror("Error", "MaSV phải có đúng 13 số!")
				return

			if len(new_hoten) > 255:
				messagebox.showerror("Error", "Họ tên không được vượt quá 255 ký tự!")
				return

			update_query = f"UPDATE {self.table_name.get()} SET MaSV = ?, HoTen = ? WHERE MaSV = ?"
			self.cur.execute(update_query, (new_masv, new_hoten, old_masv))
			self.conn.commit()

			self.tree.item(selected_item, values=(new_masv, new_hoten))

			messagebox.showinfo("Success", "Data updated successfully!")
		except Exception as e:
			messagebox.showerror("Error", f"Error updating data: {e}")

if __name__ == "__main__":
	root = tk.Tk()
	app = DatabaseApp(root)
	root.mainloop()
