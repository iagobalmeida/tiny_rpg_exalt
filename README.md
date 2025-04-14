# Tiny RPG

## Instalação
```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução
```bash
cd app
source .venv/bin/activate
python main.py
```

## Todo
- [ ] Inventário
    - [X] Renderização
        - [X] Exibir quantidade
        - [X] Popover para descrição
            - [X] Ação de usar
            - [X] Ação de descartar
            - [X] Ação de descartar todos
            - [X] Detalhamento atributos
        - [X] Identificador quantidade
        - [X] Identificador "Em uso"
        - [X] Atualização condicionada
    - [ ] Classe Item, Consumivel, ConsumivelCura e Equipamento
        - [X] Cadastrar itens iniciais
        - [X] Uso de item de cura
        - [ ] Uso de item equipamento
        - [ ] Considerar atributos de equipamentos em cálculo combate
        - [ ] Exibir atributos de equipamentos em atributos jogador


- [ ] Placar de Líderes

- [ ] Banco de dados
- [ ] Criação de conta
- [ ] Verificação de e-mail

- [ ] Deploy railway
- [ ] Rate Limit