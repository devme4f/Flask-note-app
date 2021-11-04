from website import create_app

app = create_app()

# only run web when execute this file, not when being import for debug
if __name__=='__main__':
	app.run(debug=True)
	