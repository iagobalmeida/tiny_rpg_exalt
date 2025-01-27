import kaplay from "kaplay";
import battle from "./battle";
import { Entity } from "./entity";

const k = kaplay({
    width: 480,
    height: 480
});

k.loadRoot("./"); // A good idea for Itch.io publishing later
k.loadSprite("player", "sprites/player.png");
k.loadSprite("bandit_leader", "sprites/bandit_leader.png");
k.loadSprite("pirate", "sprites/pirate.png");
k.loadSprite("beached_bucaneer", "sprites/beached_bucaneer.png");
k.loadSprite("treasure_chest", "sprites/treasure_chest.png");
k.loadSprite("dreadstump_the_pirate_king", "sprites/dreadstump_the_pirate_king.png");
k.loadSprite("beach", "sprites/beach.png", {
    sliceX: 5,
    sliceY: 5
});
loadFont("jersey", "fonts/jersey.ttf");
k.onClick(() => k.addKaboom(k.mousePos()));

const center = k.center();

const createMessage = (text, duration=1) => {
    const width = text.length * 22;
    const textBackground = k.add([
        k.rect(16 + width, 48),
        k.color(k.rgb(0,0,0)),
        k.opacity(0.5),
        k.pos(center.x, center.y+32),
        k.anchor('center'),
        k.move(k.vec2(0,-1), 50),
        k.lifespan(duration, { fade: 0.5 }),
    ])
    textBackground.add([
        k.text(text, { font: 'jersey' }),
        k.anchor('center')
    ])
    return textBackground;
}

const createBackground = (spriteName) => {
    k.addLevel([
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
    ], {
        tileHeight: 256/5,
        tileWidth: 256/5,
        tiles: {
            "1": () => [
                k.sprite(spriteName, { frame: 1})
            ]
        }
    })
}


const regionWindow = k.add([
    k.rect(0, 32),
    k.pos(12, 12),
    k.color(k.rgb(0,0,0)),
    k.opacity(0.5),
    k.z(10)
])
const regionLabel = regionWindow.add([
    k.text('', { font: 'jersey', size: 24 }),
    k.pos(6, 4),
    k.anchor('topleft')
])
const updateRegionCount = (regionName, count) => {
    regionLabel.text = `${regionName} ${count}/25`
    regionWindow.width = regionLabel.width + 16
}

const inputGold = document.querySelector('input#gold')
const updateGold = (value) => {
    inputGold.value = value;
}

const updateAtrtibutes = ({ level, exp, dex, att }) => {
    document.querySelector('#attribute-level').innerHTML = level;
    document.querySelector('#attribute-exp').innerHTML = exp;
    document.querySelector('#attribute-dex').innerHTML = dex;
    document.querySelector('#attribute-att').innerHTML = att;
}


let battleActions = []
let battleStep = 0;

let player = null;
let enemy = null;

const actions = {
    battleStart({ playerData, enemyData, regionData }) {
        createBackground(regionData.spriteName);
        updateRegionCount(regionData.name, regionData.level);
        updateAtrtibutes(playerData)
        
        if(player) player.die(k);
        player = new Entity(k, center.x, center.y+125, 'player', playerData);
        
        if(enemy) enemy.die(k);
        enemy = new Entity(k, center.x, center.y-125, enemyData.name, enemyData);

    },
    damagePlayer({ damage }) {
        player.damage(k, damage)
    },
    damageEnemy({ damage }) {
        enemy.damage(k, damage)
    },
    winPlayer({ playerData }) {
        updateGold(playerData.gold)
        updateAtrtibutes(playerData)
        enemy.die(k);
    },
    winEnemy() {
        player.die(k);
    },
    alert({ content }) {
        createMessage(content);
    }
}

k.onUpdate(() => {
    if(enemy != null) {
        enemy.updateLifebar();
    }
    if(player != null) {
        player.updateLifebar();
    }
});


const buttonExplore = document.querySelector('button#explore')

buttonExplore.addEventListener('click', () => {
    if(battleStep >= battleActions.length) {
        createMessage('Exploring...');
        battleActions = battle.randomBattle('beach');
        battleStep = 0;
    } else {
        createMessage('Wait!');
    }
})

k.loop(.5, () => {
    if(battleStep < battleActions.length) {
        buttonExplore.setAttribute('disabled', true);
        buttonExplore.innerHTML = 'Exploring...';
        const actioName = battleActions[battleStep].action;
        const args = battleActions[battleStep].args || {};
        actions[actioName](args);
        battleStep++;
    } else {
        buttonExplore.removeAttribute('disabled')
        buttonExplore.innerHTML = 'Explore';
    }
})