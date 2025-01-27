const playerData = {
    level: 1,
    exp: 0,
    hp: 100,
    maxHP: 100,
    gold: 10,
    dex: 10,
    att: 20
}

const regionData = {
    level: 1,
    maxLevel: 25,
    name: 'Beach',
    spriteName: 'beach'
}
const regions = {
    'beach': {
        name: 'Beach',
        spriteName: 'beach',
        enemies: {
            'bandit_leader': {
                name: 'Bandit Leader',
                hp: 60,
                maxHP: 60,
                dex: 8,
                att: 10,
                gold: 5,
                exp: 5
            },
            'pirate': {
                name: 'Pirate',
                hp: 20,
                maxHP: 20,
                dex: 16,
                att: 5,
                gold: 2,
                exp: 2,
            },
            'beached_bucaneer': {
                name: 'Beached Bucaneer',
                hp: 120,
                maxHP: 120,
                dex: 10,
                att: 15,
                gold: 25,
                exp: 15
            },
            'treachure_chest': {
                name: 'Treasure Chest',
                hp: 50,
                maxHP: 50,
                dex: 0,
                att: 0,
                gold: 100,
                exp: 0,
            },
            'dreadstump_the_pirate_king': {
                name: 'Dreadstump the Pirate King',
                hp: 1000,
                maxHP: 1000,
                dex: 25,
                att: 30,
                gold: 200,
                exp: 45,
            }
        }
    }
}


const randomInt = (base=5) => (Math.round(-1* Math.random()*base));

const calculateBattle = (player, region_name, enemy_name) => {
    const ret = []
    const enemiesData = regions[region_name].enemies
    const __enemy = {...enemiesData[enemy_name]}
    ret.push({
        action: 'battleStart',
        args: {
            playerData: {...player},
            enemyData: {...__enemy},
            regionData: {...regionData}
        }
    })

    ret.push({
        action: 'alert',
        args: {
            content: `${__enemy.name} found!`
        }
    })

    while(player.hp > 0 && __enemy.hp > 0) {
        const playerDexFactor = Math.random() * player.dex;
        const enemyDexFactor = Math.random() * __enemy.dex;
        
        if(playerDexFactor > enemyDexFactor && player.hp > 0) {
            const playerAttack = randomInt(player.att);
            __enemy.hp += playerAttack;
            ret.push({
                action: 'damageEnemy',
                args: {
                    damage: playerAttack
                }
            });
        } 
        
        if(enemyDexFactor > playerDexFactor && __enemy.hp > 0) {
            const damageEnemy = randomInt(__enemy.att);
            player.hp += damageEnemy;
            ret.push({
                action: 'damagePlayer',
                args: {
                    damage: damageEnemy
                }
            });
        }
    }

    if(player.hp > 0 && __enemy.hp <= 0) {
        regionData.level = Math.min(regionData.maxLevel, regionData.level+1);
        const gold = __enemy.gold;
        const exp = __enemy.exp;
        let message = []
        if(exp) message.push(`+${exp} EXP`)
        if(gold) message.push(`+${gold} Gold`)
        ret.push({
            action: 'alert',
            args: {
                content: message.join(' ')
            }
        });

        playerData.exp += exp;
        playerData.gold += gold;
        if(playerData.exp >= playerData.level*25) {
            playerData.exp -= playerData.level*25;
            playerData.level++;
            playerData.att += 2;
            playerData.dex += 2;
            playerData.maxHP *= 1.5;
            playerData.hp = playerData.maxHP;
            ret.push({
                action: 'alert',
                args: {
                    content: 'Level Up! +2 ATT / + 2 DEX'
                }
            });
        }

        ret.push({action: 'winPlayer', args: { playerData }});
    } else if(player.hp <= 0 && __enemy.hp > 0){ 
        ret.push({action: 'winEnemy'});
        ret.push({
            action: 'alert',
            args: {
                content: 'You died'
            }
        });
        player.hp = player.maxHP
        regionData.level = 0;
    }

    return ret;
}

const randomBattle = (regionName) => {
    if(regionName != regionData.name) {
        regionData.name = regionName;
        regionData.level = 0;
    }

    const enemiesNames = Object.keys(regions[regionName].enemies);

    const currentLevel = regionData.level;
    const maxLevel = regionData.maxLevel;

    const perc = currentLevel/maxLevel;
    const aprox = Math.floor(enemiesNames.length * perc);

    const enemyName = enemiesNames[Math.floor(Math.random()*aprox)];
    return calculateBattle(playerData, regionData.name, enemyName)
}

export default {
    calculateBattle,
    randomBattle
}