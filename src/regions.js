function toTitleCase(str) {
    return str.replaceAll('_', ' ').replace(
      /\w\S*/g,
      text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
    );
  }
  

const factoryEnemy = (spriteName, hp, dex, att, def, exp=null) => {
    const baseFactor = Math.round((dex+att+def)/4)
    const hpFactor = Math.round(hp/baseFactor)
    const expFactor = exp != null ? exp : (baseFactor ^ 2) + hpFactor * 2;
    return {
        spriteName: spriteName,
        name: toTitleCase(spriteName),
        hp:hp,
        maxHP:hp,
        mp: 0,
        maxMP: 50+Math.round(hp/20),
        dex:dex,
        att:att,
        def:def,
        exp: expFactor
    }
}

const factoryEnemyDEX = (spriteName, factor, hp=null) => (factoryEnemy(spriteName, hp != null ? hp : 30*factor, 16*factor, 8*factor, 2*factor))
const factoryEnemyATT = (spriteName, factor, hp=null) => (factoryEnemy(spriteName, hp != null ? hp : 40*factor, 8*factor, 16*factor, 2*factor))
const factoryEnemyDEF = (spriteName, factor, hp=null) => (factoryEnemy(spriteName, hp != null ? hp : 60*factor, 2*factor, 8*factor, 8*factor))
const factoryEnemyChest = (spriteName, factor, hp=null) => (factoryEnemy(spriteName, hp != null ? hp : 30*factor, 0, 0, 0, 4*factor))

export const regions = {
    'beach': {
        level: 1,
        maxLevel: 10,
        name: 'Beach',
        spriteName: 'beach',
        enemies: [
            factoryEnemyATT('bandit_leader', 1),
            factoryEnemyDEX('pirate', 1),
            factoryEnemyDEF('beached_bucaneer', 1),
            factoryEnemyChest('treasure_chest', 1),
            factoryEnemyATT('dreadstump_the_pirate_king', 2, 500)
        ]
    },
    'mid_plains': {
        level: 1,
        maxLevel: 15,
        name: 'Mid Plains',
        spriteName: 'mid_plains',
        enemies: [
            factoryEnemyATT('big_green_slime', 2),
            factoryEnemyDEX('fire_sprite', 2),
            factoryEnemyDEX('swarm', 2),
            factoryEnemyDEF('earth_golem', 2),
            factoryEnemyChest('beach/treasure_chest', 2),
            factoryEnemyATT('shambling_sludge', 3, 1000)
        ]
    }
}


export const randomEncounter = (regionName, currentLevel) => {
    const region = regions[regionName];
    const maxIndex = Math.floor(region.enemies.length * (currentLevel/region.maxLevel));
    return region.enemies[Math.floor(Math.random()*maxIndex)];
}