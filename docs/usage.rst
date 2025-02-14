Usage
=====

**bpf90tools** provides commands for a variety of operations. Here are examples of
usage.

**Calculation Aireml, Blup, create file param**::

    from bpf90tools.tools import (
        Params,
        Blupf90,
        AIremlf90,
        Remlf90,
        Renumf90
    )

    or

    from bpf90tools import (
        Params,
        Blupf90,
        AIremlf90,
        Remlf90,
        Renumf90
    )

**Computation of parentage**::

    from bpf90tools.parsers import (
        PParams,
        PPed,
        PSolution
        PVar
    )
