# Empire Earth image slicer for backgrounds

#### what is this?

Empire Earth saves backrgound images in multiple tiles, which makes editing them quite cumbersome.
This tool splits and joins SST and TGA images, which can be used to convert and create new backrgound images

## How to use it?

Download the latest version of the software from the [releases](https://github.com/EE-modders/SST-image_slicer/releases) page.

In order to split / join the file(s), you just Drag&Drop the file(s) onto the executable.

You can also use the CLI interface via a terminal.

The software runs standalone and no installation is needed. 

### supported conversions:

- 1 SST -> n TGA
- n SST -> 1 TGA
- 1 TGA -> n SST
- n TGA -> 1 TGA

image formats other than TGA (Type 2) and SST (v1) are not supported

## Known problems:

- 
- TGA images with any sort of metadata will not convert properly, make sure to remove any metadata from the file
- TGA images with RLE compression will not work

## Contribute

- if you have an issue or suggestion feel free to create an [issue](https://github.com/EE-modders/SST-image_slicer/issues) or [pull request](https://github.com/EE-modders/SST-image_slicer/pulls) 
- you can also join our official [EE-reborn Discord server](https://discord.gg/BjUXbFB).
