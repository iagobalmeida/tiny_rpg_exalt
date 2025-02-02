<template>
    <canvas :aria-loading="loading" id="game" v-show="playing" width="480" height="480"></canvas>
    <div :aria-loading="loading" class="info-wrapper" v-show="playing">
        <div class="info">
            <label >
                Region
                <select id="region" v-model="selectedRegion">
                    <option :selected="selectedRegion == regionIndex" v-for="(region, regionIndex) in avaiableRegions" :key="`region_${regionIndex}`" :value="regionIndex">{{region.name}}</option>
                </select>
            </label>
            <button v-on:click="explore" :disabled="!allowExplore">{{ allowExplore ? 'Explore' : '...' }}</button>
            <label for="auto-explore">
                Auto
                <input type="checkbox" v-model="autoExplore" />
            </label>
        </div>
        <div class="info">
            <label>
                Attributes
                <ul>
                    <li>
                        <span id="attribute-level">{{ playerData.level }}</span>
                        <small>LVL</small>
                    </li>
                    <li style="grid-column-start: 2;grid-column-end: 4;">
                        <span id="attribute-exp">{{ playerData.exp }}/{{ playerData.next }}</span>
                        <small>EXP</small>
                    </li>
                </ul>
                <ul>
                    <li>
                        <span id="attribute-att">{{ playerData.att }}<small>+1</small></span>
                        <small>ATT</small>
                    </li>
                    <li>
                        <span id="attribute-dex">{{ playerData.dex }}<small>+1</small></span>
                        <small>DEX</small>
                    </li>
                    <li>
                        <span id="attribute-def">{{ playerData.def }}<small>+1</small></span>
                        <small>DEF</small>
                    </li>
                </ul>
            </label>
        </div>
        <div class="info">
            <label>
                Inventory ({{inventory.length}}/10)
                <ul class="inventory">
                    <li @click="clickItem" :data-index="item_index" :class="item == null ? 'empty' : (item.active ? 'active' : '')" v-for="(item, item_index) in inventory" :key="`item_${item_index}`">
                        <template v-if="item != null">
                            <div class="item-image">
                                <img :src="`./sprites/items/${item.spriteName}`" :alt="item.spriteName">
                            </div>
                            <div class="item-description">
                                <p>{{ item.name }}</p>
                                <div class="item-attributes" v-for="(itemAttribute, itemAttribute_index) in item.attributes" :key="`item_${item_index}_attribute_${itemAttribute_index}`">
                                    <small>+{{ itemAttribute }} {{ itemAttribute_index.toUpperCase() }}</small>
                                </div>
                            </div>
                        </template>
                        <template v-else>
                            <div class="item-image">
                                <img src="/sprites/items/empty.png" alt="empty">
                            </div>
                            <div class="item-description">
                                <p>-</p>
                            </div>
                        </template>
                    </li>
                </ul>
            </label>
        </div>
        <div class="info">
            <label>
                Options
                <button class="danger" @click="logout">Logout</button>
            </label>
        </div>
    </div>
    <form :aria-loading="loading" class="info-wrapper" @submit.prevent="login" v-if="!playing">
        <p class="error" v-if="loginError">
            {{ loginError }}
        </p>
        <div class="info">
            <label >
                Username
                <input type="text" v-model="username">
            </label>
        </div>
        <div class="info">
            <label >
                Password
                <input type="password" v-model="password">
            </label>
        </div>
        <button>Play</button>
        <div class="info">
            <label>
                Options
                <button class="danger" :click="restartProgress">Restart Progress</button>
            </label>
        </div>
    </form>
  </template>
  
  <script>
import battle from './battle.js';
import { init } from './kaplayMain.js';
import { createBackground, createDamageText, createEntity, createLifeBar, createManaBar, createMessage, createProjectile, createRegionInfo } from './kaplayUtils.js';
;

  export default {
    name: 'App',
    data() {
        return {
            username: 'admin',
            password: '',
            loginError: '',
            loading: false,
            playing: false,
            forceStop: false,
            kaPlay: null,
            playerData: {
                level: 1,
                exp: 0,
                next: 0,
                att: 10,
                dex: 10,
                def: 10
            },
            inventory: [
                {
                    name: 'Iron Mail',
                    spriteName: 'iron_mail.png',
                    type: 'equip_chest',
                    active: false,
                    attributes: {
                        att: 1
                    }
                }, 
                {
                    name: 'Iron Mail',
                    spriteName: 'iron_mail.png',
                    type: 'equip_chest',
                    active: false,
                    attributes: {
                        att: 1
                    }
                },
                {
                    name: 'Short Sword',
                    spriteName: 'short_sword.png',
                    type: 'equip_weapon',
                    active: false,
                    attributes: {
                        att: 1
                    }
                }, null, null, null, null, null, null, null, null
            ],
            allowExplore: false,
            autoExplore: false,
            selectedRegion: 'beach',
            avaiableRegions: {
                'beach': { name: 'Beach' },
                'mid_plains': { name: 'Mid Plains' },
            },
            battleStep: 0,
            battleActions: [],
            player: null,
            playerLifeBar: null,
            playerManaBar: null,
            enemy: null,
            enemyLifeBar: null,
            enemyManaBar: null,
        }
    },
    methods: {
        BATTLE_START({ playerData, enemyData, regionData }) {
            this.kaPlay.destroyAll();
            createBackground(regionData.spriteName);
            createRegionInfo(regionData);
            let center = this.kaPlay.center();

            this.player = createEntity(center.x, center.y+125, 'player', playerData);
            this.playerLifeBar = createLifeBar(this.player, playerData.hp, playerData.maxHP);
            this.playerManaBar = createManaBar(this.player, playerData.mp, playerData.maxMP);

            this.enemy = createEntity(center.x, center.y-125, enemyData.name, enemyData);
            this.enemyLifeBar = createLifeBar(this.enemy, enemyData.hp, enemyData.maxHP);
            this.enemyManaBar = createManaBar(this.enemy, enemyData.mp, enemyData.maxMP);
        },
        BATTLE_ENEMY_ATTACK({ playerData, damage }) {
            createProjectile(this.enemy, this.player, { color: [255,0,0]});
            this.kaPlay.wait(0.25, () => { this.playerLifeBar.value = playerData.hp });
            this.kaPlay.wait(0.5, () => { createDamageText(this.player, damage) });
        },
        BATTLE_PLAYER_ATTACK({ enemyData, damage }) {
            createProjectile(this.player, this.enemy, {});
            this.kaPlay.wait(0.25, () => { this.enemyLifeBar.value = enemyData.hp });
            this.kaPlay.wait(0.5, () => { createDamageText(this.enemy, damage) });
        },
        BATTLE_WIN() {
            this.enemyLifeBar.destroy();
            this.enemyManaBar.destroy();
            this.enemy.destroy();
        },
        BATTLE_DIE() {
            this.playerLifeBar.destroy();
            this.playerManaBar.destroy();
            this.player.destroy();
        },
        MESSAGE({ content }) {
            createMessage(content);
        },
        restartProgress() {
        },
        explore() {
            if(this.battleStep >= this.battleActions.length) {
                createMessage('Exploring...');
                this.kaPlay.wait(0.5, () => {
                    this.battleActions = battle.randomBattle(this.selectedRegion);
                    this.battleStep = 0;
                })
            } else  {
                createMessage('Wait!');
            }
        },
        battleExecuteStep() {
            let actions = {
                'BATTLE_START': this.BATTLE_START,
                'BATTLE_ENEMY_ATTACK': this.BATTLE_ENEMY_ATTACK,
                'BATTLE_PLAYER_ATTACK': this.BATTLE_PLAYER_ATTACK,
                'BATTLE_WIN': this.BATTLE_WIN,
                'BATTLE_DIE': this.BATTLE_DIE,
                'MESSAGE': this.MESSAGE
            }
            let duration = .5;
            if(this.battleStep < this.battleActions.length) {
                this.allowExplore = false;

                const actionName = this.battleActions[this.battleStep].action;
                const actionArgs = this.battleActions[this.battleStep].args || {};
                const actionDuration = this.battleActions[this.battleStep].duration || duration;
                duration = actionDuration;
                
                actions[actionName](actionArgs);

                if(this.player && 'playerData' in actionArgs) {
                    this.playerData = actionArgs['playerData'];
                    this.playerManaBar.value = actionArgs['playerData'].mp;
                    if(actionName == 'MESSAGE') {
                        this.playerLifeBar.value = actionArgs['playerData'].hp;
                    }
                }

                if(this.enemy && 'enemyData' in actionArgs) {
                    this.enemyManaBar.value = actionArgs['enemyData'].mp;
                }

                this.battleStep++;
            } else {
                this.allowExplore = true;
                if(this.autoExplore) {
                    this.explore();
                }
            }
            if(!this.forceStop) {
                this.kaPlay.wait(duration, () => {
                    this.battleExecuteStep();
                })
            }
        },
        clickItem(e) {
            this.loading = true;
            setTimeout(() => {
                let itemIndex = e.target.getAttribute('data-index');
                if(!this.inventory[itemIndex]) return;
                let itemType = this.inventory[itemIndex].type;
                let isActivating = !this.inventory[itemIndex].active;

                this.inventory.forEach((item, index) => {
                    if(!item) return;
                    if(index == itemIndex) {
                        item.active = !item.active
                    } else {
                        item.active = isActivating ? (item.active && item.type != itemType) : item.active
                    }
                });
                this.loading = false;
            }, 1500);
        },
        login() {
            if(this.username != 'admin' || this.password != 'admin') {
                this.loginError = 'Invalid username and/or password';
                return;
            }
            this.loading = true;
            this.playing = true;
            setTimeout(() => {
                this.kaPlay = init();
                this.kaPlay.destroyAll();
                createBackground();
                this.kaPlay.wait(1, () => {
                    this.loading = false;
                    this.battleExecuteStep();
                })
            }, 1000)
        },
        logout() {
            location.reload();
        }
    }
  };
  </script>
  
  <style>
  /* Seus estilos aqui */
  </style>
  