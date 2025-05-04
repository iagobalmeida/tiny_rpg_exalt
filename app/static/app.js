const { createApp } = Vue

function deepMerge(target, patch) {
    if (target === null || typeof target !== 'object') {
        return structuredClone(patch);
    }

    for (const key in patch) {
        const patchVal = patch[key];
        const targetVal = target[key];

        if (Array.isArray(patchVal)) {
            target[key] = [...patchVal];
        } else if (
            patchVal !== null &&
            typeof patchVal === 'object'
        ) {
            target[key] = deepMerge(targetVal, patchVal);
        } else {
            target[key] = patchVal;
        }
    }

    return target;
}

const app = createApp({
    data() {
        return {
            erroMultiplosClientes: false,
            autenticado: false,
            podeEnviarAcao: true,
            jogador: null,
            inimigo: null,
            masmorra: null,
            tamanhoInventario: 8,
            inventario: [],
            usarAutomaticoVidaNome: null,
            usarAutomaticoEnergiaNome: null,
            atributosEquipamentosJogador: null,
            messages: [],
            conexoes: {},
            missoes: [],
            nome: '',
            email: '',
            senha: '',
            audioLigado: false,
            confirmarSenha: '',
            cadastrando: false,
            conexaoAtual: null,
            placar_de_lideres: []
        }
    },
    mounted() {
        document.body.classList.remove('opacity-0');
        this.wsConnect();
    },
    computed: {
        jogadorFatorClasseNivel() {
            return this.jogador.classe.nivel ? parseInt(Math.pow(this.jogador.classe.nivel, 1.5)) : 0;
        },
        jogadorEvoluirClasseLevel() { 
            return 15 + (this.jogadorFatorClasseNivel * 30)
        },
        jogadorEvoluirClassePreco() {
            return 1500 + (this.jogadorFatorClasseNivel * 5000)
        },
        jogadorForca() {
            let ret = `${this.jogador.forca}`;
            if(this.atributosEquipamentosJogador && this.atributosEquipamentosJogador['forca']) {
                ret += `<small>+${this.atributosEquipamentosJogador['forca']}</small>`;
            }
            if(this.jogador.bonus_atributos_classe['forca']) {
                ret += ` <small>+${this.jogador.bonus_atributos_classe['forca']}</small>`;
            }
            return ret;
        },
        jogadorAgilidade() {
            let ret = `${this.jogador.agilidade}`;
            if(this.atributosEquipamentosJogador && this.atributosEquipamentosJogador['agilidade']) {
                ret += ` <small>+${this.atributosEquipamentosJogador['agilidade']}</small>`;
            }
            if(this.jogador.bonus_atributos_classe['agilidade']) {
                ret += ` <small>+${this.jogador.bonus_atributos_classe['agilidade']}</small>`;
            }
            return ret;
        },
        jogadorResistencia() {
            let ret = `${this.jogador.resistencia}`;
            if(this.atributosEquipamentosJogador && this.atributosEquipamentosJogador['resistencia']) {
                ret += ` <small>+${this.atributosEquipamentosJogador['resistencia']}</small>`;
            }
            if(this.jogador.bonus_atributos_classe['resistencia']) {
                ret += ` <small>+${this.jogador.bonus_atributos_classe['resistencia']}</small>`;
            }
            return ret;
        },
        jogadorInteligencia() {
            let ret = `${this.jogador.inteligencia}`;
            if(this.atributosEquipamentosJogador && this.atributosEquipamentosJogador['inteligencia']) {
                ret += ` <small>+${this.atributosEquipamentosJogador['inteligencia']}</small>`;
            }
            if(this.jogador.bonus_atributos_classe['inteligencia']) {
                ret += ` <small>+${this.jogador.bonus_atributos_classe['inteligencia']}</small>`;
            }
            return ret;
        },
        jogadorEstadoClasses() {
            return this.jogador ? this.jogador.estados.map(e => (e.nome.toLowerCase())) : [];
        },
        inimigoEstadoClasses() {
            return this.inimigo ? this.inimigo.estados.map(e => (e.nome.toLowerCase())) : [];
        },
        jogadorProximaMissao(){
            if(!this.jogador) return;
            for(missao_chave in this.missoes) {
                const missao = this.missoes[missao_chave];
                if(!missao['completa']) return missao;
            }
            return null;
        }
    },
    watch: {
        audioLigado() {
            document.querySelectorAll('audio').forEach(el => {
                el.volume = this.audioLigado ? 1 : 0
            });
        }
    },
    methods: {
        wsConnect() {
            const ws = new WebSocket(window.WS_URL)
            const conexaoId = Date.now().toString()
            
            ws.onopen = () => {
                this.conexoes[conexaoId] = ws
                this.conexaoAtual = conexaoId
                console.log(`Conexão ${conexaoId} estabelecida`)
            }
            
            ws.onmessage = (event) => {
                this.wsReceive(event)
            }
            
            ws.onclose = () => {
                console.log(`Conexão ${conexaoId} fechada`)
                delete this.conexoes[conexaoId]
                if (this.conexaoAtual === conexaoId) {
                    this.conexaoAtual = Object.keys(this.conexoes)[0] || null
                }
            }

            ws.onerror = (error) => {
                console.error(`Erro na conexão ${conexaoId}:`, error)
                this.erroMultiplosClientes = true;
            }
        },
        wsSend(type, data) {
            const ws = this.conexoes[this.conexaoAtual]
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: type,
                    data: data
                }))
                this.podeEnviarAcao = false
            }
        },
        wsReceive(event) {
            const data = JSON.parse(event.data)
            if(data.type == 'update') {
                this.wsAnimate(data);
            }
            if (data.type === 'update' || data.type === 'paused' || data.type == 'action_response') {
                this.wsUpdateState(data);
            }
            if(data.type == 'error') {
                this.criarToast('Erro', data.message)
            }
            this.usarAutomatico();
        },
        wsAnimateParticulas(alvo, particulas, particula_atual=0) {
            if(particula_atual >= particulas.length) return;
            const [texto, cor, sprite] = particulas[particula_atual]
            if(sprite) {
                this.criarParticulas({
                    'alvo': alvo,
                    'sprite_arquivo': `particulas/${sprite}`
                }).then((top_left) => {
                    this.criarTextoFlutuante(texto, alvo, cor, 24, top_left[0], top_left[1]).then(() => {
                            this.wsAnimateParticulas(alvo, particulas, particula_atual+1)
                        }
                    )
                })
            } else {
                this.criarTextoFlutuante(texto, alvo, cor, 24).then(() => {
                        this.wsAnimateParticulas(alvo, particulas, particula_atual+1)
                    }
                )
            }
        },
        wsAnimate(data) {
            this.wsAnimateParticulas('jogador', data.jogador_particulas ? data.jogador_particulas : []);
            this.wsAnimateParticulas('inimigo', data.inimigo_particulas ? data.inimigo_particulas : []);
        },
        wsUpdateState(data) {
            this.podeEnviarAcao = true;
            if(data.jogador) {
                if(!this.autenticado) {
                    this.autenticado = true;
                    document.querySelector('#audio_musica').play();
                    setTimeout(() => {
                        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
                        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
                    }, 250)
                }
            }
            if(data.placar_de_lideres) {
                this.placar_de_lideres = data.placar_de_lideres;
            }
            if(data.jogador){
                this.jogador = deepMerge(this.jogador, data.jogador);
            }
            if(data.inventario){
                this.inventario = data.inventario
            }
            if(data.inimigo) {
                this.inimigo = deepMerge(this.inimigo, data.inimigo);
            }
            if(data.masmorra) {
                this.masmorra = deepMerge(this.masmorra, data.masmorra);
            }
            if(data.masmorras) {
                this.masmorras = deepMerge(this.masmorras, data.masmorras);
            }
            if(data.atributos_equipamentos_jogador) {
                this.atributosEquipamentosJogador = data.atributos_equipamentos_jogador;
            }
            if(data.tamanho_inventario) {
                this.tamanhoInventario = data.tamanho_inventario;
            }
            if(data.missoes) {
                this.missoes = data.missoes;
            }
        },
        usarAutomatico() {
            if(!this.jogador) return;
            if(this.usarAutomaticoVidaNome) {
                const precisaUsar = this.jogador.vida + this.usarAutomaticoVidaFator <= this.jogador.vida_maxima || this.jogador.vida <= this.jogador.vida_maxima * 0.25;
                if(precisaUsar) {
                    const itemIndice = this.inventario.findIndex(item => item.nome == this.usarAutomaticoVidaNome);
                    if(itemIndice > 0) {
                        this.itemAcao(itemIndice, 'usar');
                    }
                }
            } 
            if(this.usarAutomaticoEnergiaNome && this.jogador.energia + this.usarAutomaticoEnergiaFator <= this.jogador.energia_maxima) {
                const precisaUsar = this.jogador.energia + this.usarAutomaticoEnergiaFator <= this.jogador.energia_maxima || this.jogador.energia <= this.jogador.energia_maxima * 0.25;
                if(precisaUsar) {
                    const itemIndice = this.inventario.findIndex(item => item.nome == this.usarAutomaticoEnergiaNome);
                    if(itemIndice > 0) {
                        this.usarAutomaticoEnergiaNome = null;
                        this.usarAutomaticoEnergiaFator = null;
                    }
                }
            } 
        },
        processarDescricaoItem(descricao) {
            return descricao.map((linha) => {
                _linha = linha.replace('ATTR_FORCA', '% <span class="material-symbols-outlined">fitness_center</span>')
                _linha = _linha.replace('ATTR_AGILIDADE', '% <span class="material-symbols-outlined">directions_run</span>')
                _linha = _linha.replace('ATTR_RESISTENCIA', '% <span class="material-symbols-outlined">shield</span>')
                _linha = _linha.replace('ATTR_INTELIGENCIA', '% <span class="material-symbols-outlined">psychology</span>')
                _linha = _linha.replace('ATTR_VIDA', '<span class="font-bold" style="color:#198754">Pontos de Vida</span>')
                _linha = _linha.replace('ATTR_ENERGIA', '<span class="font-bold" style="color:#1976d2">Pontos de Energia</span>')
                return `<span class="d-flex align-items-center gap-1 w-full mb-1">${_linha}</span>`;
            }, '').join('');
        },
        toggleCadastrando() {
            this.cadastrando = !this.cadastrando;
        },
        tocarAudio(id) {
            setTimeout(() => {
                const audio = document.querySelector(id);
                audio.pause();
                audio.currentTime = 0;
                audio.play();
            }, Math.random()*250)
        },
        itemAcao(indice, acao) {
            if(acao == 'usar_automatico') {
                const item = this.inventario[indice]
                if(item.atributo == 'vida') {
                    if(this.usarAutomaticoVidaNome == item.nome) this.usarAutomaticoVidaNome = null;
                    else {
                        this.usarAutomaticoVidaNome = item.nome;
                        this.usarAutomaticoVidaFator = item.fator;
                    }
                } else if(item.atributo == 'energia') {
                    if(this.usarAutomaticoEnergiaNome == item.nome) this.usarAutomaticoEnergiaNome = null;
                    else {
                        this.usarAutomaticoEnergiaNome = item.nome;
                        this.usarAutomaticoEnergiaFator = item.fator;
                    }
                }
            } if(acao == 'usar') {
                this.wsSend('usar_item', { item_indice: indice });
            } else if(acao == 'descartar') {
                this.wsSend('descartar_item', { item_indice: indice });
            } else if(acao == 'descartar_todos') {
                this.wsSend('descartar_item_todos', { item_indice: indice });
            }
        },
        criarToast(titulo, conteudo) {
            const toast = document.createElement('div');
            toast.classList.add('toast', 'fade', 'show');

            const header = document.createElement('div');
            header.classList.add('toast-header');
            
            const title = document.createElement('strong');
            title.innerHTML = titulo;

            const closeButton = document.createElement('button');
            closeButton.classList.add('ms-auto', 'btn');
            closeButton.setAttribute('data-bs-dismiss', 'toast');
            closeButton.innerHTML = '✖'

            const body = document.createElement('div');
            body.classList.add('toast-body');
            body.innerHTML = conteudo;

            header.appendChild(title);
            header.appendChild(closeButton);
            toast.appendChild(header);
            toast.appendChild(body);
            document.querySelector('#toast-container').appendChild(toast);
        },
        criarTextoFlutuante(texto, alvo, cor, tamanho=32, top=null, left=null) {
            return new Promise((resolve) => {
                const container = document.querySelector(`#wrapper-sprite-${alvo}`);
                const textoFlutuante = document.createElement('div');

                textoFlutuante.className = 'texto-flutuante';
                textoFlutuante.style.color = cor;
                textoFlutuante.style.fontSize = tamanho + 'px';
                textoFlutuante.textContent = texto;
                if(top == null) top = 50;
                else top -= 16;
                if(left == null) left = 25 + Math.random() * 50;

                textoFlutuante.style.top = `${top}%`;
                textoFlutuante.style.left = `${left}%`;
                container.appendChild(textoFlutuante);

                setTimeout(() => {
                    textoFlutuante.remove();
                    resolve();
                }, 1000);
            });
        },
        criarParticulas({alvo, sprite_arquivo, aleatorio=true, tamanho=1, duracao=750, opacidade=1}) {
            return new Promise((resolve) => {
                const container = document.querySelector(`#wrapper-sprite-${alvo}`);
                const elementParticula = document.createElement('div');
                const top = aleatorio ? 25 + Math.random() * 25 : 50
                const left = aleatorio ? 25 + Math.random() * 25 : 50
                elementParticula.style.top = `${top}%`;
                elementParticula.style.left = `${left}%`;
                elementParticula.classList.add('particula-dano');
                elementParticula.style.animationDuration = `${duracao}ms`;
                elementParticula.style.opacity = opacidade;
                if(tamanho != 1) {
                    elementParticula.style.transform = `translate(-50%, -50%) scale(${tamanho})`;
                }
                elementParticula.style.setProperty('--particula-sprite', `url('static/${sprite_arquivo}')`)
                container.appendChild(elementParticula);

                setTimeout(() => {
                    elementParticula.remove();
                }, duracao-50);

                setTimeout(() => {
                    resolve([top, left]);
                }, duracao/15);
            })
        },
        login() {
            if(this.cadastrando) {
                this.wsSend('signup', { nome: this.nome, email: this.email, senha: this.senha, confirmar_senha: this. confirmarSenha});
            } else {
                this.wsSend('login', { email: this.email, senha: this.senha });
            }
        },
        toggleSons() {
            this.audioLigado = !this.audioLigado;
        },
        mudarMasmorra(masmorraChave) {
            this.wsSend('mudar_masmorra', { masmorra: masmorraChave });
        },
        aumentarAtributo(atributo) {
            this.wsSend('aumentar_atributo', { atributo: atributo });
        },
        enviarAcao(acao) {
            this.wsSend('acao_jogador', { acao: acao });
        },
        subirNivelClasse(classe) {
            this.wsSend('subir_nivel_classe', { classe: classe });
        },
        spriteXClasse(nomeClasse) {
            switch(nomeClasse) {
                case 'INICIANTE':
                    return 0
                case 'VIGIA':
                    return 1
                case 'GUARDIAO':
                    return 2
                case 'PALADINO':
                    return 3
                case 'APRENDIZ':
                    return 0
                case 'MAGO':
                    return 1
                case 'FEITICEIRO':
                    return 2
                case 'ARCANO':
                    return 3
                case 'SELVAGEM':
                    return 0
                case 'BARBARO':
                    return 1
                case 'BERSERKER':
                    return 2
                case 'CAMPEAO':
                    return 3
                case 'VAGABUNDO':
                    return 0
                case 'LADINO':
                    return 1
                case 'ASSASSINO':
                    return 2
                case 'PREDADOR':
                    return 3
                default:
                    return 0
            }
        },
        spriteYClasse(nomeClasse) {
            switch(nomeClasse) {
                case 'INICIANTE':
                    return 3
                case 'VIGIA':
                    return 3
                case 'GUARDIAO':
                    return 3
                case 'PALADINO':
                    return 3
                case 'APRENDIZ':
                    return 2
                case 'MAGO':
                    return 2
                case 'FEITICEIRO':
                    return 2
                case 'ARCANO':
                    return 2
                case 'SELVAGEM':
                    return 1
                case 'BARBARO':
                    return 1
                case 'BERSERKER':
                    return 1
                case 'CAMPEAO':
                    return 1
                case 'VAGABUNDO':
                    return 0
                case 'LADINO':
                    return 0
                case 'ASSASSINO':
                    return 0
                case 'PREDADOR':
                    return 0
                default:
                    return 4
            }
        },
        comprarExpansaoInventario() {
            this.wsSend('comprar_expansao_inventario');
        }
    }
})

app.config.compilerOptions.delimiters = ['[[', ']]'];

app.mount('#app')