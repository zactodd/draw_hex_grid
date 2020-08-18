# Install
Can be installed by:
```
pip install git+https://github.com/zactodd/draw_hex_grid.git 
```



# Commands
dhg has 2 commands.
They can be run by inside the draw_hex_grid "python dhg" followed by the commands.

-d, --draw followed by an int x where x is greater than 1.
An outfile maybe specified after the x to write the hex grid, without this the file is writen as hex_grid_size_x.png.
The command draws a hex grid with the side length of x.
<br>Examples:
```
python dhg -d 8
python dhg --draw 12 hex_grid.png
```

-i, --interpret followed by an int x communicating the the size of the grid and the path of hex grid image.
An outfile maybe specified after hex grid image and the outfile, without this the file is writen as coords.txt.
The command a interpreters a hex grid where the grid has been coloured grey (![#C3C3C3](https://via.placeholder.com/15/c3c3c3/000000?text=+) #C3C3C3, (195,195,195))
hexes and returns a list in the outfile of cube coords of the grey hexes.
<br>Examples:

```
python dhg -i 8 hex_grid.png
python dhg --interpret 16 hex_grid.png cube_coords.txt
```
