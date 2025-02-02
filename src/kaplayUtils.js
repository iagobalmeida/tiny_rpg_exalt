import { k } from "./kaplayMain";

export const createProgressBar = (entity, curr, max, {height=8, width=72, tweenDuration=.25, color=[0,255,0], colorSteps=[], distance=0}) => {
    let kRectBackground = k.add([
        k.rect(width, height),
        k.pos(entity.pos.x, entity.pos.y + entity.height/1.5 + distance),
        k.outline(2, 'black'),
        k.opacity(1),
        k.color(0,0,0),
        k.anchor('center')
    ]);
    let kRectForeground = kRectBackground.add([
        k.rect(Math.round(width*curr/max), height),
        k.pos(-36, -height/2),
        k.outline(2, 'black'),
        k.color(color[0], color[1], color[2]),
        {
            maxWidth: width,
            foregroundWidth: Math.round(width*curr/max),
            value: curr,
            max: max
        }
    ]);
    colorSteps = colorSteps.sort((a,b) =>(b.porc - a.porc))
    let destroy = () => {
        k.tween(1, 0, tweenDuration, (o) => { kRectBackground.opacity = o });
        k.wait(tweenDuration, () => {
            kRectBackground.destroy();
            kRectForeground.destroy();
        })
    }
    let updateColor = () => {
        if(colorSteps) {
            colorSteps.forEach(v => {
                let __porc = kRectForeground.width/kRectForeground.maxWidth
                if(__porc <= v.porc) {
                    kRectForeground.color.r = v.color[0]
                    kRectForeground.color.g = v.color[1]
                    kRectForeground.color.b = v.color[2]
                }
            });
        }
    }
    k.loop(tweenDuration, () => {
        k.tween(kRectForeground.width, kRectForeground.foregroundWidth, tweenDuration, (v) => { kRectForeground.width = v });
    })
    updateColor();
    return {
        get value() {
            return kRectForeground.value
        },
        set value(value) {
            let porc = value/kRectForeground.max
            kRectForeground.foregroundWidth = Math.min(kRectForeground.maxWidth, Math.round(kRectForeground.maxWidth*porc));
            updateColor();
        },
        destroy
    }
}

export const createLifeBar = (entity, curr, max) => {
    return createProgressBar(entity, curr, max, {
        color: [0,255,0], 
        colorSteps: [
            { porc:0.5, color: [255, 200, 0]},
            { porc:0.3, color: [255,0,0]}
        ]
    });
}

export const createManaBar = (entity, curr, max) => {
    return createProgressBar(entity, curr, max, {
        color: [0,0,255],
        distance: 8
    });
}

export const createMessage = (text, duration=1, infinite=false) => {
    let center = k.center();
    let width = text.length * 22;
    let components = [
        k.rect(16 + width, 48),
        k.color(k.rgb(0,0,0)),
        k.opacity(0.7),
        k.pos(center.x, center.y+( infinite ? 0 : 32 )),
        k.anchor('center'),
        k.z(100)
    ]
    if(!infinite) {
        components.push(k.move(k.vec2(0,-1), 50))
        components.push(k.lifespan(duration, { fade: 0.5 }))
    }
    let textBackground = k.add(components)
    textBackground.add([
        k.text(text, { font: 'jersey' }),
        k.anchor('center')
    ])
    return textBackground;
}

export const createBackground = (spriteName=null) => {
    if(spriteName == null) {
        k.add([
            k.rect(480,480),
            k.color(k.rgb(0,0,0))
        ])
        createMessage('Start Exploring', 1, true);
    } else {
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
}

export const createRegionInfo = (regionData) => {
    let regionWindow = k.add([
        k.rect(0, 32),
        k.pos(12, 12),
        k.color(k.rgb(0,0,0)),
        k.opacity(0.7),
        k.z(10)
    ])
    let regionLabel = regionWindow.add([
        k.text('', { font: 'jersey', size: 24 }),
        k.pos(6, 4),
        k.anchor('topleft')
    ])
    regionLabel.text = `${regionData.name} ${regionData.level}/${regionData.maxLevel}`
    regionWindow.width = regionLabel.width + 16
}

export const createEntity = (positionX, positionY, name) => {
    let spriteName = name.toLowerCase().replaceAll(' ', '_');
    let entity = k.add([
        k.pos(positionX, positionY),
        k.sprite(spriteName),
        k.anchor('center'),
        k.animate(),
        k.opacity(1),
        k.rotate(),
        k.scale()
    ]);
    let direction = entity.pos.y > k.center().y ? 1 : -1;
    k.tween(0, 1, 0.5, (v) => {
        entity.opacity = v;
        entity.pos.y = positionY + ((1 - v) * direction * 20)
    });
    const destroy = () => {
        k.tween(1, 0, 1, (v) => {
            entity.opacity = v;
            if(v == 1) {
                entity.destroy();
            }
        });
    }
    
    return { ...entity, destroy };
}

export function createDamageText(entity, ammount, lifeSpan=1) {
    let color = '#ffffff';
    if(ammount > 0) color = '#00ff00';
    if(ammount < 0) color = '#ff0000';
    entity.add([
        k.text(`${Math.abs(ammount)}`, { font: 'jersey' }),
        k.color(color),
        k.pos(0, -20),
        k.opacity(1),
        k.lifespan(lifeSpan, { fade: 0.5 }),
        k.anchor('center'),
        k.z(99),
        k.move(k.vec2(0, -1), 60),
    ]);
}

export function createProjectile(entity, entityTarget, { color=[255,255,255], speed=300, offset=30 }) {
    const __offset = (-1 * offset) + (Math.random()*offset*2)
    const angle = entityTarget.pos.angle(k.vec2(entity.pos.x + __offset, entity.pos.y));
    k.add([
        k.rect(8,32),
        k.anchor('center'),
        k.color(color),
        k.pos(entity.pos.x + __offset, entity.pos.y),
        k.opacity(1),
        k.lifespan(.55),
        k.z(99),
        k.rotate(angle - 90),
        k.move(angle, speed),
    ]);
}