# rofi_pet_snippets

[Rofi](https://github.com/davatorium/rofi) script/plugin to list, search and copy [pet](https://github.com/knqyf263/pet) snippets to clipboard (wayland only).

![screenshot](screenshot.png "screenshot")

## Dependencies

- [rofi](https://github.com/davatorium/rofi)
- [pet](https://github.com/knqyf263/pet)
- `python3.9` or newer
- `wl-copy` e.g. from the debian package `wl-clipboard` (Optional)
- `notify-send` e.g. from debian package `libnotify4` (Optional)
- `requirements.txt` for runtime dependencies
- `requirements_dev.txt` for development dependencies
- `make` (optional)

## Getting Started

For a quick run or test of the rofi script.

```bash
make run
```

To install the rofi script.

```bash
make install
```

and run the rofi script in your window manager or wherever like this.

```bash
rofi -show snippets -modi "snippets:rofi-pet-snippets"
```
