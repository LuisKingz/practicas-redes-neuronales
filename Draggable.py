class Draggable_elements:
    def on_drag_start(event):
        widget = event.widget
        widget.start_x = event.x
        widget.start_y = event.y
        
    def on_drag_motion(event):
        widget = event.widget
        x = widget.winfo_x() - widget.start_x + event.x
        y = widget.winfo_y() - widget.start_y + event.y
        widget.place(x=x, y=y)