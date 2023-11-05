ExodusAutomaton Rewrite
===
---
## General

Currently, I'm using pycharm community for development; though on Nov 29th I'll be applying for Pycharm Professional
> Primary Features: 
>> * Project: 
>>> * Easily Setup
>>> * Open Source [GPL 3.0]
>>> * Logging /w "Syntax"
>>> * Slash Commands
>>> * Dangerously Cheesy [so much spaghetti]
>>> * In Active Development [NOV 2023]
>> * Client: 
>>> * CogManager
>>> * V5 VTM Dice Roller /w Character Tracker


> Heavily Work-In-Progress Features: 
>> * Notes System

placeholder 3

---
## LOGGING
When things are logged they should have a "reason" or prefix attached to the beginning these can be "stacked". \
So if something is a __Minor Error__ *and* comes from a Cog it's prefix would be ``*>`` \
For a __Major Error__ regarding Client __Startup__ would have a prefix of ``***$``

The way in which these are "stacked" is done from top to bottom of the list below. \
Higher they are on the list, the more important/higher "priority" \

---
> Prefix List
>> SHUTDOWN :: <<<{text}>>> \
> Error     :: * \
> Startup   ::  $ \
> From Cog  ::  >
---
