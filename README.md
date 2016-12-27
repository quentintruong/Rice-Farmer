
~~~~~~

RiceFarmer
Bot for http://freerice.com/

~~~~~~

Requires:
Scrapy (v1.3.0)
selenium (Python binding) (v3.0.2)
geckodriver (v0.11.1)
Mozilla Firefox

~~~~~~

Before running-
1. Create a freerice account
2. Type (your freerice username) into line 29 for ricefarmer-chem.py, or line 30 for ricefarmer-vocab.py
3. Type (your freerice password) into line 32 for ricefarmer-chem.py, or line 33 for ricefarmer-vocab.py
4. Save file

~~~~~~

For the faster, looping, periodic elements bot (160 grains/minute)-
RUN:
$ scrapy runspider ricefarmer-chem.py

For the slower, but cooler vocab bot (35 grains/minute)-
RUN:
$ scrapy runspider ricefarmer-vocab.py

~~~~~~

For infinite loops-
RUN:
$ while True
$ do
$ (enter the CMD from above for the bot you wish to run)
$ done

~~~~~~

Note:
For educational purposes only

~~~~~~
