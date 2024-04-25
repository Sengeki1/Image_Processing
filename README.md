# Image_Processing

## Morphing

Technique of morphing between two clips together was extended from morphing two still images

Input: Two images containing human faces (Image I₀ and Image I₁)

Output: A fluid transformation video transitioning from ```I₀``` to ```I₁```

We can look at the target transformation video results as a sequence of frames. Given two input images I₀ and I₁, at each timestamp t between ```0``` and ```1```, every pixel ```(x, y)``` in the morphed frame can be interpolated as follows:

