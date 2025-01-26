# Folder structure

- `src` - source code for your kaplay project
- `dist` - distribution folder, contains your index.html, built js bundle and static assets


## Development

```sh
$ npm run dev
```

will start a dev server at http://localhost:8000

## Distribution

```sh
$ npm run build
```

will build your js files into `dist/`

```sh
$ npm run zip
```

will build your game and package into a .zip file, you can upload to your server or itch.io / newground etc.

## TODO

- Communication between client/server mockup
    - [X] Simple battle
    - [X] Random encounter
    - [X] Simple Battle animation
    - [ ] Die animation
    - [ ] Background Tiling
    - [X] Transfer simple battle
    - [X] Base battles on DEX
    - [X] Base battles on DEX and ATT
    - [ ] Transfer current HP of each entity on each turn
    - [ ] Transfer information about region on each exploration