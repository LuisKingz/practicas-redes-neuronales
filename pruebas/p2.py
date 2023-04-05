import tkinter as tk
from tkinter import ttk


def add_test_2(root):
    """Add a test button."""
    button = ttk.Button(root, text='Test 2', command=root.quit)
    return button

