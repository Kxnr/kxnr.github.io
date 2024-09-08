// requires jquery
(function( background, $, undefined ) {

    let  numParticles = 1000, // TODO: scale based on device
            particles = []
               height = 0,
                width = 0,
                timer = 'undefined',
       frame_interval = 50, // ms / frame
          force_scale = .02 * frame_interval, // assumes that base function is scaled -1 to 1
    terminal_velocity = 1500, // pixels / second
               drag_C =  2 * force_scale * Math.pow(frame_interval, 2) / Math.pow(terminal_velocity, 2), // force * frame**2
             lifetime = 200,
     coordinate_scale = 400,
           time_scale = 600,
     initial_velocity = 1,
            fadeAlpha = 5/255,
            particleAlpha = .15,
                    t = 0,
               t_max = Number.MAX_SAFE_INTEGER,
               t_step = 1;


    // equivalent to 'ready'
    $(() => {
                $(window).resize(onResize);
                $(window).scroll(onScroll);
            });

    $(window).on("load", function init() {
        initParticles();
        animate('perlin');
    });

    function initParticles() {
        height = $(window).height(),
        width = $(window).width();

        let buffer = document.createElement('canvas');
        buffer.id = "draw-buffer";
        buffer.width = width;
        buffer.height = height;

        if ($("#draw-buffer").length > 0) {
            $("#draw-buffer").replaceWith(buffer);
        } else {
            $(".parallax").prepend(buffer);
        }

        var canvas = buffer.getContext("2d");
        canvas.save();
        let bg = Math.ceil(1 / (2 * fadeAlpha));
        canvas.fillStyle = `rgb(${bg}, ${bg}, ${bg})`;
        canvas.fillRect(0, 0, width, height);
        canvas.restore();

        particles = [];
        for(let i=0; i < numParticles; i++) {
            // integer coordinates, for perlin noise, experience no force
            particles.push(seedParticle());
        }
        background.particles = particles;
    }

    function draw_perlin() {
        var canvas = document.getElementById("draw-buffer").getContext("2d");
        const imgdata = canvas.getImageData(0, 0, width, height);
        const data = imgdata.data;

        let px = 0;
        let color = 0;
        for(let x=0; x < width; x++) {
            for(let y=0; y < height; y++) {
                px = y * (width * 4) + x * 4;
                color = (noise.perlin(x / coordinate_scale, y / coordinate_scale, 0.5, t / time_scale) + 1) * 128;
                data[px]     = color; // red
                data[px + 1] = color; // green
                data[px + 2] = color; // blue
                data[px + 3] = 255;   // alpha
            }
        }

        canvas.putImageData(imgdata, 0, 0)
    }

    function alphaBlend(canvas) {
        canvas.save();
        canvas.globalAlpha = fadeAlpha;
        canvas.fillStyle = "black";
        canvas.fillRect(0, 0, width, height);
        canvas.restore();
    }

    function draw_scene() {
        let buffer = document.getElementById('draw-buffer');
        let canvas = buffer.getContext('2d');

        alphaBlend(canvas);
        particles.forEach((x) => x.draw(canvas));
        t++;
    }

    function animate(style) {
        if(style == 'boids') {
            // TODO
        } else if(style == 'stars') {
            // TODO
        } else if(style == 'random') {
            timer = setInterval(() => {
                particles.forEach((p) => {
                                            if(getRandomFloat(lifetime) < 1) {
                                                Object.assign(p, seedParticle());
                                            }

                                            p.force(getRandomInt(10),
                                                   getRandomInt(10));
                                            p.drag(.1);
                                            p.update(.5);
                                          });
                draw_scene();
            }, frame_interval);
        }
        else if(style == "perlin") {
            timer = setInterval(() => {
                particles.forEach((p) => {
                                    if(getRandomFloat(lifetime) < 1) {
                                        Object.assign(p, seedParticle());
                                    }

                                    let sx = p.x / coordinate_scale,
                                        sy = p.y / coordinate_scale,
                                        st = t / time_scale;

                                    // force should be ~ +/- 1
                                    // using a z-offset to simulate having two
                                    // independent noise generators
                                    let fx = noise.perlin(sx, sy, 0.5, st) * force_scale,
                                        fy = noise.perlin(sx, sy, Math.max(width, height) + 0.5, st) * force_scale;


                                    p.force(fx, fy);
                                    p.drag(drag_C);
                                    p.update(1);
                                  });
                draw_scene();
            }, frame_interval);
        }
        else {
            console.log("animation style not supported")
        }
    }

    function seedParticle() {
        let p = new Particle(getRandomFloat(width), getRandomFloat(height), size=2, alpha=particleAlpha);
        p.vx = getRandomFloat(initial_velocity*2) - initial_velocity;
        p.vy = getRandomFloat(initial_velocity*2) - initial_velocity;
        return p;
    }

    function onScroll(e) {
    }

    function onResize(e) {
        initParticles();
    }

    function pairwise(arr, func){
        let acc = []
        for(let i=0; i < arr.length - 1; i++){
            acc.push(func(arr[i], arr[i + 1], i))
        }
        return acc;
    }

    function getRandomInt(max) {
      return Math.floor(Math.random() * max);
    }

    function getRandomFloat(max) {
      return Math.random() * max;
    }

    function wrap(val, min, max) {
        if(val >= max) {
            return  [true, val % max];
        }

        if(val < min) {
            return  [true, max - ((min - val) % max)];
        }

        return  [false, val];
    }

    class Particle {
        constructor(x, y, size=4, alpha=.2) {
            this.x = x;
            this.y = y;
            this.prev_x = x;
            this.prev_y = y;

            this.vx = 0;
            this.vy = 0;

            this.size = size;
            this.alpha = alpha;
        }

        force(ax, ay) {
            this.vx += ax;
            this.vy += ay;

        }

        // NOTE: move out of particle?
        drag(C) {
            let fx = -1*Math.sign(this.vx)*C*Math.pow(this.vx, 2)*this.size,
                fy = -1*Math.sign(this.vy)*C*Math.pow(this.vy, 2)*this.size;

            this.force(fx, fy);
        }

        update(dt) {
            this.move(this.vx*dt, this.vy*dt);
        }

        move(dx, dy) {
            this.prev_x = this.x;
            this.prev_y = this.y;

            let xwrapped, ywrapped;
            [xwrapped, this.x] = wrap(this.x + dx, 0, width);
            [ywrapped, this.y] = wrap(this.y + dy, 0, height);

            // prevent lines being drawn across the canvas
            if(xwrapped || ywrapped) {
                this.prev_x = this.x;
                this.prev_y = this.y;
            }
        }

        draw(canvas) {
            canvas.save()
            canvas.beginPath();
            canvas.strokeStyle = `rgb(255, 255, 255)`;
            canvas.globalAlpha = this.alpha;
            canvas.moveTo(this.prev_x, this.prev_y);
            canvas.lineTo(this.x, this.y);
            canvas.lineWidth = this.size;
            canvas.stroke();
            canvas.restore();
        }
    }
} (window.background = window.background || {}, jQuery));