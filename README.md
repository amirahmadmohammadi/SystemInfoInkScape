# Icon Inserter Extension for Inkscape

This extension allows you to insert icons into your SVG documents with customizable transformations and metadata.

## Installation

### Step 1: Copy Extension Files
Copy the following files to your Inkscape extensions directory:

**Linux:**
```bash
cp icon_inserter.inx ~/.config/inkscape/extensions/
cp icon_inserter.py ~/.config/inkscape/extensions/
cp icon_inserter.ui ~/.config/inkscape/extensions/
mkdir -p ~/.config/inkscape/extensions/icons
cp icons/*.svg ~/.config/inkscape/extensions/icons/
```

**Windows:**
```
%APPDATA%\inkscape\extensions\
```

**macOS:**
```
~/Library/Application Support/inkscape/extensions/
```

### Step 2: Restart Inkscape
Close and reopen Inkscape for the extension to appear.

## Usage

1. **Select a shape** in your Inkscape document (rectangle, circle, ellipse, or path)
2. **Open the extension**: Extensions → Custom → Icon Inserter
3. **Configure the dialog**:
   - Choose an icon from the dropdown list
   - Adjust scale X and Y values
   - Set rotation angle
   - Enter metadata string
4. **Click Apply**

The extension will:
- Create a "components" layer if it doesn't exist
- Insert the selected icon as an image element
- Apply the specified transformations
- Add the metadata to the image element

## Files Structure

```
/workspace/
├── icon_inserter.inx      # Extension definition file
├── icon_inserter.py       # Main Python script
├── icon_inserter.ui       # Dialog UI definition
├── icons/                 # Directory containing icon SVG files
│   ├── alert.svg
│   ├── info.svg
│   ├── warning.svg
│   ├── success.svg
│   └── settings.svg
├── test_document.svg      # Test SVG document
└── README.md              # This file
```

## Testing

A test document `test_document.svg` is provided. Open it in Inkscape and:

1. Select the rectangle shape
2. Run the extension from Extensions → Custom → Icon Inserter
3. Configure your settings and apply

## Adding Custom Icons

To add more icons:

1. Create SVG files (recommended size: 64x64)
2. Place them in the `icons/` directory
3. Edit `icon_inserter.ui` to add new `<option>` entries in the select dropdown
4. Restart Inkscape

## Technical Details

The extension:
- Uses Inkscape's inkex module for SVG manipulation
- Creates image elements with xlink:href pointing to icon files
- Applies affine transformations using SVG transform attribute
- Stores metadata in RDF Description elements

## Troubleshooting

- **Extension not appearing**: Ensure files are in the correct directory and restart Inkscape
- **Icons not loading**: Check that icon paths are correct and files exist
- **Transformations not working**: Verify numeric input values are valid
