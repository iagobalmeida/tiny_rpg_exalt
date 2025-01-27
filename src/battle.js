const playerData = {
    hp: 100,
    maxHP: 100,
    dex: 10,
    att: 20
}

const regionData = {
    name: 'Beach',
    spriteName: 'beach',
    level: 1
}

const enemiesData = {
    'bandit_leader': {
        name: 'Bandit Leader',
        hp: 60,
        maxHP: 60,
        dex: 8,
        att: 10
    },
    'pirate': {
        name: 'Pirate',
        hp: 20,
        maxHP: 20,
        dex: 16,
        att: 5
    },
    'beached_bucaneer': {
        name: 'Beached Bucaneer',
        hp: 120,
        maxHP: 120,
        dex: 10,
        att: 15
    },
    'treachure_chest': {
        name: 'Treasure Chest',
        hp: 300,
        maxHP: 300,
        dex: 0,
        att: 0
    }
}

const randomInt = (base=5) => (Math.round(-1* Math.random()*base));

const calculateBattle = (player, enemy_name) => {
    const ret = []
    const __enemy = {...enemiesData[enemy_name]}
    ret.push({
        action: 'battleStart',
        args: [
            {...player},
            {...__enemy},
            {...regionData}
        ]
    })

    ret.push({
        action: 'alert',
        args: [`${__enemy.name} found!`]
    })

    while(player.hp > 0 && __enemy.hp > 0) {
        const playerDexFactor = Math.random() * player.dex;
        const enemyDexFactor = Math.random() * __enemy.dex;
        
        if(playerDexFactor > enemyDexFactor && player.hp > 0) {
            const playerAttack = randomInt(player.att);
            __enemy.hp += playerAttack;
            ret.push({
                action: 'damageEnemy',
                args: [playerAttack]
            });
        } 
        
        if(enemyDexFactor > playerDexFactor && __enemy.hp > 0) {
            const damageEnemy = randomInt(__enemy.att);
            player.hp += damageEnemy;
            ret.push({
                action: 'damagePlayer',
                args: [damageEnemy]
            });
        }
    }

    if(player.hp > 0 && __enemy.hp <= 0) {
        ret.push({
            action: 'winPlayer', args: []
        });
        ret.push({
            action: 'alert',
            args: [`+10 EXP`]
        });
        regionData.level++;
    } else if(player.hp <= 0 && __enemy.hp > 0){ 
        ret.push({
            action: 'winEnemy', args: []
        });
        ret.push({
            action: 'alert',
            args: ['You died']
        });
        player.hp = player.maxHP
        regionData.level=1;
    }

    return ret;
}

const randomBattle = () => {
    const enemiesNames = Object.keys(enemiesData);
    const enemyName = enemiesNames[Math.floor(Math.random()*enemiesNames.length)];
    return calculateBattle(playerData, enemyName)
}

export default {
    calculateBattle,
    randomBattle,
    enemiesData,
    playerData
}