import tkinter as tk
from tkinter import ttk


def add_test_1(root):
    """Add a test button."""
    button = ttk.Button(root, text='Test 1 ', command=root.quit)
    return button

