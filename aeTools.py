import asyncio

import PySimpleGUI as sg
from zenlog import log

layout = [
    [sg.Button('Start ExodusAutomaton')],
    [sg.Button('Sqlite3'), sg.Button('Template'), sg.Button('Exit')]
]

window = sg.Window('aeTool Manager', layout)


async def aeTool():
    # Event Loop
    while True:
        event, values = window.read()
        log.debug(f'{event=}, {values=}')

        # Window Closer
        if event in (None, 'Exit'):
            break

        # ExodusAutomaton Start/Stop
        if event == 'Start ExodusAutomaton':
            from sys import executable
            from subprocess import Popen

            popen_result = Popen([executable, 'aeClient.py'])

        elif event == 'Stop ExodusAutomaton':
            break

        # Opens the windows of other tools
        if event == 'Sqlite3':
            exec(open('aeTools/tool_windows/sqlite_tool/sqlite_window.py').read())

        elif event == 'TEMPLATE':
            pass


async def main():
    log.debug('Starting aeTools')
    future = asyncio.ensure_future(aeTool())


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    window.close()
