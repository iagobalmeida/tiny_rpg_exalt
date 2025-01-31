import kaplay from "kaplay";

const k = kaplay({
    width: 480,
    height: 480
});

k.loadRoot("./");
k.loadSprite("player", "sprites/player.png");

// Beach Sprites
const sprites = {
    'beach': [
        'bandit_leader',
        'pirate',
        'beached_bucaneer',
        'treasure_chest',
        'dreadstump_the_pirate_king',
    ],
    'mid_plains': [
        'big_green_slime',
        'earth_golem',
        'fire_sprite',
        'swarm',
        'shambling_sludge'
    ]
}

Object.keys(sprites).forEach(spritesFolder => {
    k.loadSprite(spritesFolder, `sprites/${spritesFolder}/${spritesFolder}.png`, {
        sliceX: 5,
        sliceY: 5
    });
    sprites[spritesFolder].forEach(spriteName => {
        k.loadSprite(spriteName, `sprites/${spritesFolder}/${spriteName}.png`);
    })
});

loadFont("jersey", "fonts/jersey.ttf");

export default k;