# TinyRPG Exalt
[Play it now!](https://iagobalmeida.github.io/tiny_rpg_exalt/)


## Folder structure

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

## Deploy
```sh
$ npm install --save-dev gh-pages
```
```sh
$ npm run deploy
```

## TODO

- Project
    - [X] Define libs
    - [X] Prototype
    - [X] GitHub Repo
    - [X] Deploy to Github Pages

- Communication between client/server mockup
    - [X] Simple battle
    - [X] Random encounter
    - [X] Simple Battle animation
    - [X] Die animation
    - [X] Background Tiling
    - [X] Transfer simple battle
    - [X] Base battles on DEX
    - [X] Base battles on DEX and ATT
    - [X] Treasure Chest
    - [X] Regions based enemies list
    - [X] Region progression based enemies
    - [X] Region selection exploring
    - [X] Skill with mana
    - [X] LocalStorage
    - [X] LocalStorage version verifier
    - [X] Server side action duration
    - [X] Transfer information about region on each exploration

- Interface
    - [X] Base info input
    - [X] Region selection
    - [X] Messages
    - [X] Region Counter
    - [X] Attributes
    - [X] Attack projectiles
