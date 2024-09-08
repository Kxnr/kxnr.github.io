// Not the world's fastest Perlin noise implementation,
// but simple and good enough for this use case

(function( noise, $, undefined ) {
    const permutationTable = [151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36,
                      103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148, 247, 120, 234, 75, 0,
                      26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33, 88, 237, 149, 56,
                      87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166,
                      77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55,
                      46, 245, 40, 244, 102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132,
                      187, 208, 89, 18, 169, 200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109,
                      198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126,
                      255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183,
                      170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43,
                      172, 9, 129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112,
                      104, 218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162,
                      241, 81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106,
                      157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205,
                      93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180];

    function unitVector(seed) {
        // TODO: hash seed per improved noise
        let vec = [Math.random() - .5, Math.random() - .5, Math.random() - .5, Math.random() - .5];
        let mag = vec.reduce((i, x) => i + x*x, 0);
        return vec.map((x) => x / Math.sqrt(mag));
    }

    const gradientTable = [...Array(256).keys()].map((x) => unitVector(x));

    function interp(a0, a1, w) {
        if(w < 0) return a0;
        if(w > 1) return a1;

        return (a1-a0)*((w*(w*6.0-15.0) + 10.0)*w*w*w)+a0;
    }

    function dotGradient(ix, iy, iz, iw, x, y, z, w) {
        let p = function(i) { return permutationTable[i % 256]; }
        let grad = gradientTable[p(iw + p(iz + p(iy + p(ix))))];
        return (x-ix)*grad[0] + (y-iy)*grad[1] + (z-iz)*grad[2] + (w-iw)*grad[3];
    }

    noise.perlin = function(x, y, z=0.5, w=0.5) {
        let x0 = Math.floor(x),
            x1 = Math.ceil(x),
            y0 = Math.floor(y),
            y1 = Math.ceil(y),
            z0 = Math.floor(z),
            z1 = Math.ceil(z),
            w0 = Math.floor(w),
            w1 = Math.ceil(w),
            dx = x-x0,
            dy = y-y0,
            dz = z-z0,
            dw = w-w0;

        let ix0 = interp(dotGradient(x0, y0, z0, w0, x, y, z, w), dotGradient(x1, y0, z0, w0, x, y, z, w), dx),
            ix1 = interp(dotGradient(x0, y1, z0, w0, x, y, z, w), dotGradient(x1, y1, z0, w0, x, y, z, w), dx),
            ix2 = interp(dotGradient(x0, y0, z1, w0, x, y, z, w), dotGradient(x1, y0, z1, w0, x, y, z, w), dx),
            ix3 = interp(dotGradient(x0, y1, z1, w0, x, y, z, w), dotGradient(x1, y1, z1, w0, x, y, z, w), dx),
            ix4 = interp(dotGradient(x0, y0, z0, w1, x, y, z, w), dotGradient(x1, y0, z0, w1, x, y, z, w), dx),
            ix5 = interp(dotGradient(x0, y1, z0, w1, x, y, z, w), dotGradient(x1, y1, z0, w1, x, y, z, w), dx),
            ix6 = interp(dotGradient(x0, y0, z1, w1, x, y, z, w), dotGradient(x1, y0, z1, w1, x, y, z, w), dx),
            ix7 = interp(dotGradient(x0, y1, z1, w1, x, y, z, w), dotGradient(x1, y1, z1, w1, x, y, z, w), dx);

        let iy0 = interp(ix0, ix1, dy),
            iy1 = interp(ix2, ix3, dy),
            iy2 = interp(ix4, ix5, dy),
            iy3 = interp(ix6, ix7, dy);

        let iz0 = interp(iy0, iy1, dz),
            iz1 = interp(iy2, iy3, dz);

        let val = interp(iz0, iz1, dw);

        return val;
    }
} (window.noise = window.noise || {}, jQuery));
