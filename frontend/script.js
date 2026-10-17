document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById('loginForm');
    let perfilLogado = ''; 

    // Referência das telas
    const telas = {
        login: document.getElementById('tela-login'),
        dashboardRec: document.getElementById('tela-dashboard'),
        cadastroRec: document.getElementById('tela-cadastro'),
        agendamentosRec: document.getElementById('tela-agendamentos'),
        configuracoesRec: document.getElementById('tela-configuracoes'),
        dashboardVet: document.getElementById('tela-dashboard-vet'),
        agendamentosVet: document.getElementById('tela-agendamentos-vet'),
        configuracoesVet: document.getElementById('tela-configuracoes-vet'),
        internacoesVet: document.getElementById('tela-internacoes-vet'),
        prontuariosVet: document.getElementById('tela-prontuarios-vet'),
        plantaoVet: document.getElementById('tela-plantao-vet')
    };

    function mostrarTela(telaNome) {
        Object.values(telas).forEach(tela => {
            if (tela) tela.style.display = 'none';
        });
        if (telas[telaNome]) telas[telaNome].style.display = 'flex';
    }

    // Login
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault(); 
            const loginValue = document.getElementById('login').value.toLowerCase();
            const senhaValue = document.getElementById('senha').value;

            if (loginValue === 'recepcionista' && senhaValue === '123') {
                perfilLogado = 'recepcionista';
                mostrarTela('dashboardRec');
            } else if (loginValue === 'veterinario' && senhaValue === '123') {
                perfilLogado = 'veterinario';
                mostrarTela('dashboardVet');
            } else {
                alert('Login ou senha incorretos.');
            }
        });
    }

    // Navegação Lateral
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const textoBotao = this.innerText.trim();
            
            if (textoBotao === 'Pagina inicial') {
                mostrarTela(perfilLogado === 'veterinario' ? 'dashboardVet' : 'dashboardRec');
            } else if (textoBotao === 'Cadastro') {
                if (perfilLogado === 'recepcionista') mostrarTela('cadastroRec');
            } else if (textoBotao === 'Agendamentos') {
                mostrarTela(perfilLogado === 'veterinario' ? 'agendamentosVet' : 'agendamentosRec');
            } else if (textoBotao === 'Configurações') {
                mostrarTela(perfilLogado === 'veterinario' ? 'configuracoesVet' : 'configuracoesRec');
            } else if (textoBotao === 'Internações') {
                if (perfilLogado === 'veterinario') mostrarTela('internacoesVet');
            } else if (textoBotao === 'Plantão') {
                if (perfilLogado === 'veterinario') mostrarTela('plantaoVet');
            }
        });
    });

    // Prontuários
    const btnProntuarios = document.querySelector('.btn-prontuarios');
    if (btnProntuarios) {
        btnProntuarios.addEventListener('click', function(e) {
            e.preventDefault();
            if (perfilLogado === 'veterinario') mostrarTela('prontuariosVet');
        });
    }

    // ================= FUNCIONALIDADE DO BLOCO DE NOTAS (PLANTÃO) =================
    const btnAdicionarPlantao = document.querySelector('.btn-adicionar-plantao');
    const blocoNotasPlantao = document.getElementById('bloco-notas-plantao');
    const btnCancelarPlantao = document.getElementById('btn-cancelar-plantao');
    const btnSalvarPlantao = document.getElementById('btn-salvar-plantao');
    const listaPlantoes = document.getElementById('lista-plantoes');
    const cardVazio = document.getElementById('card-plantao-vazio');

    // Abre o bloco de notas
    if (btnAdicionarPlantao) {
        btnAdicionarPlantao.addEventListener('click', function() {
            blocoNotasPlantao.style.display = 'flex';
        });
    }

    // Fecha e limpa o bloco de notas
    if (btnCancelarPlantao) {
        btnCancelarPlantao.addEventListener('click', function() {
            blocoNotasPlantao.style.display = 'none';
            document.getElementById('input-data-plantao').value = '';
            document.getElementById('input-info-plantao').value = '';
        });
    }

    // Salva a nota e cria o cartão
    if (btnSalvarPlantao) {
        btnSalvarPlantao.addEventListener('click', function() {
            const dataP = document.getElementById('input-data-plantao').value;
            const infoP = document.getElementById('input-info-plantao').value;

            // Validação simples
            if (dataP === '' || infoP === '') {
                alert('Por favor, preencha a data e as informações do plantão.');
                return;
            }

            // Esconde o aviso "Vazio"
            if (cardVazio) {
                cardVazio.style.display = 'none';
            }

            // Cria a formatação da data para ficar mais bonita (DD/MM/YYYY)
            const partesData = dataP.split('-');
            const dataFormatada = `${partesData[2]}/${partesData[1]}/${partesData[0]}`;

            // Cria um novo HTML para o cartão e insere no topo da lista
            const novoCard = document.createElement('div');
            novoCard.className = 'card-plantao';
            novoCard.innerHTML = `
                <div class="data-plantao">${dataFormatada}</div>
                <div class="notas-plantao">${infoP}</div>
            `;
            
            listaPlantoes.prepend(novoCard);

            // Limpa os campos e esconde o bloco de notas
            blocoNotasPlantao.style.display = 'none';
            document.getElementById('input-data-plantao').value = '';
            document.getElementById('input-info-plantao').value = '';
        });
    }

    // Função de saída
    function sairDaConta(e) {
        e.preventDefault();
        document.getElementById('login').value = '';
        document.getElementById('senha').value = '';
        perfilLogado = ''; 
        mostrarTela('login');
    }

    const btnSairRec = document.getElementById('btn-sair-conta');
    const btnSairVet = document.getElementById('btn-sair-conta-vet');
    if (btnSairRec) btnSairRec.addEventListener('click', sairDaConta);
    if (btnSairVet) btnSairVet.addEventListener('click', sairDaConta);
});

