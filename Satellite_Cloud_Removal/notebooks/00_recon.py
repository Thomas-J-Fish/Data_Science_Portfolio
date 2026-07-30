from datasets import load_dataset
import matplotlib.pyplot as plt

ds = load_dataset("mespinosami/sen12mscr", split="train", streaming=True)
example = next(iter(ds))

print(example.keys())

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, key in zip(axes, ("s1", "s2", "s2_cloudy")):
    img = example[key]
    print(key, type(img), getattr(img, "size", None), getattr(img, "mode", None))
    ax.imshow(img)
    ax.set_title(key)
    ax.axis("off")
plt.show()