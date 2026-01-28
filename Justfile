build:
    mkdir -p docs
    mkdir -p docs/css
    raco pollen render -pr ./src
    raco pollen publish ./src ./docs
    npx tailwindcss -i ./src/css/source.css -o ./docs/css/output.css -m
