ExodusAutomaton Rewrite
===
---
## General

placeholder 1 \
placeholder 2 \
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
