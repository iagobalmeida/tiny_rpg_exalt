export const regions = {
    'beach': {
        level: 1,
        maxLevel: 15,
        name: 'Beach',
        spriteName: 'beach',
        enemies: {
            'bandit_leader': {
                name: 'Bandit Leader',
                hp: 60,
                maxHP: 60,
                dex: 8,
                att: 10,
                def: 1,
                gold: 5,
                exp: 5
            },
            'pirate': {
                name: 'Pirate',
                hp: 20,
                maxHP: 20,
                dex: 16,
                att: 5,
                def: 1,
                gold: 2,
                exp: 2,
            },
            'beached_bucaneer': {
                name: 'Beached Bucaneer',
                hp: 120,
                maxHP: 120,
                dex: 10,
                att: 15,
                def: 1,
                gold: 25,
                exp: 15
            },
            'treachure_chest': {
                name: 'Treasure Chest',
                hp: 50,
                maxHP: 50,
                dex: 0,
                att: 0,
                def: 1,
                gold: 100,
                exp: 0,
            },
            'dreadstump_the_pirate_king': {
                name: 'Dreadstump the Pirate King',
                hp: 500,
                maxHP: 500,
                dex: 25,
                att: 30,
                def: 1,
                gold: 200,
                exp: 45,
            }
        }
    },
    'mid_plains': {
        level: 1,
        maxLevel: 50,
        name: 'Mid Plains',
        spriteName: 'mid_plains',
        enemies: {
            'big_green_slime': {
                name: 'Big Green Slime',
                hp: 120,
                maxHP: 120,
                dex: 16,
                att: 20,
                def: 1,
                gold: 16,
                exp: 16
            },
            'earth_golem': {
                name: 'Earth Golem',
                hp: 240,
                maxHP: 240,
                dex: 18,
                att: 10,
                def: 1,
                gold: 32,
                exp: 32
            },
            'fire_sprite': {
                name: 'Fire Sprite',
                hp: 180,
                maxHP: 180,
                dex: 18,
                att: 10,
                def: 1,
                gold: 64,
                exp: 64
            },
            'swarm': {
                name: 'Swarm',
                hp: 100,
                maxHP: 100,
                dex: 22,
                att: 15,
                def: 1,
                gold: 64,
                exp: 64
            },
            'shambling_sludge': {
                name: 'Shambling Sludge',
                hp: 1200,
                maxHP: 1200,
                dex: 30,
                att: 25,
                def: 1,
                gold: 400,
                exp: 400
            }
        }
    }
}