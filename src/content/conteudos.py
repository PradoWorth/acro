# -*- coding: utf-8 -*-
"""Conteúdos: índice com busca e filtros, e as páginas individuais de artigo."""

from content.site import SITE, CATEGORIES
import build as B


ARTICLES = [
    # ------------------------------------------------------------------ 01
    {
        "slug": "custo-real-da-divida-rotativo-e-garantia-real",
        "image": "assets/img/conteudos/custo-real-da-divida-rotativo-e-garantia-real.jpg",
        "category": "Home Equity",
        "date": "2026-08-18",
        "date_label": "18 ago 2026",
        "read": "7 min",
        "title": "Trocar dívida cara por garantia real: a conta que decide, e a que engana",
        "excerpt": "A diferença de taxa entre uma linha sem garantia e uma linha com garantia real não é de pontos percentuais, é de múltiplos. Ainda assim, a migração nem sempre compensa.",
        "cta_title": "Sua dívida atual pode estar cara demais para o que ela resolve.",
        "cta_text": "Traga o saldo e a taxa da dívida atual. Avaliamos se a migração para uma estrutura com garantia real realmente compensa no seu caso.",
        "cta_primary": "Avaliar minha dívida atual",
        "sections": [
            ("A diferença que a garantia produz", [
                "Em março de 2026, o empréstimo pessoal tradicional estava em 6,67% ao mês, segundo o Banco Central. No mesmo período, levantamento divulgado pela Abecip apontava crédito com garantia de imóvel entre 1,12% e 1,80% ao mês nos 5 maiores bancos.",
                "A distância não se explica por generosidade nem por concorrência. Ela se explica por perda esperada. Em uma linha sem garantia, o credor depende de cobrança e de recuperação judicial incerta. Em uma operação com alienação fiduciária de imóvel, existe um bem identificado, registrado e executável por rito extrajudicial, com base na Lei nº 9.514/1997.",
                "Menor perda esperada permite menor preço. É uma relação econômica, não comercial. E ela funciona nos dois sentidos: o mesmo mecanismo que reduz a taxa é o que transfere ao tomador um risco patrimonial que antes não existia.",
            ]),
            ("Por que a migração nem sempre compensa", [
                "A troca de uma dívida cara por uma dívida barata parece automática no papel. Na prática, ela depende de 3 condições simultâneas, e a ausência de qualquer uma delas inverte o resultado.",
                "A primeira é saldo relevante. Custos fixos de uma operação com garantia imobiliária, como avaliação, registro em cartório, IOF e seguros, pesam proporcionalmente muito mais em valores pequenos. Abaixo de um determinado saldo, a economia de taxa não cobre o custo de contratar.",
                "A segunda é margem disponível no imóvel. O mercado costuma trabalhar com limites que chegam a 50% ou 60% do valor de avaliação, mas o que efetivamente se contrata é menor: em março de 2026, a relação média entre crédito liberado e valor do imóvel foi de 32,2%, segundo a Abecip.",
                "A terceira é capacidade de sustentar uma parcela fixa por um prazo longo. O prazo médio das operações no mesmo mês foi de 159 meses. Substituir uma dívida rotativa por um compromisso de mais de uma década muda a natureza do problema: reduz o custo mensal e amplia a duração da exposição.",
            ]),
            ("O erro mais caro: olhar a taxa e ignorar o custo efetivo", [
                "2 propostas com a mesma taxa nominal podem ter custos finais bastante diferentes. Avaliação do imóvel, emolumentos de registro, IOF, tarifa de análise e seguros obrigatórios entram no Custo Efetivo Total, e é ele que permite comparação justa entre instituições.",
                "Vale a mesma lógica na direção inversa: uma taxa ligeiramente maior com custo acessório menor pode resultar em desembolso total inferior. Quem compara apenas o percentual anunciado costuma escolher a proposta errada com convicção.",
            ]),
            ("O que checar antes de assinar", [
                "Matrícula atualizada, com certidão de ônus e sem pendência de inventário ou de averbação de construção. Documentação irregular é a causa mais frequente de operação travada depois da aprovação.",
                "Simulação em 2 prazos: o mais curto que a parcela permite e o mais longo disponível. A diferença de custo total entre eles costuma surpreender.",
                "Finalidade coerente com o prazo. Usar uma estrutura de 159 meses para cobrir um déficit de caixa recorrente não resolve o déficit: apenas o alonga e adiciona risco sobre a moradia.",
            ]),
        ],
        "sources": [
            "Abecip. Divulgação sobre crédito com garantia de imóvel no primeiro trimestre de 2026.",
            "Banco Central do Brasil. Estatísticas de taxas de juros por modalidade.",
            "Lei nº 9.514/1997. Alienação fiduciária de bem imóvel.",
        ],
    },

    # ------------------------------------------------------------------ 02
    {
        "slug": "necessidade-de-capital-de-giro",
        "image": "assets/img/conteudos/necessidade-de-capital-de-giro.jpg",
        "category": "Capital de Giro",
        "date": "2026-07-30",
        "date_label": "30 jul 2026",
        "read": "6 min",
        "title": "Lucro no papel e caixa vazio: como a necessidade de capital de giro cresce",
        "excerpt": "É possível fechar o exercício com lucro contábil e não ter caixa para o mês seguinte. Na maior parte dos casos, o motivo tem nome e tem medida.",
        "cta_title": "Sua empresa cresce e o caixa aperta na mesma proporção?",
        "cta_text": "Traga o faturamento e o ciclo de recebimento da empresa. Dimensionamos a necessidade real de capital de giro antes de indicar qualquer linha.",
        "cta_primary": "Dimensionar minha necessidade de giro",
        "sections": [
            ("A distância entre pagar e receber", [
                "Necessidade de capital de giro é o intervalo financeiro entre o desembolso e o recebimento. Ela reúne estoque comprado, produção financiada, prazo concedido a clientes, folha, tributos e despesas sazonais.",
                "Quando esse intervalo é curto, o próprio giro operacional o financia. Quando é longo, alguém precisa financiá-lo: o fornecedor, o sócio ou uma linha de crédito. A pergunta relevante não é se a empresa precisa de giro, mas quem está bancando esse intervalo hoje e a que custo.",
            ]),
            ("Por que o crescimento agrava o problema", [
                "Em expansão, a necessidade cresce de forma desproporcional à receita. Vender mais significa comprar mais estoque, financiar mais produção e, com frequência, conceder prazos maiores para conquistar clientes novos.",
                "O resultado é conhecido: uma empresa lucrativa e em crescimento pode chegar à insolvência técnica porque a linha de crédito não acompanhou a expansão do ciclo. O erro raramente está na decisão comercial. Está no dimensionamento financeiro que deveria tê-la acompanhado.",
            ]),
            ("O cenário brasileiro pressiona os dois lados", [
                "Do lado da oferta, as séries do Banco Central mostram um mercado seletivo. As concessões de capital de giro para pessoa jurídica com prazo acima de 365 dias foram de R$ 7,07 bilhões em julho de 2026, contra R$ 10,70 bilhões em junho e R$ 29,64 bilhões em dezembro de 2025, com taxa média de 23,55% ao ano no período.",
                "Vale a cautela na leitura: concessão é fluxo mensal e sofre sazonalidade forte. Uma queda entre 2 meses não indica, por si só, contração estrutural do mercado.",
                "Do lado da demanda, o quadro é mais delicado. A Serasa Experian registrou 8,9 milhões de empresas inadimplentes e R$ 213 bilhões em dívidas negativadas em dezembro de 2025, sendo 8,5 milhões de micro e pequenas empresas.",
                "Esse número tem uma consequência prática pouco discutida: parte relevante da demanda por capital de giro é, na verdade, demanda por reestruturação de passivo. As 2 coisas exigem estruturas diferentes, e tratá-las como uma só é o erro mais caro desse mercado.",
            ]),
            ("Como dimensionar antes de contratar", [
                "O cálculo começa pelos prazos médios: quantos dias o estoque permanece parado, em quantos dias a empresa recebe e em quantos dias ela paga. A diferença entre eles, aplicada ao volume de operação, dá a ordem de grandeza da necessidade.",
                "A partir daí, a estrutura correta depende do lastro disponível. Recebíveis pulverizados e bem conciliados sustentam operações melhores do que faturamento maior concentrado em poucos clientes. Para empresas elegíveis, mecanismos como Pronampe, Procred 360 e PEAC FGI reduzem a exigência de garantia real.",
                "Um cuidado permanece válido em qualquer cenário: crédito não corrige margem negativa. Se a operação consome caixa porque perde dinheiro em cada venda, o problema é operacional, e financiá-lo apenas aumenta a perda potencial.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Sistema Gerenciador de Séries Temporais, concessões e taxas de crédito.",
            "Serasa Experian. Indicadores de inadimplência empresarial, dezembro de 2025.",
        ],
    },

    # ------------------------------------------------------------------ 03
    {
        "slug": "auto-equity-prazo-e-depreciacao",
        "image": "assets/img/conteudos/auto-equity-prazo-e-depreciacao.jpg",
        "category": "Auto Equity",
        "date": "2026-07-09",
        "date_label": "9 jul 2026",
        "read": "5 min",
        "title": "Auto equity: o prazo importa mais do que a taxa",
        "excerpt": "A modalidade transforma um veículo quitado em liquidez rápida. O risco não está na velocidade, está em contratar um prazo que a curva de depreciação não sustenta.",
        "cta_title": "Quer transformar um veículo quitado em capital, sem errar o prazo?",
        "cta_text": "Traga o veículo e o valor que pretende captar. Avaliamos o prazo que cabe na curva de depreciação antes de qualquer proposta.",
        "cta_primary": "Avaliar meu veículo como garantia",
        "sections": [
            ("Não confunda com financiamento de veículo", [
                "No financiamento, o crédito compra o veículo e o próprio bem garante a compra. No auto equity, o veículo já pertence ao tomador, está quitado ou tem margem disponível, e passa a lastrear um empréstimo de uso livre.",
                "A base legal é a alienação fiduciária de bens móveis, prevista na Lei nº 4.728/1965. O proprietário mantém posse e uso enquanto o gravame é registrado junto ao Detran.",
            ]),
            ("O que a taxa nominal esconde", [
                "Um imóvel se valoriza ou oscila. Um veículo perde valor de forma previsível e acelerada. Isso impõe um limite que não existe nas operações imobiliárias: o prazo do contrato precisa caber sob a curva de depreciação do bem.",
                "Quando a amortização é mais lenta do que a perda de valor, o saldo devedor pode superar o próprio veículo. A partir desse ponto, o tomador carrega uma dívida maior do que a garantia, e o credor carrega um colateral que não cobre a exposição. Ninguém sai bem dessa configuração.",
                "Por isso, o indicador relevante não é a taxa anunciada, e sim o Custo Efetivo Total confrontado com o ritmo de depreciação. Em operações de valor menor, vistoria, tarifas, IOF e seguro pesam proporcionalmente mais e podem alterar bastante a comparação.",
            ]),
            ("O que não existe: uma estatística pública isolada", [
                "Não há série do Banco Central que separe auto equity de outras operações com garantia móvel. Números de concessão para aquisição de veículos, como os R$ 22,98 bilhões registrados em julho de 2026, medem financiamento de compra, e não empréstimo garantido por veículo já existente.",
                "Qualquer estimativa que apresente o volume de financiamento como “tamanho do mercado de auto equity” está misturando 2 coisas distintas. É uma limitação da estatística pública, e vale dizê-la em vez de contorná-la com um número aproximado.",
            ]),
            ("Quando faz sentido, e quando não faz", [
                "Faz sentido para necessidade de liquidez de curto ou médio prazo, quando o custo do crédito pessoal sem garantia seria proibitivo e a janela da oportunidade não comporta o rito de uma operação imobiliária.",
                "Não faz sentido como substituto de capital de giro estrutural. Financiar necessidade recorrente com um ativo que deprecia rápido é um erro de prazo, não de produto. Nesses casos, a avaliação correta passa por giro dimensionado ou por garantia imobiliária.",
                "Um ponto adicional de atenção: uso profissional intensivo, como aplicativo, frota ou transporte, acelera a depreciação e altera a liquidez de revenda, o que restringe tanto o prazo quanto o percentual liberável.",
            ]),
        ],
        "sources": [
            "Lei nº 4.728/1965. Alienação fiduciária de bens móveis.",
            "Banco Central do Brasil. Séries de concessão para aquisição de veículos por pessoas físicas.",
            "B3. Informações do mercado de financiamento de veículos e Sistema Nacional de Gravames.",
        ],
    },

    # ------------------------------------------------------------------ 04
    {
        "slug": "marco-das-garantias-o-que-mudou",
        "image": "assets/img/conteudos/marco-das-garantias-o-que-mudou.jpg",
        "category": "Estratégia Financeira",
        "date": "2026-06-24",
        "date_label": "24 jun 2026",
        "read": "6 min",
        "title": "Marco das Garantias: o que mudou para quem usa imóvel como lastro",
        "excerpt": "A Lei nº 14.711/2023 e sua regulamentação tornaram o patrimônio imobiliário um colateral mais eficiente. Eficiência maior não significa risco menor para o tomador.",
        "cta_title": "Seu imóvel já foi usado como garantia em outra operação?",
        "cta_text": "Desde a Lei nº 14.711/2023, pode haver margem para uma nova operação em determinadas condições. Avaliamos o seu caso à luz da regra atual.",
        "cta_primary": "Avaliar a margem do meu imóvel",
        "sections": [
            ("O que a lei alterou", [
                "A Lei nº 14.711/2023 aprimorou as regras de garantias e disciplinou mecanismos extrajudiciais de execução de créditos imobiliários, alterando dispositivos da Lei nº 9.514/1997, entre outras normas.",
                "A regulamentação posterior permitiu que um mesmo imóvel seja utilizado em mais de uma operação quando existe margem disponível. Na prática, um bem parcialmente financiado ou já dado em garantia pode voltar a gerar crédito sem que a operação anterior precise ser liquidada.",
            ]),
            ("Por que isso importa economicamente", [
                "O patrimônio imobiliário brasileiro é grande e historicamente subutilizado como colateral. Quando cada imóvel só podia lastrear uma operação por vez, boa parte da margem disponível ficava ociosa.",
                "A mudança melhora a eficiência do ativo e a previsibilidade da recuperação para o credor. Execução mais previsível reduz perda esperada, e perda esperada menor tende a se refletir em preço.",
                "O crescimento observado no mercado é coerente com isso. As concessões de crédito com garantia de imóvel somaram R$ 3,166 bilhões no primeiro trimestre de 2026, alta de 25,83% sobre o mesmo período anterior, segundo a Abecip. Em 2025, o total foi de R$ 11,5 bilhões, algo próximo de 3,5% dos R$ 324 bilhões movimentados pelo crédito imobiliário naquele ano.",
            ]),
            ("O que a mudança exige de controle", [
                "Operações sucessivas sobre o mesmo bem exigem rigor em prioridade de garantia, avaliação, registro, consentimento e efeitos de vencimento cruzado. A margem precisa ser calculada sobre valor de avaliação atualizado, não sobre expectativa.",
                "Do lado do tomador, a atenção é outra: a possibilidade de reutilizar margem torna mais fácil comprometer o mesmo bem 2 vezes. Facilidade de contratação e adequação da decisão são coisas diferentes.",
                "Execução extrajudicial mais previsível melhora a recuperação do credor. Ela não elimina risco de preço, de liquidez, de litígio nem de custo operacional, e não reduz em nada a consequência prática para quem oferece a moradia como lastro.",
            ]),
            ("O que continua valendo", [
                "Capacidade de pagamento demonstrada por fluxo, e não por patrimônio. Garantia forte melhora as condições da operação; ela não substitui a análise de quem paga a parcela todo mês.",
                "Coerência entre finalidade e prazo. E a leitura completa do custo efetivo, que inclui avaliação, emolumentos, IOF e seguros, antes de comparar qualquer proposta.",
            ]),
        ],
        "sources": [
            "Lei nº 14.711/2023. Marco Legal das Garantias.",
            "Banco Central do Brasil. Regulamentação sobre uso de imóvel em mais de uma operação.",
            "Abecip. Concessões de crédito com garantia de imóvel, primeiro trimestre de 2026.",
        ],
    },

    # ------------------------------------------------------------------ 05
    {
        "slug": "scd-sep-e-a-natureza-do-credor",
        "image": "assets/img/conteudos/scd-sep-e-a-natureza-do-credor.jpg",
        "category": "Crédito PJ",
        "date": "2026-06-02",
        "date_label": "2 jun 2026",
        "read": "5 min",
        "title": "SCD, SEP, banco ou cooperativa: por que a natureza do credor muda o seu contrato",
        "excerpt": "2 propostas com a mesma taxa podem se comportar de formas muito diferentes ao longo do contrato. Boa parte dessa diferença está em quem financia o financiador.",
        "cta_title": "Recebeu propostas de instituições diferentes e não sabe qual pesa mais?",
        "cta_text": "Traga as propostas em mãos. Comparamos por Custo Efetivo Total e pela natureza de cada credor, não só pela taxa anunciada.",
        "cta_primary": "Comparar minhas propostas",
        "sections": [
            ("De onde vem o dinheiro do credor", [
                "Sociedades de Crédito Direto operam com capital próprio. Isso tende a produzir maior previsibilidade de condições quando o cenário aperta, porque o apetite não depende diretamente da disposição de terceiros.",
                "Sociedades de Empréstimo entre Pessoas intermediam recursos de investidores. Podem oferecer condições muito competitivas quando há apetite forte, com maior sensibilidade a mudanças de cenário.",
                "Bancos universais trazem funding diversificado e relacionamento. Cooperativas têm política própria e presença regional relevante. Fintechs competem em jornada, velocidade e distribuição. Nenhuma dessas categorias é superior em abstrato.",
            ]),
            ("A pergunta correta não é qual é a melhor", [
                "É qual delas se comporta melhor no prazo e no cenário da operação em questão. Para uma necessidade pontual de curto prazo, a melhor condição de hoje resolve. Para uma necessidade recorrente que será renovada, previsibilidade vale mais do que o melhor número do primeiro contrato.",
                "Uma taxa promocional de entrada que não se sustenta na recontratação pode custar mais, ao longo de 3 renovações, do que uma condição inicial ligeiramente pior e estável.",
            ]),
            ("O que comparar além da taxa", [
                "Custo Efetivo Total, com IOF, tarifas, seguros e demais encargos. É o único indicador que permite comparação justa entre instituições de naturezas diferentes.",
                "Condições acessórias: exigência de reciprocidade, manutenção de saldo médio, cláusulas de vencimento antecipado cruzado e restrição a novo endividamento. Contratos com essas cláusulas podem inviabilizar a operação seguinte.",
                "Perfil de amortização. Uma parcela menor com prazo maior não é automaticamente melhor; depende de quanto tempo a empresa quer carregar a exposição e de como o fluxo de caixa se comporta ao longo dele.",
            ]),
            ("Mecanismos públicos mudam a estrutura possível", [
                "Pronampe, Procred 360 e PEAC FGI reduzem a exigência de garantia real para empresas elegíveis, o que amplia o conjunto de instituições dispostas a analisar a operação.",
                "Enquadramento não é aprovação. A análise de crédito da instituição continua valendo integralmente, e os critérios dos programas são revisados periodicamente. Verificar elegibilidade antes de estruturar evita expectativa mal calibrada.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Regulamentação de SCD e SEP e estatísticas de crédito.",
            "FEBRABAN. Panorama do Mercado de Crédito.",
        ],
    },

    # ------------------------------------------------------------------ 06
    {
        "slug": "construcao-financiada-liberacao-por-medicao",
        "image": "assets/img/conteudos/construcao-financiada-liberacao-por-medicao.jpg",
        "category": "Construção",
        "date": "2026-05-14",
        "date_label": "14 mai 2026",
        "read": "7 min",
        "title": "Construção financiada: o que a liberação por medição exige antes da primeira obra",
        "excerpt": "Numa obra, o ativo é construído com o próprio crédito. Isso transforma orçamento, cronograma e responsabilidade técnica em elementos da estrutura financeira.",
        "cta_title": "Vai construir e precisa que o desembolso acompanhe a obra?",
        "cta_text": "Traga o cronograma e o orçamento do projeto. Avaliamos a estrutura de liberação por medição que se aplica ao seu caso.",
        "cta_primary": "Avaliar meu projeto de obra",
        "sections": [
            ("Comprar pronto e construir são operações distintas", [
                "Na aquisição, o crédito é liberado contra um bem que já existe e pode ser avaliado hoje. Na construção, o bem passa a existir com o próprio recurso, e o credor libera contra avanço físico verificado por vistoria.",
                "Essa diferença traz para dentro da operação financeira elementos que, em outra estrutura, ficariam restritos à execução: orçamento detalhado, cronograma físico-financeiro, licenciamento e responsabilidade técnica com ART ou RRT durante toda a obra.",
                "Durante o período de obra, o encargo incide sobre o valor já liberado, sem amortização de principal. A amortização começa depois da conclusão, o que preserva fluxo no período mais intenso de desembolso.",
            ]),
            ("O risco principal não é a taxa", [
                "É o descasamento entre orçamento e valor de venda. Insumos, mão de obra, licenciamento, atraso, distrato e velocidade de vendas abaixo do previsto consomem margem antes que o custo financeiro apareça no resultado.",
                "Atraso custa 2 vezes: estende o período de incidência do encargo sobre o valor liberado e adia o início dos repasses. O fluxo é comprimido pelos dois lados simultaneamente.",
                "Financiar o limite de um orçamento sem folga transfere qualquer variação de custo para aporte próprio não planejado, normalmente no pior momento do ciclo.",
            ]),
            ("O que acompanhar durante a operação", [
                "Velocidade de vendas sobre oferta, custo por unidade, estoque de terrenos, percentual de obra concluída, repasses, distratos e cobertura de juros. São esses indicadores, e não o volume lançado, que dizem se o cronograma financeiro tem folga.",
                "Vale para o mercado inteiro. A pesquisa nacional da CBIC apontou 453.005 unidades lançadas nos 12 meses até o quarto trimestre de 2025, alta de 10,6%, com VGL de R$ 292,3 bilhões. As vendas subiram 5,4%, para 426,2 mil unidades. Volume recorde e rentabilidade não são sinônimos, especialmente com custo financeiro elevado.",
            ]),
            ("Terreno e obra: separados ou em contrato único", [
                "O contrato único de aquisição de terreno e construção tende a reduzir custo cartorário e a simplificar a estrutura de garantia. Em contrapartida, exige projeto suficientemente maduro no momento da contratação.",
                "Contratos separados dão mais flexibilidade de prazo entre a compra e o início da obra, ao custo de duplicar emolumentos e de expor a operação a mudança de condição entre uma etapa e outra.",
                "Não existe resposta única. A comparação correta considera custo total, maturidade do projeto, prazo entre aquisição e início de obra, e a política da instituição para cada estrutura.",
            ]),
        ],
        "sources": [
            "CBIC. Indicadores do mercado imobiliário nacional, quarto trimestre de 2025.",
            "Caixa Econômica Federal. Linhas de financiamento para construção e aquisição.",
            "BNDES. Finem, itens financiáveis em projetos de investimento.",
        ],
    },

    # ------------------------------------------------------------------ 07
    {
        "slug": "comprar-a-vista-ou-financiar",
        "image": "assets/img/conteudos/comprar-a-vista-ou-financiar.jpg",
        "category": "Imóveis",
        "date": "2026-04-21",
        "date_label": "21 abr 2026",
        "read": "5 min",
        "title": "Comprar à vista ou financiar: a conta do capital imobilizado",
        "excerpt": "Pagar à vista elimina o custo financeiro e cria outro, menos visível. Para quem tem operação em crescimento, imobilizar caixa costuma ser a decisão mais cara das 2.",
        "cta_title": "Na dúvida entre pagar à vista ou financiar?",
        "cta_text": "Traga o valor do imóvel e o retorno que o capital gera hoje na empresa. Fazemos essa conta com os números reais do seu caso.",
        "cta_primary": "Fazer essa conta com meu caso",
        "sections": [
            ("O custo que não aparece no contrato", [
                "Quem paga à vista não tem juros. Tem custo de oportunidade: o retorno que aquele capital deixaria de gerar dentro da operação, no estoque, na expansão ou em uma aquisição melhor.",
                "A comparação correta não é entre juros e zero. É entre o Custo Efetivo Total da operação e o retorno marginal do capital na atividade do comprador, dentro do mesmo horizonte de tempo.",
                "Para uma empresa com giro apertado e demanda em crescimento, imobilizar caixa em um imóvel raramente é a alocação mais eficiente disponível. Para quem não tem uso alternativo produtivo para o recurso, a conta pode se inverter.",
            ]),
            ("O que entra na conta além da taxa", [
                "Seguros obrigatórios, tarifas, avaliação, emolumentos de registro e IOF quando aplicável. Em prazos longos, esses componentes deixam de ser detalhe.",
                "Limite de comprometimento de renda ou de geração de caixa, que restringe o valor financiável independentemente do valor do imóvel.",
                "Enquadramento no sistema pretendido. Regras como a de não possuir outro financiamento ativo no Sistema Financeiro de Habitação podem eliminar alternativas antes de qualquer simulação.",
            ]),
            ("Uma estrutura intermediária que costuma ser esquecida", [
                "Comprar à vista e, depois, mobilizar o imóvel como garantia para recompor o caixa é uma alternativa viável em alguns casos. Ela combina poder de negociação na compra com liquidez posterior.",
                "O custo dessa combinação inclui a operação de garantia real completa: avaliação, registro e encargos. Só compensa quando o desconto obtido na compra à vista supera esse custo, o que exige medir o desconto real, não o desconto anunciado.",
            ]),
            ("Como decidir sem depender de intuição", [
                "Monte os 2 cenários com números reais: desembolso total à vista contra desembolso total financiado, no mesmo horizonte, incluindo todos os custos acessórios.",
                "Estime o retorno do capital dentro da operação de forma conservadora. Se o retorno esperado só supera o custo do crédito no cenário otimista, a resposta prudente é pagar à vista.",
                "Considere a liquidez. Capital imobilizado em imóvel não está disponível para a próxima oportunidade nem para o próximo aperto de caixa, e essa indisponibilidade tem valor econômico próprio.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Séries de concessão de financiamento imobiliário e taxas por modalidade.",
            "Caixa Econômica Federal. Condições e prazos de linhas habitacionais.",
        ],
    },

    # ------------------------------------------------------------------ 08
    {
        "slug": "como-conseguir-credito-para-a-empresa",
        "image": "assets/img/conteudos/como-conseguir-credito-para-a-empresa.jpg",
        "category": "Crédito PJ",
        "date": "2026-08-25",
        "date_label": "25 ago 2026",
        "read": "7 min",
        "title": "Como conseguir crédito para a empresa: documentos, prazo e o que pesa na análise",
        "excerpt": "Não existe um passo a passo universal, mas existe uma ordem que reduz recusa e acelera aprovação: dimensionar antes de pedir, organizar documento antes de simular, comparar custo antes de assinar.",
        "cta_title": "Pronto para dimensionar o crédito certo para a sua empresa?",
        "cta_text": "Traga o motivo da busca e os números da empresa. A leitura técnica é gratuita e não gera compromisso.",
        "cta_primary": "Avaliar meu caso",
        "sections": [
            ("Comece pelo motivo, não pela linha", [
                "A pergunta \"como conseguir crédito para minha empresa\" costuma vir antes da pergunta certa, que é: para financiar o quê. Capital de giro cobre o intervalo entre pagar e receber. Financiamento amarra o crédito a um bem específico, com prazo casado ao bem. Crédito com garantia real reduz custo em troca de comprometer um ativo.",
                "Escolher a modalidade errada não é só uma questão de nome. Um giro de curto prazo contratado como financiamento longo alonga desnecessariamente a exposição. Um financiamento de equipamento contratado como rotativo custa mais do que precisaria.",
            ]),
            ("Os documentos que toda instituição pede", [
                "Contrato social ou estatuto consolidado, com o CNPJ ativo. Faturamento comprovado, por nota fiscal ou por extrato. Balanço patrimonial e demonstrativo de resultado, quando a empresa os produz. Relação de dívidas vigentes, incluindo saldo, vencimento e credor. E, quando há garantia envolvida, a documentação do ativo oferecido.",
                "Empresas menores, como MEI e microempresas, costumam ter um checklist mais enxuto em programas como Pronampe e Procred 360, que usam dados de faturamento já declarados à Receita Federal em vez de pedir demonstrativos completos.",
            ]),
            ("O que pesa na análise, além do documento", [
                "Capacidade de pagamento demonstrada por fluxo de caixa. Qualidade e liquidez da garantia oferecida, quando há uma. Histórico de crédito. Coerência entre a finalidade declarada e o prazo pedido. E o enquadramento nas políticas internas da instituição, que variam de banco para banco mesmo para o mesmo produto.",
                "Em operações empresariais, pesam também a concentração de receita em poucos clientes e a composição do endividamento atual. Duas empresas com o mesmo faturamento podem receber propostas bem diferentes por causa desses dois fatores.",
            ]),
            ("Programas que podem facilitar o enquadramento", [
                "Pronampe, Procred 360 e o PEAC FGI existem para reduzir a exigência de garantia real de empresas elegíveis, ampliando o conjunto de instituições dispostas a analisar a operação. Nenhum dos três garante aprovação: eles mudam o risco percebido pelo banco, não substituem a análise dele.",
            ]),
            ("Erros que atrasam ou derrubam um pedido", [
                "Recebível já cedido em outra operação, oferecido de novo como se estivesse livre. Documentação desatualizada, principalmente matrícula de imóvel e contrato social. Prazo pedido incompatível com a finalidade declarada. E buscar uma única instituição, quando taxa e condição variam bastante entre bancos para o mesmo perfil de risco.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Resolução CMN nº 4.881, Custo Efetivo Total em operações de crédito.",
            "Ministério do Empreendedorismo. Programas de crédito para micro e pequenas empresas.",
        ],
    },

    # ------------------------------------------------------------------ 09
    {
        "slug": "como-calcular-necessidade-de-capital-de-giro",
        "image": "assets/img/conteudos/como-calcular-necessidade-de-capital-de-giro.jpg",
        "category": "Capital de Giro",
        "date": "2026-08-29",
        "date_label": "29 ago 2026",
        "read": "6 min",
        "title": "Como calcular a necessidade de capital de giro da empresa",
        "excerpt": "A conta não exige balanço auditado nem planilha complexa. Três prazos médios, aplicados ao custo operacional diário, já dão uma ordem de grandeza para negociar de posição melhor.",
        "cta_title": "Já calculou e quer confirmar se o número faz sentido?",
        "cta_text": "Traga os 3 prazos médios e o custo operacional da empresa. Revisamos a conta e indicamos a estrutura compatível.",
        "cta_primary": "Revisar meu cálculo",
        "sections": [
            ("Os 3 prazos que compõem a conta", [
                "Prazo médio de estoque: quantos dias, em média, a mercadoria fica parada antes de ser vendida. Prazo médio de recebimento: quantos dias a empresa leva para receber depois de vender. Prazo médio de pagamento: quantos dias a empresa leva para pagar seus fornecedores.",
                "A diferença entre o que a empresa recebe depois e o que ela paga antes é o que define se o giro operacional se autofinancia ou se alguém precisa bancar esse intervalo.",
            ]),
            ("A fórmula, em termos simples", [
                "Ciclo financeiro = prazo médio de estoque + prazo médio de recebimento, menos prazo médio de pagamento. Quanto maior esse número, maior o intervalo que a empresa precisa financiar com capital próprio ou com crédito.",
                "Para transformar dias em valor, multiplica-se o ciclo financeiro pelo custo operacional médio diário da empresa. O resultado é uma ordem de grandeza, não um número exato: ele não substitui uma análise financeira completa, mas já é suficiente para chegar a uma conversa de crédito sabendo quanto pedir.",
            ]),
            ("Um exemplo simplificado", [
                "Uma empresa com prazo médio de estoque de 45 dias, prazo médio de recebimento de 30 dias e prazo médio de pagamento de 20 dias tem um ciclo financeiro de 55 dias. Se o custo operacional médio dela é de R$ 4 mil por dia, a necessidade de giro estimada fica perto de R$ 220 mil.",
                "Esse exemplo é ilustrativo. Concentração de clientes, sazonalidade e margem real de cada operação mudam a leitura, e é isso que uma análise individual verifica antes de qualquer proposta.",
            ]),
            ("Por que o número não é fixo", [
                "O ciclo financeiro se move junto com o negócio. Em expansão, mais vendas significam mais estoque comprado e, com frequência, prazos maiores concedidos a clientes novos, o que alonga o ciclo exatamente no momento em que o caixa já está mais apertado. O artigo sobre por que a necessidade de giro cresce mais rápido que a receita detalha esse mecanismo.",
            ]),
            ("O que fazer com o resultado", [
                "Com a ordem de grandeza em mãos, o próximo passo é escolher o lastro: recebíveis, duplicatas, aval, fiança ou garantia real, dependendo do que a empresa tem disponível. Para empresas elegíveis, Pronampe, Procred 360 e o PEAC FGI reduzem a exigência de garantia real e vale verificar o enquadramento antes de procurar uma linha convencional.",
            ]),
        ],
        "sources": [
            "Sebrae. Orientações sobre gestão de capital de giro para pequenos negócios.",
            "Banco Central do Brasil. Séries de concessão e taxas de capital de giro para pessoa jurídica.",
        ],
    },

    # ------------------------------------------------------------------ 10
    {
        "slug": "documentos-para-solicitar-credito-empresarial",
        "image": "assets/img/conteudos/documentos-para-solicitar-credito-empresarial.jpg",
        "category": "Crédito PJ",
        "date": "2026-09-02",
        "date_label": "2 set 2026",
        "read": "6 min",
        "title": "Documentos para solicitar crédito empresarial: o checklist antes de procurar um banco",
        "excerpt": "Organizar a documentação antes da primeira conversa costuma valer mais do que negociar taxa depois. Veja o que instituições financeiras pedem, e por que a ordem de apresentação importa.",
        "cta_title": "Já reuniu a documentação e quer saber o próximo passo?",
        "cta_text": "Traga o que já tem organizado. Revisamos antes de levar a proposta ao mercado, para não perder tempo com pendência.",
        "cta_primary": "Revisar minha documentação",
        "sections": [
            ("Documentos societários e cadastrais", [
                "Contrato social ou estatuto consolidado, com todas as alterações, e CNPJ ativo. Documentos de identificação dos sócios ou do representante legal. Procuração, quando alguém assina em nome da empresa sem constar como sócio.",
            ]),
            ("Documentos financeiros", [
                "Faturamento comprovado, por nota fiscal ou por extrato bancário dos últimos meses. Balanço patrimonial e demonstrativo de resultado, quando a empresa os produz regularmente. Relação de dívidas vigentes, com saldo devedor, vencimento e credor de cada uma: é esse documento que permite diferenciar demanda por capital novo de demanda por reestruturação de passivo.",
            ]),
            ("Documentos da garantia, quando houver", [
                "Matrícula atualizada e certidão de ônus, para garantia de imóvel. Documento do veículo, para auto equity. Contrato ou nota que comprove o recebível oferecido em cessão. Documentação incompleta ou desatualizada é a causa mais comum de operação que trava depois de já aprovada.",
            ]),
            ("Por que MEI e microempresa têm um checklist mais enxuto", [
                "Pronampe e Procred 360 usam dados de faturamento já declarados à Receita Federal, compartilhados pelos canais oficiais como o e-CAC, em vez de exigir balanço e demonstrativos completos. Isso reduz a burocracia para quem se enquadra, mas não elimina a análise de crédito da instituição financeira.",
            ]),
            ("Antes de enviar qualquer coisa", [
                "Confirme se cada documento está dentro da validade. Verifique se um recebível já não está comprometido em outra operação, porque um mesmo ativo não pode lastrear duas operações ao mesmo tempo. E reúna tudo antes da primeira conversa: apresentar a documentação completa de uma vez costuma acelerar a resposta mais do que qualquer negociação de taxa.",
            ]),
        ],
        "sources": [
            "Receita Federal do Brasil. Perguntas frequentes sobre o Pronampe.",
            "Banco Central do Brasil. Regulamentação de operações de crédito empresarial.",
        ],
    },

    # ------------------------------------------------------------------ 11
    {
        "slug": "pronampe-quem-pode-solicitar",
        "image": "assets/img/conteudos/pronampe-quem-pode-solicitar.jpg",
        "category": "Programas Públicos",
        "date": "2026-09-04",
        "date_label": "4 set 2026",
        "read": "6 min",
        "title": "Pronampe: quem pode solicitar, como funciona e como se preparar",
        "excerpt": "Linha de capital de giro do governo federal com garantia do FGO, pensada para reduzir a exigência de garantia real de negócios menores. Veja o público, os limites e o que revisar antes de contratar.",
        "cta_title": "Quer saber se a sua empresa se enquadra no Pronampe?",
        "cta_text": "Traga o faturamento e o tempo de CNPJ da empresa. Verificamos o enquadramento antes de qualquer proposta.",
        "cta_primary": "Simular meu limite no Pronampe",
        "cta_href": "pronampe-2026.html",
        "sections": [
            ("O que é o Pronampe", [
                "O Programa Nacional de Apoio às Microempresas e Empresas de Pequeno Porte é uma linha de capital de giro com garantia do FGO, o Fundo Garantidor de Operações, criada pela Lei nº 13.999/2020. O FGO cobre parte do risco da operação junto ao banco, o que reduz a exigência de garantia real do lado da empresa.",
            ]),
            ("Quem pode solicitar", [
                "MEI, microempresas e empresas de pequeno porte com faturamento anual de até R$ 4,8 milhões. O Ministério do Empreendedorismo mantém o programa em operação, com condições especiais previstas para empresas lideradas por mulheres, conforme as regras vigentes.",
            ]),
            ("Valor, taxa e prazo", [
                "O valor pode chegar a 50% do faturamento anual da empresa, com teto de R$ 500 mil por CNPJ. A taxa é a Selic vigente mais 6% ao ano, sem tarifa de crédito ou seguro embutidos. O prazo vai até 96 meses, com carência de até 24 meses. Como a taxa é pós-fixada, a parcela real varia ao longo do contrato conforme a Selic muda a cada reunião do Copom.",
            ]),
            ("Como funciona a contratação", [
                "A solicitação é feita diretamente na instituição financeira participante escolhida pela empresa. O compartilhamento dos dados de faturamento com o banco ocorre pelos canais oficiais, como o e-CAC. Renegociação de parcelas em atraso também deve ser tratada diretamente com a instituição financeira responsável pela operação, e não com terceiros.",
            ]),
            ("Como se preparar antes de procurar o banco", [
                "Reúna o contrato social, o CNPJ ativo e o comprovante de faturamento antes da primeira conversa. Como a taxa pós-fixada e a política de crédito variam por banco, vale simular em mais de uma instituição antes de decidir. Nosso simulador de Pronampe, Procred 360 e PEAC FGI dá uma estimativa rápida de valor, taxa e parcela para comparar cenários.",
                "Empresas com faturamento mensal declarado acima de R$ 60 mil e sem restrições ativas nos órgãos de proteção ao crédito podem simular o limite diretamente na <a href=\"../pronampe-2026.html\">página dedicada ao Pronampe 2026</a>.",
            ]),
        ],
        "sources": [
            "Ministério do Empreendedorismo. Pronampe.",
            "Lei nº 13.999/2020.",
            "Receita Federal do Brasil. Perguntas frequentes sobre o Pronampe.",
        ],
    },

    # ------------------------------------------------------------------ 12
    {
        "slug": "procred-360-publico-e-documentos",
        "image": "assets/img/conteudos/procred-360-publico-e-documentos.jpg",
        "category": "Programas Públicos",
        "date": "2026-09-06",
        "date_label": "6 set 2026",
        "read": "5 min",
        "title": "Procred 360: público, documentos e como contratar",
        "excerpt": "Linha mais recente entre os programas públicos, com uma das taxas mais baixas e concessão apoiada em dados de faturamento já declarados à Receita Federal. Veja o público e os limites.",
        "cta_title": "Quer saber se a sua empresa se enquadra no Procred 360?",
        "cta_text": "Traga o faturamento declarado e o porte da empresa. Verificamos o enquadramento e os documentos exigidos.",
        "cta_primary": "Verificar meu enquadramento",
        "sections": [
            ("O que é o Procred 360", [
                "Criado pela Lei nº 14.995/2024, o Procred 360 é descrito pelo Ministério do Empreendedorismo como alternativa de crédito para empreendedores que não foram bem atendidos pelo Pronampe. Ele é mais recente e mais estreito em público do que o Pronampe, com foco em MEI e microempresas.",
            ]),
            ("Quem pode solicitar", [
                "MEI e microempresas com faturamento anual de até R$ 360 mil. É um público mais restrito do que o do Pronampe, que vai até R$ 4,8 milhões de faturamento anual.",
            ]),
            ("Valor, taxa e prazo", [
                "O valor pode chegar a 30% do faturamento anual declarado, com o teto de R$ 150 mil por CNPJ. Empresas com o selo Mulher Empreendedora podem acessar até 50% do faturamento. A taxa é de 5% ao ano mais a Selic diária, uma das mais baixas entre os programas públicos. O prazo vai até 60 meses, com carência inicial conforme o contrato, e a garantia é do FGO.",
            ]),
            ("Procred 360 ou Pronampe: como decidir", [
                "Para quem tem faturamento acima de R$ 360 mil, o Procred 360 nem entra em questão: só o Pronampe se aplica. Dentro do público elegível a ambos, o Procred 360 tende a compensar por ter taxa mais baixa, mas o teto de valor é bem mais estreito. A escolha, na prática, depende de quanto a empresa precisa captar, não só da taxa.",
            ]),
            ("Como contratar", [
                "A contratação é feita diretamente nas instituições financeiras participantes, com o faturamento verificado pelos canais oficiais de compartilhamento de dados. Como taxa pós-fixada e condição variam por banco, vale comparar mais de uma instituição antes de assinar.",
            ]),
        ],
        "sources": [
            "Ministério do Empreendedorismo. Procred360.",
            "Lei nº 14.995/2024.",
        ],
    },

    # ------------------------------------------------------------------ 13
    {
        "slug": "garantia-para-credito-empresarial",
        "image": "assets/img/conteudos/garantia-para-credito-empresarial.jpg",
        "category": "Garantias",
        "date": "2026-09-08",
        "date_label": "8 set 2026",
        "read": "6 min",
        "title": "Garantia para crédito empresarial: tipos, custo e risco real",
        "excerpt": "Garantia não é sinônimo de aprovação automática, e ausência de garantia não é sinônimo de crédito mais fácil. Veja os tipos mais usados e o que cada um muda na operação.",
        "cta_title": "Tem um bem disponível e não sabe se vale a pena oferecer em garantia?",
        "cta_text": "Traga o tipo de bem e o valor aproximado. Avaliamos o que ele realmente muda na condição da operação.",
        "cta_primary": "Avaliar minha garantia",
        "sections": [
            ("Garantia real e garantia pessoal", [
                "Garantia real vincula um bem específico à operação: imóvel, veículo ou recebíveis. Ela costuma reduzir o custo da linha, porque reduz a perda esperada do credor, mas compromete o bem em caso de inadimplência. Garantia pessoal, como aval e fiança, estende o risco da operação ao patrimônio de quem avaliza ou afiança, sem vincular um bem determinado.",
            ]),
            ("Recebíveis e duplicatas", [
                "É a garantia mais comum em capital de giro, por não exigir um bem imóvel ou móvel específico. O cuidado principal é a dupla cessão: um recebível já comprometido em outra operação não pode lastrear uma nova, e mapear o que já está cedido evita a reprovação depois de semanas de processo.",
            ]),
            ("Fundos garantidores públicos", [
                "Vale separar três mecanismos que costumam ser confundidos. O FGO, Fundo Garantidor de Operações, é a garantia usada no Pronampe e no Procred 360. O FGI Tradicional é um produto perene do BNDES para complementação de garantias em operações diversas. Já o PEAC FGI é um programa com vigência determinada por lei, que cobre entre 10% e 80% do risco da operação, a critério do banco. Nenhum dos três é uma linha de crédito por si só: todos garantem parte do risco de uma operação contratada com um banco ou agente financeiro.",
            ]),
            ("O que uma garantia não faz", [
                "Garantia não elimina a dívida em caso de inadimplência, ela só define o que acontece depois dela. Também não substitui a análise de crédito, e não é aprovação automática, mesmo quando o mecanismo é um fundo garantidor público.",
            ]),
            ("Como decidir o que oferecer", [
                "A qualidade e a liquidez do lastro pesam mais do que o valor nominal do bem. E cláusulas acessórias como domicílio bancário obrigatório, cessão fiduciária e reforço de garantia mudam o risco real da operação, mesmo quando o preço parece igual entre duas propostas.",
            ]),
        ],
        "sources": [
            "BNDES. BNDES FGI.",
            "BNDES. FGI PEAC.",
            "Banco Central do Brasil. Fundos garantidores.",
        ],
    },

    # ------------------------------------------------------------------ 14
    {
        "slug": "bndes-para-empresas-como-funciona",
        "image": "assets/img/conteudos/bndes-para-empresas-como-funciona.jpg",
        "category": "Programas Públicos",
        "date": "2026-09-09",
        "date_label": "9 set 2026",
        "read": "6 min",
        "title": "BNDES para empresas: como funciona e quais linhas existem",
        "excerpt": "O BNDES não é uma linha única de crédito. É o banco de fomento por trás de várias linhas de repasse, cada uma com finalidade, prazo e forma de acesso diferentes.",
        "cta_title": "Quer saber qual linha do BNDES se aplica à sua empresa?",
        "cta_text": "Traga a finalidade do recurso, seja giro, equipamento ou obra. Indicamos a linha de repasse compatível.",
        "cta_primary": "Verificar linha compatível",
        "sections": [
            ("O banco de fomento, não uma linha única", [
                "Quem procura crédito pela primeira vez costuma perguntar pela taxa do BNDES, como se fosse um produto padronizado. Na prática, o BNDES é o banco de fomento por trás de várias linhas de repasse, cada uma com finalidade, teto e prazo próprios. Entre as mais conhecidas para empresas estão o Finame, voltado a máquinas e equipamentos, o Finem, para projetos de investimento maiores, e o Cartão BNDES, usado em compras a fornecedores cadastrados.",
            ]),
            ("Acesso indireto, por bancos credenciados", [
                "Na maior parte dos casos, o BNDES não contrata diretamente com quem não é grande empresa. O acesso é indireto, por bancos e financeiras credenciados, chamados de agentes financeiros. É esse agente quem analisa o crédito, define parte da taxa e assina o contrato com a empresa. Isso muda a lógica de comparação: duas empresas com o mesmo porte podem ter condições diferentes de BNDES conforme o banco escolhido.",
            ]),
            ("Por que a taxa varia tanto entre bancos", [
                "A taxa final de uma operação via BNDES é composta por três fatores: o custo do próprio BNDES, o spread do BNDES e o spread do agente financeiro repassador. Os dois primeiros são padronizados pelo banco de fomento, mas o spread do agente financeiro varia conforme a instituição, o relacionamento bancário da empresa e o risco da operação. É esse terceiro componente que explica por que cotar com mais de um banco costuma mudar o resultado.",
            ]),
            ("O que cada linha financia", [
                "Máquinas, equipamentos, obras e projetos de expansão são o núcleo do financiamento via BNDES, e o Cartão BNDES amplia esse escopo para insumos e serviços de fornecedores cadastrados. O prazo também varia por linha: de alguns anos, nas operações mais simples, até prazos longos, em projetos de investimento de maior porte.",
            ]),
            ("Como se preparar antes de cotar", [
                "Como a condição final depende do agente financeiro escolhido, o passo mais útil antes de procurar um banco é ter claro qual é a finalidade do crédito, o valor necessário e o histórico bancário da empresa organizado. Isso não garante aprovação nem taxa melhor, mas evita perder tempo cotando uma linha que não corresponde à finalidade real da operação.",
            ]),
        ],
        "sources": [
            "BNDES. Financiamento e garantias para empresas.",
            "BNDES. BNDES Finame.",
            "BNDES. Cartão BNDES.",
        ],
    },

    # ------------------------------------------------------------------ 15
    {
        "slug": "fgi-tradicional-x-fgi-peac",
        "image": "assets/img/conteudos/fgi-tradicional-x-fgi-peac.jpg",
        "category": "Garantias",
        "date": "2026-09-10",
        "date_label": "10 set 2026",
        "read": "5 min",
        "title": "FGI Tradicional x FGI PEAC: as diferenças entre os dois fundos",
        "excerpt": "Os dois nomes aparecem juntos com frequência e cobrem situações diferentes. Um é permanente, o outro tem vigência determinada por lei. Veja o que muda na prática.",
        "cta_title": "Não sabe se sua operação se enquadra no FGI Tradicional ou no FGI PEAC?",
        "cta_text": "Traga o porte e a finalidade da operação. Verificamos qual fundo garantidor se aplica ao seu caso.",
        "cta_primary": "Verificar qual fundo se aplica",
        "sections": [
            ("Dois fundos, dois propósitos", [
                "FGI Tradicional e FGI PEAC são citados com frequência como se fossem a mesma coisa, mas cobrem situações diferentes. Nenhum dos dois é uma linha de crédito por si só: ambos garantem parte do risco de uma operação contratada com um banco ou agente financeiro, reduzindo a exigência de garantia real da empresa.",
            ]),
            ("FGI Tradicional: produto permanente do BNDES", [
                "O FGI Tradicional é um produto perene do BNDES, sem prazo de encerramento definido, usado para complementação de garantias em operações diversas de financiamento. Ele funciona como um reforço: a empresa oferece a garantia que tem, e o fundo completa a diferença até o percentual exigido pelo banco.",
            ]),
            ("FGI PEAC: programa com vigência determinada", [
                "O PEAC FGI é um programa com vigência determinada por lei, voltado a micro, pequenas e médias empresas, cooperativas e associações com faturamento anual de até R$ 300 milhões. Ele cobre entre 10% e 80% do risco da operação, a critério do banco, para valores de R$ 1 mil a R$ 10 milhões por CNPJ por instituição financeira, com teto médio regulatório de 1,75% ao mês e prazo de até 96 meses.",
            ]),
            ("O que muda na prática para a empresa", [
                "A diferença mais relevante para quem está solicitando crédito não é o nome do fundo, e sim se o programa está em vigência e se o banco escolhido opera com ele. Um agente financeiro pode oferecer FGI Tradicional para uma linha e não operar com PEAC FGI para outra, e isso muda o percentual de garantia disponível e o processo de contratação.",
            ]),
            ("Nenhum dos dois garante aprovação", [
                "Um fundo garantidor reduz o risco de quem empresta, não substitui a análise de crédito. A aprovação final continua dependendo do enquadramento da empresa, do relacionamento bancário e da política de crédito de cada instituição financeira.",
            ]),
        ],
        "sources": [
            "BNDES. BNDES FGI.",
            "BNDES. FGI PEAC.",
        ],
    },

    # ------------------------------------------------------------------ 16
    {
        "slug": "capital-de-giro-pronampe-procred-360-ou-bndes",
        "image": "assets/img/conteudos/capital-de-giro-pronampe-procred-360-ou-bndes.jpg",
        "category": "Estratégia Financeira",
        "date": "2026-09-10",
        "date_label": "10 set 2026",
        "read": "6 min",
        "title": "Capital de giro, Pronampe, Procred 360 ou BNDES: como decidir",
        "excerpt": "Cada alternativa responde a uma necessidade diferente. Antes de comparar taxa, vale entender o que cada uma financia e para qual porte de empresa ela foi desenhada.",
        "cta_title": "Ainda em dúvida entre as alternativas para financiar o giro?",
        "cta_text": "Traga o porte da empresa e o valor que pretende captar. Comparamos as alternativas e indicamos a que se aplica ao seu caso.",
        "cta_primary": "Comparar as alternativas para o meu caso",
        "sections": [
            ("Comece pela finalidade, não pela taxa", [
                "É comum comparar Pronampe, Procred 360 e BNDES só pela taxa anunciada, mas cada um responde a uma necessidade diferente. Capital de giro cobre o descompasso entre pagar fornecedores e receber de clientes. Pronampe e Procred 360 são linhas de capital de giro do governo federal com regras de elegibilidade específicas. O BNDES, na maior parte das linhas, financia investimento: máquinas, equipamentos e projetos de expansão, não o giro do dia a dia.",
            ]),
            ("Pronampe: MEI e pequeno porte, teto de R$ 500 mil", [
                "O Pronampe é voltado a MEI, microempresas e empresas de pequeno porte com faturamento anual de até R$ 4,8 milhões. O valor máximo chega a 50% do faturamento anual, com teto de R$ 500 mil por CNPJ, taxa de Selic vigente mais 6% ao ano e prazo de até 96 meses. A garantia, em regra, é do FGO, sem exigência de garantia real.",
            ]),
            ("Procred 360: foco em MEI e microempresas menores", [
                "O Procred 360 é mais recente e mais restrito em porte: MEI e microempresas com faturamento anual de até R$ 360 mil. O valor máximo é 30% do faturamento declarado, chegando a 50% com o selo Mulher Empreendedora, com teto de R$ 150 mil, taxa de 5% ao ano mais Selic diária e prazo de até 60 meses. Para quem se enquadra nos dois tetos, o Procred 360 costuma ter taxa mais baixa, mas limite de valor menor.",
            ]),
            ("BNDES: quando a necessidade é investimento", [
                "Se a necessidade é comprar uma máquina, ampliar a estrutura ou financiar um projeto de expansão, o BNDES tende a ser mais adequado do que uma linha de capital de giro, mesmo que a taxa final dependa do agente financeiro escolhido. Não é uma alternativa a Pronampe ou Procred 360: é uma resposta a um tipo diferente de necessidade.",
            ]),
            ("Como decidir sem comparar só a taxa", [
                "Verifique primeiro se a empresa se enquadra no teto de faturamento de cada programa, depois se o valor necessário cabe no teto de cada um, e só então compare taxa e prazo entre as opções elegíveis. Nenhuma dessas linhas garante aprovação automática: a decisão final é sempre da instituição financeira, após análise do perfil de crédito da empresa.",
            ]),
        ],
        "sources": [
            "Ministério do Empreendedorismo. Pronampe.",
            "Ministério do Empreendedorismo. Procred360.",
            "BNDES. Financiamento e garantias para empresas.",
        ],
    },

    # ------------------------------------------------------------------ 17
    {
        "slug": "pedido-de-credito-negado-o-que-fazer",
        "image": "assets/img/conteudos/pedido-de-credito-negado-o-que-fazer.jpg",
        "category": "Estratégia Financeira",
        "date": "2026-09-11",
        "read": "6 min",
        "date_label": "11 set 2026",
        "title": "Pedido de crédito negado: o que fazer antes de tentar de novo",
        "excerpt": "Uma negativa não é sempre sobre a empresa não ter direito ao crédito. Muitas vezes é sobre o pedido ter sido feito na linha errada, no banco errado ou sem o enquadramento certo.",
        "cta_title": "Teve um pedido de crédito negado recentemente?",
        "cta_text": "Traga o que foi negado e por qual instituição. Avaliamos o que pode ter pesado antes de tentar de novo.",
        "cta_primary": "Entender minha negativa",
        "sections": [
            ("Nem toda negativa quer dizer a mesma coisa", [
                "Uma proposta de crédito pode ser negada por motivos bem diferentes: restrição cadastral, enquadramento fora do perfil da linha escolhida, documentação incompleta, garantia insuficiente ou política interna do banco para o setor da empresa. Tentar de novo sem entender qual desses motivos pesou tende a repetir o mesmo resultado.",
            ]),
            ("Restrição cadastral não é sempre definitiva", [
                "Pendências em nome da empresa ou dos sócios pesam na análise, mas nem toda restrição impede crédito. O primeiro passo é levantar o que exatamente está pendente, quando venceu e se já foi regularizado. Uma restrição antiga e já quitada tem peso diferente de uma pendência em aberto.",
            ]),
            ("A linha pode não ser a certa para o perfil da empresa", [
                "Um pedido de Pronampe fora do teto de faturamento, ou uma linha de BNDES cotada com um banco que não opera bem com o porte da empresa, é recusado por enquadramento, não por risco de crédito. Rever se a linha escolhida realmente corresponde ao porte, ao faturamento e à finalidade do crédito costuma resolver mais casos do que insistir na mesma linha em outro banco.",
            ]),
            ("Garantia insuficiente tem solução objetiva", [
                "Quando a negativa é por falta de garantia, vale mapear o que a empresa tem disponível (recebíveis não comprometidos, bens que possam ser oferecidos) e verificar se algum fundo garantidor público, como FGO, FGI Tradicional ou PEAC FGI, se aplica ao caso antes de tentar de novo com a mesma proposta.",
            ]),
            ("Antes de tentar outro banco", [
                "Reorganize a documentação, confirme o enquadramento na linha certa e resolva o que for regularizável, porque um segundo pedido malfeito em outro banco também tende a ser negado. Nenhuma reorganização documental garante aprovação, mas um pedido bem-enquadrado tem uma chance de análise mais justa do que uma repetição do erro anterior.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Resolução CMN nº 4.881, Custo Efetivo Total em operações de crédito.",
        ],
    },

    # ------------------------------------------------------------------ 18
    {
        "slug": "como-comparar-credito-empresarial-pelo-cet",
        "image": "assets/img/conteudos/como-comparar-credito-empresarial-pelo-cet.jpg",
        "category": "Estratégia Financeira",
        "date": "2026-09-11",
        "read": "5 min",
        "date_label": "11 set 2026",
        "title": "Como comparar alternativas de crédito empresarial pelo CET",
        "excerpt": "A taxa anunciada nem sempre é o que a empresa paga de fato. O Custo Efetivo Total reúne juros, tarifas e seguros embutidos em um único número comparável.",
        "cta_title": "Tem mais de uma proposta e não sabe qual é realmente mais barata?",
        "cta_text": "Traga as propostas em mãos. Comparamos pelo Custo Efetivo Total, não só pela taxa anunciada.",
        "cta_primary": "Comparar minhas propostas pelo CET",
        "sections": [
            ("Por que a taxa anunciada engana na comparação", [
                "Duas propostas com a mesma taxa de juros podem ter custo final bem diferente, porque tarifa de crédito, seguro embutido e outras cobranças acessórias não aparecem na taxa anunciada. Comparar só o número da taxa costuma levar a escolher a proposta mais cara sem perceber.",
            ]),
            ("O que é o Custo Efetivo Total", [
                "O CET, Custo Efetivo Total, é o indicador regulado pelo Banco Central que reúne juros, tarifas, seguros e demais encargos de uma operação de crédito em uma taxa anual única. Ele existe justamente para tornar propostas de bancos diferentes comparáveis em um único número, e sua divulgação é obrigatória nas operações de crédito.",
            ]),
            ("Onde encontrar o CET de uma proposta", [
                "O CET deve constar do contrato e da proposta de crédito antes da contratação. Se uma proposta não apresenta o CET de forma clara, vale pedir explicitamente antes de comparar com outra, porque comparar taxa nominal de uma com CET de outra distorce a análise.",
            ]),
            ("Programas públicos também têm CET", [
                "Pronampe, Procred 360 e PEAC FGI têm taxa regulada e mais previsível, mas isso não elimina a necessidade de checar o CET quando a operação é feita junto a um banco, porque tarifas de manutenção de conta ou seguros associados ainda podem ser cobrados conforme a política de cada instituição.",
            ]),
            ("Como usar o CET numa comparação real", [
                "Reúna as propostas de mais de um banco, confirme que o CET de cada uma está expresso na mesma base (anual), e compare o número final, não só a taxa de juros isolada. Prazo e carência também mudam o custo total ao longo do contrato, então vale olhar o CET junto com essas duas variáveis, não isoladamente.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Resolução CMN nº 4.881, Custo Efetivo Total em operações de crédito.",
        ],
    },

    # ------------------------------------------------------------------ 19
    {
        "slug": "linhas-bndes-capital-de-giro-finame-cartao",
        "image": "assets/img/conteudos/linhas-bndes-capital-de-giro-finame-cartao.jpg",
        "category": "Programas Públicos",
        "date": "2026-09-11",
        "read": "5 min",
        "date_label": "11 set 2026",
        "title": "Linhas do BNDES para empresas: Finame, Finem e Cartão BNDES",
        "excerpt": "O BNDES reúne linhas com finalidades diferentes sob o mesmo nome. Entender a diferença entre elas evita cotar a linha errada para a necessidade real da empresa.",
        "cta_title": "Não sabe se precisa de Finame, Finem ou Cartão BNDES?",
        "cta_text": "Traga a finalidade do recurso. Indicamos qual linha do BNDES se aplica, sem cotar a linha errada.",
        "cta_primary": "Verificar a linha certa",
        "sections": [
            ("Por que separar as linhas antes de cotar", [
                "Como o BNDES é acessado por meio de bancos credenciados, chegar a um agente financeiro já sabendo qual linha corresponde à necessidade real da empresa evita perder tempo com uma cotação que não se aplica ao caso. As três linhas mais relevantes para empresas de menor porte são Finame, Finem e Cartão BNDES.",
            ]),
            ("Finame: máquinas e equipamentos", [
                "O Finame financia a compra de máquinas e equipamentos novos, nacionais e credenciados. É a linha mais indicada quando a necessidade é ampliar ou modernizar a capacidade produtiva da empresa, e o bem financiado costuma servir como parte da garantia da operação.",
            ]),
            ("Finem: projetos de investimento maiores", [
                "O Finem é voltado a projetos de investimento de maior porte, como expansão de estrutura, obras e projetos com valor mais elevado. Por isso o processo de análise tende a ser mais detalhado, exigindo um projeto ou plano de investimento mais estruturado do que o exigido para Finame.",
            ]),
            ("Cartão BNDES: compras a fornecedores cadastrados", [
                "O Cartão BNDES funciona como um limite rotativo para compras de insumos, materiais e serviços diretamente com fornecedores previamente cadastrados no programa. É a linha mais simples de operar entre as três, mas fica restrita aos fornecedores que participam do cadastro.",
            ]),
            ("Como decidir qual linha cotar", [
                "Se a necessidade é comprar um equipamento específico, o caminho natural é o Finame. Se é um projeto de expansão maior, o Finem. Se é reposição recorrente de insumos com fornecedores já cadastrados, o Cartão BNDES tende a ser mais ágil. Em todos os casos, a taxa final e a aprovação dependem do agente financeiro escolhido, não só da linha.",
            ]),
        ],
        "sources": [
            "BNDES. BNDES Finame.",
            "BNDES. BNDES Finem.",
            "BNDES. Cartão BNDES.",
        ],
    },

    # ------------------------------------------------------------------ 20
    {
        "slug": "como-funciona-o-compartilhamento-de-faturamento-no-e-cac",
        "image": "assets/img/conteudos/como-funciona-o-compartilhamento-de-faturamento-no-e-cac.jpg",
        "category": "Programas Públicos",
        "date": "2026-09-12",
        "read": "5 min",
        "date_label": "12 set 2026",
        "title": "Como funciona o compartilhamento de faturamento no e-CAC",
        "excerpt": "Pronampe e Procred 360 usam faturamento já declarado à Receita Federal. Entenda o que isso significa na prática, e o que nenhuma instituição séria vai pedir para acessar esse dado.",
        "cta_title": "Quer saber se sua empresa se enquadra em Pronampe ou Procred 360?",
        "cta_text": "O enquadramento parte do faturamento já declarado à Receita Federal. Verificamos isso com você, sem pedir senha nem procuração.",
        "cta_primary": "Verificar meu enquadramento",
        "sections": [
            ("Por que o e-CAC aparece na contratação", [
                "O e-CAC é o Centro Virtual de Atendimento da Receita Federal, o canal oficial onde uma empresa consulta suas próprias informações fiscais, incluindo o faturamento declarado. Pronampe e Procred 360 usam esse dado já declarado para calcular o valor elegível de cada empresa, em vez de exigir uma nova comprovação de faturamento a cada linha solicitada.",
            ]),
            ("O que a autorização realmente compartilha", [
                "Quando uma empresa contrata um desses programas, ela autoriza que a instituição financeira consulte o faturamento já declarado à Receita Federal, através de um mecanismo oficial de compartilhamento de dados entre o governo e o sistema financeiro. Não é um envio de documento novo: é uma autorização para consultar um dado que já existe.",
            ]),
            ("Onde essa autorização acontece", [
                "A autorização é feita pelo responsável legal da empresa, com seu próprio acesso gov.br, diretamente no ambiente oficial do banco ou do e-CAC, nunca por meio de terceiros. Nenhuma etapa legítima desse processo pede para a empresa compartilhar login, senha ou código de acesso com outra pessoa ou empresa, incluindo consultorias e intermediários.",
            ]),
            ("O que a Acrópole nunca vai pedir", [
                "A Acrópole Capital não solicita login, senha, token ou qualquer credencial de acesso ao gov.br, ao e-CAC ou ao internet banking da empresa em nenhuma etapa do processo. O papel de uma estruturação de crédito é organizar a documentação, identificar o programa e a instituição adequados, e acompanhar a negociação, nunca acessar sistemas oficiais em nome do cliente.",
            ]),
            ("Se alguém pedir sua senha, desconfie", [
                "Qualquer contato, mensagem ou ligação pedindo senha, código de verificação ou acesso remoto ao computador para 'liberar' um crédito é sinal de fraude, e deve ser reportado à instituição financeira e à Receita Federal. Autorização de dado, nesse tipo de programa, é sempre feita pelo próprio responsável legal da empresa, no canal oficial, sem intermediação de terceiros.",
            ]),
        ],
        "sources": [
            "Receita Federal do Brasil. Perguntas frequentes sobre o Pronampe.",
            "Governo Federal. Portal gov.br, acesso e segurança da conta.",
        ],
    },

    # ------------------------------------------------------------------ 21
    {
        "slug": "credito-empresarial-como-funciona",
        "image": "assets/img/conteudos/credito-empresarial-como-funciona.jpg",  # foto enviada pelo cliente (Pexels, licença livre) — 3 pessoas revisando documentos numa mesa de reunião
        "category": "Crédito PJ",
        "date": "2026-09-18",
        "date_label": "18 set 2026",
        "read": "6 min",
        "title": "Crédito empresarial: como funciona, na prática",
        "excerpt": "Antes de comparar taxa ou escolher instituição, vale entender o mecanismo: o que o credor avalia, de onde vem o dinheiro emprestado e por que 2 empresas com o mesmo faturamento recebem propostas diferentes.",
        "cta_title": "Ainda não sabe por onde começar a buscar crédito para a empresa?",
        "cta_text": "Traga o motivo da busca e o faturamento da empresa. Explicamos o caminho antes de qualquer proposta.",
        "cta_primary": "Entender meu caminho",
        "faq": [
            ("Crédito empresarial e empréstimo para CNPJ são a mesma coisa?",
             "Na prática, sim: \"empréstimo para CNPJ\" costuma ser o termo usado por quem busca no Google, e \"crédito empresarial\" é o termo mais amplo, que inclui também linhas de investimento, garantia e programas públicos."),
            ("Empresa recém-aberta consegue crédito empresarial?",
             "Consegue, mas com um universo de linhas menor, porque a maior parte da análise depende de histórico. Programas com regras próprias e operações com garantia real tendem a ser mais acessíveis nesse estágio do que crédito sem garantia."),
            ("Existe um valor mínimo de faturamento para buscar crédito empresarial?",
             "Não existe um piso único: cada instituição e cada linha tem sua própria faixa de faturamento elegível. É por isso que comparar a proposta de mais de uma instituição, em vez de assumir que a primeira recusa vale para todas, costuma mudar o resultado."),
        ],
        "sections": [
            ("O que o termo cobre", [
                "\"Crédito empresarial\" é o nome genérico para qualquer operação de crédito contratada em nome da pessoa jurídica: capital de giro, financiamento de equipamento ou obra, antecipação de recebíveis, linha com garantia real e programas públicos como Pronampe ou BNDES. O que muda entre eles é a finalidade, o prazo, a exigência de garantia e o órgão ou instituição por trás da linha.",
                "Quem busca \"crédito para empresa\" no Google geralmente está numa de duas situações: já sabe qual finalidade precisa cobrir, ou só sabe que precisa de dinheiro e ainda não decidiu qual caminho seguir. A confusão entre as opções é o motivo mais comum de perder tempo com a linha errada.",
            ]),
            ("De onde vem o dinheiro", [
                "3 fontes respondem pela maior parte do crédito empresarial disponível no Brasil: bancos e financeiras privadas, com recursos próprios e regras de aprovação próprias; instituições que operam linhas de fomento, como o BNDES, com recursos direcionados e taxa regulada; e fundos de investimento ou securitizadoras, que compram recebíveis ou estruturam operações fora do sistema bancário tradicional.",
                "A origem do recurso explica parte da diferença de taxa e de exigência entre propostas. Uma linha de fomento com recurso direcionado costuma ter taxa mais previsível e regras de enquadramento mais rígidas. Uma linha de banco com recurso próprio tem mais flexibilidade de negociação, e a taxa reflete o risco que o próprio banco decide assumir.",
            ]),
            ("O que o credor avalia antes de propor uma taxa", [
                "Toda instituição financeira parte de um conjunto parecido de informações: o histórico de crédito da empresa e dos sócios no Sistema de Informações de Crédito (SCR) do Banco Central, alimentado mensalmente pelos bancos e consultável gratuitamente pela própria empresa via Registrato; o histórico de pagamento no Cadastro Positivo, que hoje inclui pessoa jurídica de forma automática, desde a Lei Complementar nº 166/2019; o faturamento declarado, o fluxo de caixa recente e o nível de endividamento já existente.",
                "É por isso que 2 empresas com o mesmo faturamento podem receber propostas diferentes de um mesmo banco: a diferença normalmente está no histórico de pagamento, no endividamento já contratado ou na existência de garantia disponível, não no faturamento isolado.",
            ]),
            ("Por que a mesma empresa recebe respostas diferentes em bancos diferentes", [
                "Cada instituição tem sua própria política interna de crédito, seu próprio apetite de risco por setor e seu próprio limite de exposição já comprometido com aquele CNPJ ou com empresas do mesmo segmento. Uma recusa em um banco não significa recusa em todos: significa que aquela política específica não enquadrou o perfil apresentado, naquele momento.",
                "Essa é também a razão pela qual buscar crédito costuma funcionar melhor como um processo comparativo entre instituições, e não como uma tentativa isolada em um único lugar.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Sistema de Informações de Crédito (SCR) e portal Registrato.",
            "Lei Complementar nº 166/2019. Cadastro Positivo.",
            "BNDES. Como funciona o financiamento via agentes financeiros credenciados.",
        ],
    },

    # ------------------------------------------------------------------ 22
    {
        "slug": "o-que-reduz-o-custo-do-credito-empresarial",
        "image": "assets/img/conteudos/o-que-reduz-o-custo-do-credito-empresarial.jpg",  # foto enviada pelo cliente (Pexels, licença livre) — mão operando calculadora ao lado de anotações e gráfico
        "category": "Estratégia Financeira",
        "date": "2026-09-18",
        "date_label": "18 set 2026",
        "read": "6 min",
        "title": "O que realmente reduz o custo do crédito empresarial",
        "excerpt": "Negociar taxa direto com o gerente raramente é o que move o ponteiro. O que reduz custo, de forma consistente, é mudar as variáveis que o credor usa para precificar risco.",
        "cta_title": "Quer saber o que pesa contra o custo do seu crédito hoje?",
        "cta_text": "Traga a taxa que você tem contratada ou que recebeu em proposta. Avaliamos o que, no seu perfil, está encarecendo o crédito.",
        "cta_primary": "Avaliar o custo do meu crédito",
        "sections": [
            ("Taxa não é uma tabela fixa, é um cálculo de risco", [
                "Nenhuma instituição financeira define a taxa de uma proposta olhando só para o segmento da empresa. A taxa reflete a estimativa de perda esperada naquela operação específica: quanto maior a chance de inadimplência e menor a chance de recuperação em caso de não pagamento, maior a taxa cobrada para compensar esse risco.",
                "Isso significa que reduzir custo de crédito, na prática, é reduzir o risco percebido pelo credor. Negociar diretamente o número da taxa tem efeito limitado quando as variáveis por trás dela continuam as mesmas.",
            ]),
            ("Garantia muda a equação de forma mais direta que negociação", [
                "Como já mostramos ao comparar dívida com e sem garantia real, a diferença de taxa entre uma linha sem garantia e uma linha com garantia real costuma ser de múltiplos, não de pontos percentuais, porque o credor passa a contar com um bem executável em caso de inadimplência. Isso não significa que toda empresa deva migrar para uma linha com garantia, mas que garantia é a alavanca mais forte disponível sobre o custo final.",
            ]),
            ("Histórico de pagamento pesa mais do que parece", [
                "O Cadastro Positivo, que hoje inclui empresas de forma automática, existe justamente para que um histórico de pagamento consistente vire argumento de negociação, e não só um dado que o banco vê sem que a empresa saiba. Manter esse histórico limpo, e revisá-lo periodicamente pelos canais oficiais, é uma forma de custo evitável: score baixo por erro cadastral, e não por inadimplência real, ainda encarece proposta.",
                "O mesmo vale para o Sistema de Informações de Crédito (SCR) do Banco Central: qualquer operação em atraso, mesmo pequena, aparece no histórico consultado pelos bancos e afeta a taxa oferecida nas próximas contratações.",
            ]),
            ("Concentração de dívida também é custo", [
                "Uma empresa com endividamento concentrado em linhas de curto prazo e taxa alta, como cheque especial ou capital de giro rotativo, tende a receber propostas piores em qualquer linha nova, porque o credor soma esse comprometimento ao avaliar a capacidade de pagamento. Reorganizar o passivo antes de buscar uma linha nova costuma valer mais do que tentar negociar a taxa da linha nova isoladamente.",
            ]),
            ("O que, de fato, não reduz custo", [
                "Trocar de banco sem mudar nenhuma dessas variáveis tende a repetir o mesmo resultado, porque o risco percebido é sobre a empresa, não sobre a instituição. Da mesma forma, insistir na renegociação de uma única proposta, sem comparar com outra instituição, deixa a empresa sem parâmetro real de quanto daquele custo é inerente ao perfil e quanto é margem negociável daquele banco específico.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Sistema de Informações de Crédito (SCR).",
            "Lei Complementar nº 166/2019. Cadastro Positivo.",
        ],
    },

    # ------------------------------------------------------------------ 23
    {
        "slug": "como-funciona-a-analise-de-credito-da-empresa",
        "image": "assets/img/conteudos/como-funciona-a-analise-de-credito-da-empresa.jpg",  # foto enviada pelo cliente (Pexels, licença livre) — mulher revisando pastas e documentos numa mesa
        "category": "Crédito PJ",
        "date": "2026-09-18",
        "date_label": "18 set 2026",
        "read": "7 min",
        "title": "Como funciona a análise de crédito de uma empresa",
        "excerpt": "A análise não é uma decisão única, é uma sequência de filtros. Entender cada etapa explica por que uma proposta demora, é ajustada ou é recusada.",
        "cta_title": "Quer entender como sua empresa seria avaliada antes de solicitar?",
        "cta_text": "Traga o motivo da operação e o faturamento da empresa. Explicamos como a análise tende a se comportar no seu caso.",
        "cta_primary": "Entender minha análise",
        "faq": [
            ("Quanto tempo demora uma análise de crédito empresarial?",
             "Varia por instituição e por linha: propostas simples e dentro de política podem ser respondidas em dias, enquanto operações estruturadas, com garantia real ou fora do padrão costumam levar semanas, porque envolvem etapas adicionais de avaliação e formalização."),
            ("A análise de crédito é igual em todos os bancos?",
             "Não. Cada instituição tem sua própria política interna, seu próprio apetite de risco por setor e seus próprios limites de exposição, o que explica respostas diferentes para o mesmo CNPJ em bancos diferentes."),
            ("O que pesa mais na análise: faturamento ou histórico de pagamento?",
             "Nenhum dos dois isoladamente. A análise combina capacidade de pagamento (que depende do faturamento e do fluxo de caixa) com histórico de crédito (que depende do comportamento de pagamento registrado). Faturamento alto com histórico ruim, ou histórico bom com capacidade de pagamento insuficiente, tendem a limitar a aprovação da mesma forma."),
        ],
        "sections": [
            ("A análise é uma sequência, não uma decisão única", [
                "Quando uma empresa solicita crédito, a proposta passa por uma sequência de filtros até chegar a uma decisão final. Entender essa sequência ajuda a saber em qual etapa uma operação específica pode estar travando, e o que, de fato, está sob controle da empresa.",
            ]),
            ("Primeiro filtro: enquadramento na política da instituição", [
                "Antes de qualquer análise individual, a instituição verifica se o pedido se enquadra na sua própria política: segmento de atuação da empresa, porte, faturamento mínimo e máximo da linha, tempo de existência do CNPJ e, em alguns casos, restrição a determinados setores considerados de maior risco. Um pedido fora dessa política costuma ser recusado antes mesmo de chegar à análise de crédito propriamente dita.",
            ]),
            ("Segundo filtro: histórico de crédito e de pagamento", [
                "Com o pedido enquadrado, a instituição consulta o histórico da empresa e, com frequência, dos sócios: o Sistema de Informações de Crédito (SCR) do Banco Central, que mostra as operações ativas e em atraso reportadas mensalmente pelos bancos, e o Cadastro Positivo, que reúne o histórico de pagamento ao longo do tempo. Restrição registrada, operação em atraso ou concentração de dívida em linhas de curto prazo aparecem nessa etapa.",
            ]),
            ("Terceiro filtro: capacidade de pagamento", [
                "Aqui entram o faturamento declarado, o fluxo de caixa recente e o nível de endividamento já contratado. A instituição projeta se a receita da empresa sustenta mais uma parcela, considerando o que já está comprometido. É nessa etapa que faturamento alto sem fluxo de caixa organizado costuma esbarrar: a receita existe, mas a folga para uma nova parcela não fica clara na análise.",
            ]),
            ("Quarto filtro: garantia e estrutura da operação", [
                "Quando a linha exige ou admite garantia, a existência de um bem elegível, imóvel, veículo, recebíveis ou aval, muda a equação de risco e pode viabilizar uma operação que não passaria sem garantia. É também nessa etapa que o valor e o prazo da operação são ajustados: a instituição pode aprovar um valor menor ou um prazo diferente do solicitado, em vez de recusar por completo.",
            ]),
            ("Quinto filtro: decisão final e formalização", [
                "Com os 4 filtros anteriores percorridos, a instituição emite a decisão: aprovação nos termos solicitados, aprovação com ajuste de valor, prazo ou garantia, ou recusa. Operações mais simples e dentro da política tendem a ser respondidas em poucos dias. Operações estruturadas, com garantia real ou fora do padrão da instituição costumam levar mais tempo, porque envolvem etapas adicionais de avaliação jurídica e de formalização.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Sistema de Informações de Crédito (SCR).",
            "Lei Complementar nº 166/2019. Cadastro Positivo.",
        ],
    },

    # ------------------------------------------------------------------ 24
    {
        "slug": "por-que-o-banco-nao-libera-credito-para-minha-empresa",
        "image": "assets/img/conteudos/por-que-o-banco-nao-libera-credito-para-minha-empresa.jpg",  # foto enviada pelo cliente (Pexels, licença livre) — profissional pensativo à mesa, com balança e laptop
        "category": "Crédito PJ",
        "date": "2026-09-18",
        "date_label": "18 set 2026",
        "read": "6 min",
        "title": "Por que o banco não libera crédito para minha empresa",
        "excerpt": "A recusa raramente tem uma única causa. Na maior parte dos casos, é a soma de 2 ou 3 fatores, e nem sempre o banco explica qual deles pesou mais.",
        "cta_title": "Teve crédito negado e não sabe exatamente por quê?",
        "cta_text": "Traga o que foi negado e por qual instituição. Avaliamos o que pode ter pesado antes de tentar de novo.",
        "cta_primary": "Entender minha negativa",
        "sections": [
            ("A recusa é quase sempre combinada, não isolada", [
                "Bancos raramente recusam crédito empresarial por um único motivo isolado. O mais comum é a combinação de 2 ou 3 fatores que, juntos, ultrapassam o limite de risco que aquela instituição aceita para aquele tipo de operação. Isso explica por que a mesma empresa pode ser recusada em um banco e aprovada em outro: cada instituição pesa esses fatores de um jeito diferente.",
            ]),
            ("Os motivos mais frequentes", [
                "Endividamento já elevado em relação ao faturamento, mesmo sem atraso registrado, reduz a margem que o banco enxerga para uma parcela nova. Restrição ou atraso recente, seja da empresa ou dos sócios, aparece no Sistema de Informações de Crédito (SCR) do Banco Central e pesa diretamente na análise. Fluxo de caixa instável ou pouco documentado dificulta a projeção de capacidade de pagamento, ainda que o faturamento seja alto. Tempo de CNPJ curto limita o histórico disponível para análise, o que reduz o universo de linhas elegíveis. E enquadramento fora da política interna daquele banco específico, para aquele setor ou porte, encerra a análise antes mesmo de avaliar o restante.",
            ]),
            ("Por que o banco raramente explica o motivo exato", [
                "A maioria das instituições comunica apenas a recusa, sem detalhar qual dos fatores pesou mais. Isso acontece porque a decisão combina critérios internos de política de risco que o banco não é obrigado a divulgar, e porque, na prática, mais de um fator costuma estar presente ao mesmo tempo. Tentar adivinhar o motivo com base só na comunicação do banco costuma levar a correções que não resolvem o problema real.",
            ]),
            ("O que fazer depois de uma recusa", [
                "O primeiro passo é reunir as informações que o próprio banco usou: consultar o histórico da empresa no SCR pelo Registrato, revisar o Cadastro Positivo e organizar o fluxo de caixa recente. Com isso em mãos, fica mais claro se o obstáculo é endividamento, histórico, documentação ou enquadramento, e cada um desses cenários pede uma resposta diferente antes de tentar novamente.",
                "Vale evitar solicitar a mesma linha em vários bancos ao mesmo tempo sem entender o motivo da primeira recusa: isso tende a repetir o resultado, e cada nova consulta de crédito também fica registrada no histórico consultado pelas próximas instituições.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Sistema de Informações de Crédito (SCR) e portal Registrato.",
            "Lei Complementar nº 166/2019. Cadastro Positivo.",
        ],
    },

    # ------------------------------------------------------------------ 25
    {
        "slug": "faturamento-alto-e-credito-negado",
        "image": "assets/img/conteudos/faturamento-alto-e-credito-negado.jpg",  # foto enviada pelo cliente (Pexels, licença livre) — lupa sobre gráfico colorido de análise
        "category": "Estratégia Financeira",
        "date": "2026-09-18",
        "date_label": "18 set 2026",
        "read": "5 min",
        "title": "Minha empresa fatura bem, mas o crédito continua sendo negado. Por quê?",
        "excerpt": "Faturamento alto responde por uma parte da análise, não por ela inteira. A recusa costuma estar em outra variável que o faturamento, sozinho, não mostra.",
        "cta_title": "Fatura bem e mesmo assim o crédito não sai?",
        "cta_text": "Traga o faturamento e o motivo da última recusa. Avaliamos o que, além da receita, está pesando na análise.",
        "cta_primary": "Entender minha empresa",
        "sections": [
            ("Faturamento mede receita, não capacidade de pagamento", [
                "Faturamento alto mostra que a empresa vende. Não mostra, sozinho, se sobra caixa depois de pagar fornecedor, folha, tributos e dívida já existente. É essa sobra, e não a receita bruta, que o banco tenta estimar ao avaliar se a empresa suporta mais uma parcela. Uma empresa pode faturar bem e ter margem apertada ao mesmo tempo, e é esse segundo dado que costuma decidir a análise.",
            ]),
            ("Onde o descompasso costuma aparecer", [
                "O padrão mais comum é faturamento crescendo mais rápido do que a organização financeira da empresa consegue acompanhar: crescimento puxa mais estoque, mais prazo concedido a cliente e mais custo operacional, e a necessidade de capital de giro cresce junto, mesmo que o resultado contábil pareça positivo. Se esse descompasso já aparece no fluxo de caixa ou no endividamento contratado para sustentar o crescimento, o banco enxerga um risco que o número de faturamento, isolado, não revela.",
            ]),
            ("Outros fatores que se somam ao descompasso de caixa", [
                "Endividamento concentrado em linhas de curto prazo e taxa alta, restrição ou atraso recente no histórico da empresa ou dos sócios, e documentação fiscal ou contábil desatualizada também pesam, independentemente do faturamento. Como no caso de qualquer recusa, raramente é um único fator isolado: costuma ser a combinação entre um faturamento que parece sólido no papel e uma ou mais dessas variáveis que o banco avalia por trás dele.",
            ]),
            ("O que revisar antes de solicitar de novo", [
                "Vale reconstruir o fluxo de caixa dos últimos meses e confrontá-lo com o faturamento declarado, revisar o histórico da empresa e dos sócios no Sistema de Informações de Crédito (SCR) do Banco Central, e mapear o quanto da dívida atual está concentrado em linhas caras de curto prazo. Esse diagnóstico costuma apontar com mais precisão o que precisa ser ajustado antes de uma nova tentativa, em vez de repetir o pedido na expectativa de um resultado diferente.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Sistema de Informações de Crédito (SCR).",
        ],
    },

    # ------------------------------------------------------------------ 26
    {
        "slug": "como-aumentar-a-aprovacao-de-credito-empresarial",
        "image": "assets/img/conteudos/como-aumentar-a-aprovacao-de-credito-empresarial.jpg",  # foto enviada pelo cliente (Pexels, licença livre) — mão marcando item concluído numa checklist
        "category": "Crédito PJ",
        "date": "2026-09-18",
        "date_label": "18 set 2026",
        "read": "6 min",
        "title": "Como aumentar as chances de aprovação de crédito empresarial",
        "excerpt": "Não existe fórmula que garanta aprovação. Existem, sim, variáveis que a empresa controla antes de solicitar, e que mudam como a análise se comporta.",
        "cta_title": "Quer se preparar antes de solicitar crédito de novo?",
        "cta_text": "Traga o motivo da operação e o histórico recente da empresa. Organizamos o que dá para ajustar antes da próxima solicitação.",
        "cta_primary": "Preparar minha empresa",
        "sections": [
            ("Não existe garantia de aprovação, existe preparo", [
                "Nenhuma instituição, condição ou consultoria pode garantir a aprovação de uma operação de crédito: a decisão final depende da política e da análise de risco de cada banco. O que está sob controle da empresa é o preparo que antecede o pedido, e esse preparo muda de forma mensurável como a proposta é recebida.",
            ]),
            ("Organizar o histórico antes de solicitar", [
                "Consultar o próprio histórico no Sistema de Informações de Crédito (SCR) do Banco Central, gratuitamente pelo Registrato, e revisar o Cadastro Positivo antes de procurar uma instituição permite identificar e corrigir eventuais erros cadastrais, e entender com antecedência qual imagem de crédito o banco vai encontrar. É mais eficiente chegar já sabendo o que o histórico mostra do que descobrir isso apenas na recusa.",
            ]),
            ("Reduzir concentração de dívida cara", [
                "Linhas de curto prazo e taxa alta, como cheque especial ou capital de giro rotativo usado de forma recorrente, pesam contra a aprovação de uma linha nova porque reduzem a margem de endividamento que o banco enxerga disponível. Reorganizar esse passivo antes de solicitar, mesmo que signifique um passo intermediário, tende a melhorar o resultado da solicitação seguinte.",
            ]),
            ("Ter documentação fiscal e contábil atualizada", [
                "Balanço, demonstrativo de resultado e obrigações fiscais em dia agilizam a análise e evitam que a proposta seja pausada por pendência documental, que é uma causa de atraso tão comum quanto a própria análise de risco. Documentação desorganizada também dificulta que o banco enxergue com precisão o fluxo de caixa real da empresa.",
            ]),
            ("Levar garantia, quando ela existir", [
                "Quando a empresa tem um bem elegível, imóvel, veículo ou recebíveis, e a operação comporta garantia, apresentar essa opção desde o início amplia o universo de linhas disponíveis e tende a resultar em condições mais favoráveis do que buscar apenas linhas sem garantia.",
            ]),
            ("Comparar mais de uma instituição", [
                "Como cada banco tem sua própria política interna, apresentar a mesma operação bem preparada a mais de uma instituição, de forma organizada e não simultânea de forma indiscriminada, aumenta a chance de encontrar a política que melhor se encaixa no perfil da empresa, em vez de depender de uma única resposta.",
            ]),
        ],
        "sources": [
            "Banco Central do Brasil. Sistema de Informações de Crédito (SCR) e portal Registrato.",
            "Lei Complementar nº 166/2019. Cadastro Positivo.",
        ],
    },
]

ART_BY_SLUG = {a["slug"]: a for a in ARTICLES}


def hub():
    path = "conteudos.html"
    trail = [("Início", "index.html"), ("Conteúdos", None)]

    body = B.pagehead(
        path, trail, "Conteúdos",
        "Material técnico sobre o que costuma custar caro por falta de informação.",
        "Escrevemos sobre custo efetivo, prazo, garantia e adequação. Sempre com a fonte "
        "identificada, e sem transformar dado público em promessa comercial.",
        meta=[("Artigos publicados", f"{len(ARTICLES)}"),
              ("Categorias", f"{len(CATEGORIES)}")],
        variant=2, image_slot="conteudos")

    filters = '<button class="filter" data-cat="todas" aria-pressed="true">Todas</button>'
    used = [c for c in CATEGORIES if any(a["category"] == c for a in ARTICLES)]
    filters += "".join(
        f'<button class="filter" data-cat="{c}" aria-pressed="false">{c}</button>' for c in used
    )

    rows = ""
    for a in ARTICLES:
        index = f"{a['title']} {a['excerpt']} {a['category']}"
        attrs = f' data-cat="{a["category"]}" data-index="{B.esc(index)}"'
        rows += B.artrow(path, "conteudos/" + a["slug"] + ".html", a.get("image"),
                          a["category"], a["title"], a["excerpt"],
                          foot=f"{a['date_label']} · {a['read']}", extra_attrs=attrs)

    body += f"""<section class="band">
  <div class="shell">
    <h2 class="sr">Todos os artigos</h2>
    <div class="searchfield">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><circle cx="7" cy="7" r="4.6"/><path d="M10.5 10.5L14 14"/></svg>
      <label class="sr" for="busca">Buscar nos conteúdos</label>
      <input type="search" id="busca" data-artsearch placeholder="Buscar por assunto ou estrutura">
    </div>
    <div class="filters" role="group" aria-label="Filtrar por categoria">{filters}</div>
    <p class="xs muted mb-2" data-artcount aria-live="polite">{len(ARTICLES)} artigos</p>
    <div class="artlist" data-artlist>
      {rows}
      <p class="artlist__empty" style="display:none">Nenhum artigo corresponde a essa busca. Tente outro termo ou remova o filtro de categoria.</p>
    </div>
  </div>
</section>"""

    body += B.video_grid(path)

    body += B.cta_band(path, "Um artigo não substitui uma leitura do seu caso.",
                       "O conteúdo aqui é geral por definição. A recomendação depende do passivo, do patrimônio e do fluxo de caixa de quem pergunta.",
                       secondary=("Ver as soluções", "solucoes.html"), tone="ink")

    return {
        "path": path, "nav_key": "conteudos.html", "over": True,
        "title": "Conteúdos sobre crédito e garantia | Acrópole Capital",
        "desc": ("Artigos técnicos sobre custo efetivo total, capital de giro, home equity, auto equity, "
                 "crédito PJ e financiamento de obra, com fontes públicas identificadas."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail), {
            "@context": "https://schema.org", "@type": "Blog",
            "name": "Conteúdos Acrópole Capital", "inLanguage": "pt-BR",
            "url": SITE["domain"] + "/conteudos",
        }],
    }


def _sources_html(sources):
    """
    Lista de fontes no rodapé do artigo. NÃO é mais chamada em article_page
    (pedido do cliente: a lista de fontes deixava a página poluída
    visualmente) — mantida aqui só porque o campo "sources" continua nos
    dados de cada artigo (útil como referência interna/SEO), caso algum dia
    volte a fazer sentido exibi-la de outra forma (ex.: rodapé colapsável).
    """
    if not sources:
        return ""
    items = "".join(f"<li>{B.esc(s)}</li>" for s in sources)
    return (f'<div class="mt-4"><p class="xs muted" style="margin:0 0 .5rem">Fontes</p>'
            f'<ul class="art-sources muted">{items}</ul></div>')


def article_page(a):
    path = f"conteudos/{a['slug']}.html"
    trail = [("Início", "index.html"), ("Conteúdos", "conteudos.html"), (a["title"], None)]

    anchors = [(t, B.slugify(t)) for t, _ in a["sections"]]

    prose = ""
    for (title, paras), (_, sid) in zip(a["sections"], anchors):
        prose += f'<h2 id="{sid}">{title}</h2>' + "".join(f"<p>{p}</p>" for p in paras)

    # FAQ por artigo (campo opcional "faq"): só os artigos que realmente têm
    # perguntas frequentes distintas o carregam, em vez de forçar uma seção
    # genérica em todos os 20 já publicados. Vira acordeão + FAQPage schema.
    if a.get("faq"):
        prose += f'<h2 id="perguntas-frequentes">Perguntas frequentes</h2>{B.accordion(a["faq"], ident=a["slug"])}'

    related = [x for x in ARTICLES if x["slug"] != a["slug"]][:4]
    rel_cards = "".join(
        B.sidearticle(path, "conteudos/" + r["slug"] + ".html", r.get("image"),
                      r["title"], foot=r["date_label"])
        for r in related
    )

    art_variant = ARTICLES.index(a) % 3
    # Mesmo helper usado por toda página interna (B.pagehead), em vez de
    # reconstruir a seção à mão: essa duplicação já tinha causado um desvio
    # real — a versão daqui não passava eager=True pro photo_or_art, então a
    # imagem de topo do artigo (tão acima da dobra quanto em qualquer outra
    # página) carregava lazy à toa, atrasando o LCP só nesse template.
    body = B.pagehead(
        path, trail[:2] + [(a['category'], None)], a['category'], a['title'], a['excerpt'],
        meta=[("Publicado", a['date_label']), ("Leitura", a['read']),
              ("Autoria", "Equipe Acrópole Capital")],
        variant=art_variant, image_slot="artigo-" + a["slug"])

    body += f"""<section class="band">
  <div class="shell">
    <div class="cols cols--8-4 cols--aside-sticky">
      <article class="prose">
        {prose}
        <div class="notice mt-4">Este artigo tem finalidade informativa e não constitui recomendação de contratação, consultoria de investimentos ou promessa de aprovação. Taxas, prazos e limites variam por instituição financeira e por perfil de crédito, e estão sujeitos a análise.</div>
        <div class="mt-3 share">
          <button class="btn btn--line btn--sm" data-share type="button">Compartilhar</button>
        </div>
      </article>
      <aside class="artside">
        <p class="sidearts__eyebrow">Continuar lendo</p>
        <p class="sidearts__heading">Outros conteúdos</p>
        <div class="sidearts">{rel_cards}</div>
        <div class="mt-3">{B.tlink("Ver todos os conteúdos", "conteudos.html", path)}</div>
        <div class="capture-sticky mt-4">{B.newsletter_box(path)}</div>
      </aside>
    </div>
  </div>
</section>"""

    # CTA contextual: cada artigo tem seu próprio título, texto e rótulo de
    # botão (chaves "cta_title"/"cta_text"/"cta_primary" no dicionário do
    # artigo), em vez do mesmo "Aplicar isso ao seu caso" repetido nos 20.
    # O texto de cada um parte do problema/dúvida real que o próprio artigo
    # responde, sem prometer aprovação, taxa ou valor.
    body += B.cta_band(path, a.get("cta_title", "Aplicar isso ao seu caso."),
                       a.get("cta_text", "Traga os números reais da operação. A leitura técnica é gratuita e não gera compromisso."),
                       primary=(a.get("cta_primary", "Solicitar uma análise"), a.get("cta_href", "contato.html")),
                       secondary=None, tone="ink")

    body += B.comments_section(a["slug"])

    # Título de SEO com corte pelo total (não só pelo título do artigo): o
    # sufixo " | Acrópole Capital" tem 20 caracteres, e o limite de exibição
    # do Google gira em torno de 60. O corte antigo permitia até 71
    # caracteres no total, o que truncava o título nos resultados de busca.
    _suffix = " | Acrópole Capital"
    _max_title = 60 - len(_suffix)
    _title_text = (a['title'] if len(a['title']) <= _max_title
                   else a['title'][:_max_title - 1].rstrip() + "…")

    return {
        "path": path, "nav_key": "conteudos.html", "over": True, "og_type": "article",
        "title": _title_text + _suffix,
        "desc": B.fit_desc(a["excerpt"]),
        # Identifica a origem do lead para o CRM sem depender de reconstruir
        # a categoria a partir da URL: vira campo oculto no formulário do
        # popup de captação (ver build.lead_modal). O endereço da página em
        # si já é enviado por padrão em toda submissão (site.js, payload.page).
        "lead_context": {"article": a["slug"], "category": a["category"]},
        "body": body,
        "schema": [B.breadcrumb_schema(trail)] + ([B.faq_schema(a["faq"])] if a.get("faq") else []) + [{
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": a["title"], "description": a["excerpt"],
            # dateModified existe desde a publicação (igual a datePublished, por
            # ora) em vez de só depois da primeira revisão: assim o campo já
            # aparece na marcação estruturada, e passa a refletir a data real
            # assim que o artigo for revisado de fato — usar a chave "updated"
            # no dicionário do artigo quando isso acontecer.
            "datePublished": a["date"], "dateModified": a.get("updated", a["date"]),
            "inLanguage": "pt-BR",
            "articleSection": a["category"],
            "author": {"@type": "Organization", "name": "Acrópole Capital"},
            "publisher": {"@type": "Organization", "name": "Acrópole Capital"},
            "mainEntityOfPage": SITE["domain"] + "/conteudos/" + a["slug"],
        }],
    }


def pages():
    return [hub()] + [article_page(a) for a in ARTICLES]
