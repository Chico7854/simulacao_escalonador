all:
	pyinstaller main.spec
	mv dist/main .
	rm -r build dist