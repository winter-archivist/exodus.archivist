import PySimpleGUI as sg
from zenlog import log

layout = [
    [sg.Text('Select Target File.Sqlite3 |'), sg.FileBrowse('Browse', key='-IN-')],
    [sg.Button('Exit')]
]

window = sg.Window('aeTool Manager', layout)

# Event Loop
while True:
    event, values = window.read()
    log.debug(f'{event=}, {values=}')

    # Window Closer
    if event in (None, 'Exit'):
        break

    # ExodusAutomaton Start/Stop
    if event == '-IN-':
        log.debug('Browser Tink')

window.close()
