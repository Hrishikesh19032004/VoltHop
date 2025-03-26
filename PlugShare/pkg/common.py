import modal

"""
Shared setup across functions.
"""

base_image = modal.Image.debian_slim().pip_install("requests", "pandas", "openai")
stub = modal.Stub(
    "plugshare-sentiment",
    image=base_image,
)
