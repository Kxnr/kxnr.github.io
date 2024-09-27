import random
import math
from functools import partial
from PIL import Image
from typing import Callable
from typing import TypeAlias
from collections.abc import Sequence

NOISE_MIN = 0
NOISE_MAX = 0

IMAGE_SIZE = 1028

TWO_PI = 2 * math.pi
GRID_SIZE = 256
VECTOR_INDICES = list(range(GRID_SIZE))
VECTORS = [
    (math.cos(TWO_PI * (a / GRID_SIZE)), math.sin(TWO_PI * (a / GRID_SIZE)))
    for a in VECTOR_INDICES
]

# TODO: make these looped lists
RANDOM_SHIFTS = [random.uniform(1, 10) for _ in range(100)]
RANDOM_SCALES = [random.uniform(3, 5) for _ in range(100)]

random.shuffle(VECTOR_INDICES)
# random.shuffle(VECTORS)

color: TypeAlias = tuple[float, float, float]


def hex_to_rgb(hex: str) -> color:
    return color(int(hex[i * 2 : i * 2 + 2], 16) for i in range(3))


COLOR_PALETTE = [
    hex_to_rgb("70abbd"),  # light blue
    hex_to_rgb("36484e"),  # charcoal
    hex_to_rgb("a7742f"),  # copper
    hex_to_rgb("e2d4c1"),  # bone
]

# COLOR_PALETTE = [
#     hex_to_rgb("ff0000"),
#     hex_to_rgb("00ff00"),
#     hex_to_rgb("0000ff"),
#     hex_to_rgb("ffff00"),
# ]

# random.shuffle(COLOR_PALETTE)


def vector_length(vec: tuple[float, float]) -> float:
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def interpolate(a: float, b: float, w: float) -> float:
    """
    smooth step cubic interpolation function
    """
    if w < 0:
        return a
    if w > 1:
        return b

    return (b - a) * (3.0 - w * 2.0) * w * w + a


def color_interpolate(a: color, b: color, w: float) -> color:
    return (
        interpolate(a[0], b[0], w),
        interpolate(a[1], b[1], w),
        interpolate(a[2], b[2], w),
    )


def to_clamped(*args: float, lower=0, upper=255):
    # TODO: this doesn't actually handle the one or tuple case yet because we're passing in a
    # TODO: tuple, rather than unpacking it
    return tuple(
        clamp(int(upper * v), lower, upper)
        if not isinstance(v, Sequence)
        else tuple(to_clamped(v_) for v_ in v)
        for v in args
    )


def clamp(v: float, lower=0, upper=255) -> int:
    return int(min(max(v, lower), upper))


def coordinate_hash(x: int, y: int, period: int = GRID_SIZE) -> int:
    """
    Hash x and y to return a reproducible value [0, GRID_SIZE)
    """
    return VECTOR_INDICES[
        ((VECTOR_INDICES[(x % period) % GRID_SIZE] + y) % period) % GRID_SIZE
    ]


def noise(x, y, period: int = GRID_SIZE):
    """
    Perlin (ish) noise

    steps:
    1. find the bottom left hand corner of the unit grid square for the current point
    2. calculate vector from each corner to the current point
    3. lookup vectors for each corner of this grid square
    4. take the dot product between the corresponding grid and offset vectors
    5. interpolate between dot products, weighted by location in the unit grid square
    """

    # 1. floor coordinates, giving the bottom left of the unit grid square
    unit_x = math.floor(x)
    unit_y = math.floor(y)

    # 2. vector from bottom left of unit square to current point
    unit_x_offset = x - unit_x
    unit_y_offset = y - unit_y

    corner_offsets = ((0, 0), (1, 0), (0, 1), (1, 1))
    dot_products = []
    for x_off, y_off in corner_offsets:
        x_corner = unit_x + x_off
        y_corner = unit_y + y_off

        x_corner_offset = x - x_corner
        y_corner_offset = y - y_corner

        # 3
        corner_index = coordinate_hash(x_corner, y_corner, period)
        corner_vector = VECTORS[corner_index]

        # 4
        dot_product = (
            x_corner_offset * corner_vector[0] + y_corner_offset * corner_vector[1]
        )
        dot_products.append(dot_product)

    # 5
    value = interpolate(
        interpolate(dot_products[0], dot_products[1], unit_x_offset),
        interpolate(dot_products[2], dot_products[3], unit_x_offset),
        unit_y_offset,
    )

    global NOISE_MIN, NOISE_MAX

    NOISE_MIN = min(NOISE_MIN, value)
    NOISE_MAX = max(NOISE_MAX, value)

    # domain is [-1, 1]
    return value


def fractal_noise(x: float, y: float, period: float, octaves: int) -> float:
    # sum is of variables that are more or less random in the domain [-1, 1], the result could
    # exceed that domain but is likely to stay within in

    return (
        sum(
            (0.5**o) * noise(x * 2**o, y * 2**o, period=period * 2**o)
            for o in range(octaves)
        )
        * 0.5
    ) + 0.5


def warping(x, y, period: float, octaves: int) -> float:
    return fractal_noise(
        x
        + 4
        * fractal_noise(x + RANDOM_SHIFTS[0], y + RANDOM_SHIFTS[1], period, octaves),
        y
        + 4
        * fractal_noise(x + RANDOM_SHIFTS[2], y + RANDOM_SHIFTS[2], period, octaves),
        period,
        octaves,
    )


def colored_warping(
    x,
    y,
    period: float,
    octaves: int,
    color_a: color,
    color_b: color,
    color_c: color,
    color_d: color,
) -> tuple[int, int, int]:
    iterations = 3
    vectors = [(x, y)]
    for i in range(iterations):
        k = 8 * i
        vectors.append(
            (
                fractal_noise(
                    x
                    + RANDOM_SCALES[k] * vectors[-1][0] * (i > 0)
                    + RANDOM_SHIFTS[k + 1],
                    y
                    + RANDOM_SCALES[k + 2] * vectors[-1][1] * (i > 0)
                    + RANDOM_SHIFTS[k + 3],
                    period,
                    octaves,
                ),
                fractal_noise(
                    x
                    + RANDOM_SCALES[k + 4] * vectors[-1][0] * (i > 0)
                    + RANDOM_SHIFTS[k + 5],
                    y
                    + RANDOM_SCALES[k + 6] * vectors[-1][1] * (i > 0)
                    + RANDOM_SHIFTS[k + 7],
                    period,
                    octaves,
                ),
            )
        )

    r_color_interp = color_interpolate(color_a, color_b, vectors[-2][0])
    q_color_interp = color_interpolate(r_color_interp, color_c, vectors[-1][1])
    t_color_interp = color_interpolate(q_color_interp, color_d, vectors[-1][0])
    return t_color_interp


def make_tiling_image(
    noise_func: Callable[[float, float, float], int],
    size: int,
    period: float,
    image_mode: str = "L",
):
    # period determines the scaling of pixel coordinates to noise coordinates. A greater period means
    # the image repeats after more noise coordinates, giving fewer pixels per noise grid
    coordinate_scale = period / size
    im = Image.new(image_mode, (size, size))
    pixels = []
    for y in range(size):
        for x in range(size):
            color = noise_func(
                x * coordinate_scale, y * coordinate_scale, period=period
            )
            pixels.append(tuple(clamp(c) for c in color))

    im.putdata(pixels)
    return im.convert("RGB")


# TODO: shuffle vectors differenly per octave
# for exp in range(2, 6):
for exp in [1, 2, 3]:
    period = 2**exp
    # im = make_tiling_image(noise, 1028, period)
    # im.save(f"noise_{period}.png")

    # im = make_tiling_image(partial(fractal_noise, octaves=5), 1028, period)
    # im.save(f"fractal_noise_{period}.png")

    # im = make_tiling_image(
    #     partial(
    #         warping,
    #         octaves=5,
    #     ),
    #     1028,
    #     period,
    # )
    # im.save(f"warping_{period}.png")

    im = make_tiling_image(
        partial(
            colored_warping,
            octaves=7,
            color_a=COLOR_PALETTE[0],
            color_b=COLOR_PALETTE[1],
            color_c=COLOR_PALETTE[2],
            color_d=COLOR_PALETTE[3],
        ),
        IMAGE_SIZE,
        period,
        image_mode="RGB",
    )
    im.save(f"colored_warping_{period}.png")

print(f"noise min: {NOISE_MIN}")
print(f"noise max: {NOISE_MAX}")
