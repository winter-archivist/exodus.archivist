import PySimpleGUI as gui  # Can only show PNG & GIF
# import PySimpleGUIQt

layout = [
    [gui.Text('Test Text')],
    [gui.Button('Test Button')]
]

window = gui.Window(title='Test Title!', layout=layout, margins=(100, 50))

while True:
    event, values = window.read()

    if event == 'Test Button' or event == gui.WIN_CLOSED:
        break

window.close()

