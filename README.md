# within-reach

Hot reload and screen-capture helpers for working with Halo: Reach and Halo: MCC. Part of the in-reach family:

- [`in-reach`](https://pypi.org/project/in-reach/) -- the library and command line for Megalo game variants
- [`in-reach-ide`](https://pypi.org/project/in-reach-ide/) -- the desktop IDE
- `within-reach` -- this package; `in-reach` and `in-reach-ide` will depend on it

**Status:** system detection works; hot reload and screen capture are still to come.

```
pip install within-reach
within-reach detect          # is Tesseract on PATH? where are Steam, Halo: MCC and the gametype/map folders?
within-reach --help
```

`within_reach.system_verify` is what the IDE's "Verify System Settings" runs (Tesseract OCR on `PATH`, the Steam and MCC
install folders and everything derived from them).

Windows only. Licensed under the GPLv3.
