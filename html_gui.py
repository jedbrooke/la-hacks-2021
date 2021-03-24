import os
from gui_engine.gui_engine import Form, Window, TagUtility, Button, Field

def main():
	windows = {

	}

	start_page = "main.html"
	path = os.path.join("gui_pages",start_page)
	w = Window(TagUtility.get_html(path),main=True,windows=windows)

	w.start()

if __name__ == '__main__':
	main()