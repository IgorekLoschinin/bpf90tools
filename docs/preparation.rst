*****************************
Preparation of data and files
*****************************


**1. Before you start using the BLUPF90 utilities, you should download the BLUPF90 utilities themselves.**

**Depending on the operating system:**

* linux - https://nce.ads.uga.edu/html/projects/programs/Linux/Temp/
* windows - https://nce.ads.uga.edu/html/projects/programs/Windows/Temp/


.. note::
    For Windows you will need to download ``libiomp5md.dll``. It can be placed
    in the /system32 folder or it should be next to the executable. More details in
    BLUPF90 documentation.

**2. Place them in the project folder:**

::

    myproject/
        airemlf90.exe
        remlf90.exe
        blupf90.exe
        renumf90.exe
        libiomp5md.dll


**3. Add a parameter file:**

.. note::
    You can compose it manually or use the generator from the lib.

::

    myproject/
        ...
        param.txt

**4. Everything for launching programs is ready!**
