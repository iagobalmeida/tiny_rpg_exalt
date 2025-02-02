import kaplay from 'kaplay';
import { regions } from "./regions";


export let k;

export const loadAssets = (k) => {
    k.loadRoot("./");
    k.loadSprite("player", "sprites/player.png");

    Object.keys(regions).forEach(regionName => {
        k.loadSprite(regionName, `sprites/${regionName}/${regionName}.png`, {
            sliceX: 5,
            sliceY: 5
        });
        regions[regionName].enemies.forEach(enemy => {
            if(enemy.spriteName.includes('/')) k.loadSprite(enemy.spriteName, `sprites/${enemy.spriteName}.png`);
            else k.loadSprite(enemy.spriteName, `sprites/${regionName}/${enemy.spriteName}.png`);
        })
    });

    loadFont("jersey", "fonts/jersey.ttf");
}

export const init = (canvas='#game', width=480, height=480, autoLoad=true) => {
    if(!k) {
        k = kaplay({
            width: width,
            height: height,
            canvas: document.querySelector(canvas)
        });
        if(autoLoad) {
            loadAssets(k);
        }
    }
    return k;
}

