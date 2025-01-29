export class Entity {
    constructor(k, positionX, positionY, name, data) {
        this.positionX = positionX;
        this.positionY = positionY;
        this.data = data;
        const spriteName = name.toLowerCase().replaceAll(' ','_');
        this.entity = k.add([
            k.pos(positionX, positionY),
            k.sprite(spriteName),
            k.anchor('center'),
            k.animate(),
            k.opacity(0),
            k.rotate(),
            k.scale(),
            {
                ...data
            }
        ])

        const barPositionY =this.entity.height/1.5

        this.lifeBarBackground = this.entity.add([
            k.rect(72, 8),
            k.pos(0, barPositionY),
            k.outline(3, 'black'),
            k.color(0,0,0),
            k.anchor('center')
        ])
        this.lifeBar = this.lifeBarBackground.add([
            k.rect(Math.round(data.hp*72/data.maxHP), 8),
            k.pos(-36, -4),
            k.outline(1, 'black'),
            k.color(0,255,0)
        ])

        
        this.manaBarBackground = this.entity.add([
            k.rect(72, 6),
            k.pos(0, barPositionY + 8),
            k.outline(3, 'black'),
            k.color(0,0,0),
            k.anchor('center')
        ])
        this.manaBar = this.manaBarBackground.add([
            k.rect(Math.round(data.mp*72/data.maxMP), 6),
            k.pos(-36, -3),
            k.outline(1, 'black'),
            k.color(0,0,255)
        ])

        const direction = this.entity.pos.y > k.center().y ? 1 : -1;

        k.tween(0, 1, 0.5, (v) => {
            this.entity.opacity = v;
            this.entity.pos.y = positionY + ((1 - v) * direction * 20)
        })
    }

    updateHP(k, hp) {
        this.entity.hp = hp;
        const percHP = Math.ceil(this.entity.hp*72/this.entity.maxHP)
        k.tween(this.lifeBar.width, percHP, .5, (v) => { this.lifeBar.width = v });
    }

    updateMP(k, mp) {
        this.entity.mp = mp;
        const percMP = Math.ceil(this.entity.mp*72/this.entity.maxMP)
        k.tween(this.manaBar.width, percMP, .5, (v) => { this.manaBar.width = v });
    }

    emmitAttack(k) {
        const barPositionY =this.entity.height/1.5
        const direction = this.entity.pos.y > k.center().y ? -1 : 1;
        const color = direction < 0 ? k.rgb(255, 255, 255) : k.rgb(255, 0, 0)
        k.add([
            k.rect(8,32),
            k.anchor('center'),
            k.color(color),
            k.outline(2, k.rgb(0,0,0)),
            k.pos(this.positionX, this.positionY + (direction*barPositionY)),
            k.move(k.vec2(0, direction), 240),
            k.opacity(1),
            k.lifespan(.55)
        ])
    }

    damage(k, ammount) {
        const color = k.rgb(255, 255, 255);
        if(ammount > 0) {
            color.b = 0;
            color.r = 0;
        } else if(ammount < 0) {
            color.b = 0;
            color.g = 0;
        }
        
        this.entity.add([
            k.text(`${Math.abs(ammount)}`, { font: 'jersey' }),
            k.color(color),
            k.pos(0, -20),
            k.opacity(1),
            k.lifespan(1, { fade: 0.5 }),
            k.anchor('center'),
            k.z(99),
            k.move(k.vec2(0, -1), 60),
        ]);

        this.updateHP(k, Math.min(this.entity.maxHP, this.entity.hp + ammount));
    }
    
    die(k) {
        k.tween(1, 0, 1, (v) => {
            this.entity.opacity = v;
            this.lifeBarBackground.opacity = v;
            this.manaBarBackground.opacity = v;
        });
        k.wait(1, () => {
            this.entity.destroy();
            this.lifeBarBackground.destroy();
            this.manaBarBackground.destroy();
        })
    }
}

