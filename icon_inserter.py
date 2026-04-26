#!/usr/bin/env python3
"""
Icon Inserter Extension for Inkscape

This extension allows users to:
1. Select a shape in Inkscape
2. Choose an icon from predefined SVG files
3. Apply affine transformations (scale, rotation)
4. Add metadata string
5. Insert the icon as an image tag in a "components" layer
"""

import sys
import os
import inkex
from inkex import EffectExtension, BooleanElement, FloatElement, StringElement
import lxml.etree as ET

# Define paths for icons (relative to user's system or extension directory)
ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

class IconInserter(EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--icon-path", type=str, default="", help="Path to selected icon SVG")
        pars.add_argument("--scale-x", type=float, default=1.0, help="Scale factor in X direction")
        pars.add_argument("--scale-y", type=float, default=1.0, help="Scale factor in Y direction")
        pars.add_argument("--rotation", type=float, default=0.0, help="Rotation angle in degrees")
        pars.add_argument("--metadata", type=str, default="", help="Metadata string for the image")
        pars.add_argument("--tab", type=str, default="main", help="Tab selection")

    def effect(self):
        # Get selected elements
        if not self.svg.selection:
            inkex.errormsg("Please select a shape first.")
            return

        selected_element = self.svg.selection[0]
        
        # Get dialog parameters
        icon_path = self.options.icon_path
        scale_x = self.options.scale_x
        scale_y = self.options.scale_y
        rotation = self.options.rotation
        metadata = self.options.metadata

        if not icon_path:
            inkex.errormsg("Please select an icon.")
            return

        # Create or get "components" layer
        components_layer = self.get_or_create_components_layer()

        # Get bounding box of selected element to position the icon
        bbox = selected_element.bounding_box()
        if bbox is None:
            inkex.errormsg("Could not determine bounding box of selected element.")
            return

        center_x = bbox.x + bbox.width / 2
        center_y = bbox.y + bbox.height / 2

        # Build transformation matrix
        transform = self.build_transform(scale_x, scale_y, rotation, center_x, center_y)

        # Create image element
        image_element = self.create_image_element(icon_path, center_x, center_y, transform, metadata)

        # Add image to components layer
        components_layer.append(image_element)

    def get_or_create_components_layer(self):
        """Get existing 'components' layer or create a new one."""
        svg_root = self.document.getroot()
        
        # Try to find existing components layer
        for layer in svg_root.findall('.//{http://www.w3.org/2000/svg}g[@inkscape:groupmode="layer"]'):
            layer_name = layer.get('{http://www.inkscape.org/namespaces/inkscape}label', '')
            if layer_name == 'components':
                return layer

        # Create new components layer
        new_layer = inkex.Group()
        new_layer.set_label('components')
        new_layer.set('{http://www.inkscape.org/namespaces/inkscape}groupmode', 'layer')
        svg_root.append(new_layer)
        return new_layer

    def build_transform(self, scale_x, scale_y, rotation, center_x, center_y):
        """Build SVG transformation string."""
        transforms = []
        
        # Translate to center
        transforms.append(f"translate({center_x}, {center_y})")
        
        # Apply rotation
        if rotation != 0:
            transforms.append(f"rotate({rotation})")
        
        # Apply scale
        if scale_x != 1.0 or scale_y != 1.0:
            transforms.append(f"scale({scale_x}, {scale_y})")
        
        # Translate back
        transforms.append(f"translate(-{center_x}, -{center_y})")
        
        return " ".join(transforms)

    def create_image_element(self, icon_path, center_x, center_y, transform, metadata):
        """Create an image element with the specified properties."""
        # Make path absolute if relative
        if not os.path.isabs(icon_path):
            icon_path = os.path.abspath(icon_path)
        
        # Convert to file:// URL for href
        href_url = f"file://{icon_path}"
        
        # Create image element
        image = inkex.Image()
        image.set('{http://www.w3.org/1999/xlink}href', href_url)
        image.set('transform', transform)
        
        # Set position using x and y attributes (or we could use transform)
        image.set('x', str(center_x))
        image.set('y', str(center_y))
        
        # Add metadata as a title or desc element, or custom attribute
        if metadata:
            metadata_elem = ET.Element('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description')
            metadata_elem.text = metadata
            image.append(metadata_elem)
        
        return image


if __name__ == '__main__':
    IconInserter().run()
