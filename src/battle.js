import { regions } from './regions';

const playerData = localStorage.getItem('playerData') ? JSON.parse(localStorage.getItem('playerData')) : {
    level: 1,
    exp: 0,
    hp: 100,
    maxHP: 100,
    gold: 10,
    dex: 10,
    att: 10,
    def: 2
}

const regionData = localStorage.getItem('regionData') ? JSON.parse(localStorage.getItem('regionData')) : {
    level: 1,
    maxLevel: 25,
    name: 'Beach',
    spriteName: 'beach'
}


const randomInt = (base=5) => (-1 * (Math.round(base*0.25) + Math.round(Math.random()*base*0.75)));

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
            const playerAttack = randomInt(player.att - __enemy.def);
            __enemy.hp += playerAttack;
            ret.push({
                action: 'damageEnemy',
                args: {
                    damage: playerAttack
                }
            });
        } 
        
        if(enemyDexFactor > playerDexFactor && __enemy.hp > 0) {
            const damageEnemy = randomInt(__enemy.att - player.def);
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
            playerData.def += 2;
            playerData.maxHP += 50;
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
        regionData.level = 1;
    }

    localStorage.setItem('playerData', JSON.stringify(playerData))
    localStorage.setItem('regionData', JSON.stringify(regionData))
    return ret;
}

const randomBattle = (regionName) => {
    const targetRegion = regions[regionName] || null;
    if(!targetRegion) return [{
        action: 'alert',
        args: {
            content: 'Invalid region!'
        }
    }];

    if(targetRegion.name != regionData.name) {
        regionData.level = 1;
        regionData.name = targetRegion.name;
        regionData.spriteName = targetRegion.spriteName;
        regionData.maxLevel = targetRegion.maxLevel;
    }

    const enemiesNames = Object.keys(targetRegion.enemies);

    const currentLevel = regionData.level;
    const maxLevel = regionData.maxLevel;

    const perc = currentLevel/maxLevel;
    const aprox = Math.floor(enemiesNames.length * perc);

    const enemyName = enemiesNames[Math.floor(Math.random()*aprox)];
    return calculateBattle(playerData, regionName, enemyName)
}

export default {
    calculateBattle,
    randomBattle
}