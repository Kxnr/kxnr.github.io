build:
    mkdir -p build
    mkdir -p build/css
    raco pollen publish ./src ./build
    npx tailwindcss -i ./src/css/source.css -o ./build/css/output.css -m
    npx tailwindcss -i ./src/css/resume_source.css -o ./build/css/resume.css -m
