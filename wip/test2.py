import cv2
import numpy as np

# Read the image
src = cv2.imread('wip/machado.png')

# Convert from BGR to CIE Lab color space
converted = cv2.cvtColor(src, cv2.COLOR_BGR2Lab)

# Split the channels into L, a, b
L, a, b = cv2.split(converted)

# Debugging step: print ranges
print("Original ranges:")
print(f"L: min={L.min()}, max={L.max()}")
print(f"a: min={a.min()}, max={a.max()}")
print(f"b: min={b.min()}, max={b.max()}")

# Correct scaling for the L channel (normalize to [0, 100] range)
L = (L / 255.0 * 100.0).astype(np.float32)  # Normalize L to [0, 100]

# Correct scaling for a and b channels:
# Subtract 128 to shift to [-128, 127] for proper Lab representation
a = a.astype(np.float32) - 128.0
b = b.astype(np.float32) - 128.0

# Debugging step: print ranges after processing
print("Adjusted ranges:")
print(f"L: min={L.min()}, max={L.max()}")
print(f"a: min={a.min()}, max={a.max()}")
print(f"b: min={b.min()}, max={b.max()}")

# Perform your processing here (example: just retain the same values)
# Ensure colors are restored properly afterward

# Map L back to [0, 255]
L = (L / 100.0 * 255.0).clip(0, 255).astype(np.uint8)

# Map a and b back to [0, 255]
a = (a + 128).clip(0, 255).astype(np.uint8)
b = (b + 128).clip(0, 255).astype(np.uint8)

# Merge channels back together
restored = cv2.merge([L, a, b])

# Convert back to BGR to visualize
result = cv2.cvtColor(restored, cv2.COLOR_Lab2BGR)

# Save or display the result
cv2.imwrite("result.png", result)
