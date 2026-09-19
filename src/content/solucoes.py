# -*- coding: utf-8 -*-
"""Hub de soluções e as oito páginas dedicadas."""

from content.site import SOLUTIONS, SOL_BY_SLUG, CONDITIONS_NOTICE
import build as B


DETAIL = {
    # ------------------------------------------------------------------ giro
    "capital-de-giro": {
        "h1": "Liquidez dimensionada pelo ciclo, não pela urgência.",
        "lead": "Capital de giro financia a distância entre pagar fornecedores e receber de clientes. "
                "Quando essa distância é medida antes de apertar, a linha custa menos, dura mais e não "
                "precisa ser renovada em condição desfavorável.",
        "meta": [("Modalidade", "Crédito PJ, rotativo ou parcelado"),
                 ("Lastro", "Recebíveis, duplicatas, aval, fiança ou garantia real"),
                 ("Referência de mercado", "23,55% a.a. médios em jul/2026, série SGS/BCB")],
        "variant": 0,
        "context_title": "O problema não é o valor. É a defasagem.",
        "context": [
            "A necessidade de capital de giro é o intervalo financeiro entre o momento em que a empresa "
            "desembolsa e o momento em que recebe. Ela inclui estoque, prazo concedido a clientes, folha, "
            "tributos, fornecedores e despesas sazonais.",
            "Em fase de expansão, esse intervalo cresce de forma desproporcional: mais vendas significam "
            "mais estoque comprado, mais produção financiada e, com frequência, prazos maiores concedidos "
            "para conquistar novos clientes.",
            "É por isso que dimensionamos a necessidade antes de discutir linha. Contratar abaixo do gap real "
            "obriga a empresa a voltar ao mercado em situação pior; contratar muito acima transforma custo "
            "financeiro em despesa desnecessária.",
        ],
        "pull": "Uma empresa pode fechar o exercício com lucro contábil e, ainda assim, não ter caixa para o mês seguinte.",
        "problems_title": "Quando essa estrutura faz sentido",
        "problems": [
            "A empresa cresce e o caixa aperta na mesma proporção, mesmo com margem preservada.",
            "Rotativo, cheque especial ou antecipação avulsa viraram rotina, e não exceção.",
            "Há sazonalidade previsível que exige comprar estoque ou financiar produção com meses de antecedência.",
            "O prazo concedido a clientes aumentou para sustentar a competitividade comercial.",
            "Existe uma oportunidade de compra com desconto relevante que exige caixa imediato.",
        ],
        "how": [
            ("Cálculo da necessidade",
             "Levantamos prazo médio de estoque, de recebimento e de pagamento para dimensionar o gap real, e não o valor que a empresa imagina precisar."),
            ("Escolha do lastro",
             "Definimos o que sustenta a operação: recebíveis, duplicatas, adquirência, aval, fiança, alienação de equipamentos ou garantia imobiliária."),
            ("Enquadramento em programas",
             "Verificamos elegibilidade a Pronampe, Procred 360 e PEAC FGI, que podem reduzir a exigência de garantia real para empresas de menor porte."),
            ("Comparação e formalização",
             "Comparamos instituições por custo efetivo total e perfil de amortização, e conduzimos a formalização junto à escolhida."),
        ],
        "audience": [
            ("Empresas em expansão", "Crescimento de receita acompanhado por aumento desproporcional da necessidade de giro."),
            ("Negócios sazonais", "Operações que precisam antecipar estoque ou produção meses antes do pico de venda."),
            ("Empresas com prazo longo a clientes", "Fornecedores de grandes contas, indústrias e distribuidores com ciclo de recebimento estendido."),
            ("Empresas em recomposição", "Negócios saudáveis que precisam substituir dívida curta e cara por estrutura compatível com o ciclo."),
        ],
        "benefits": [
            "<strong>Amortização aderente ao fluxo.</strong> Parcela dimensionada pelo ciclo real de caixa, não por um prazo padrão de prateleira.",
            "<strong>Antecipação da falha de liquidez.</strong> A linha é estruturada antes do aperto, quando a empresa ainda negocia de posição favorável.",
            "<strong>Acesso a mecanismos públicos de garantia.</strong> Pronampe, Procred 360 e PEAC FGI reduzem a exigência de garantia real para quem se enquadra.",
            "<strong>Comparação entre naturezas de instituição.</strong> SCDs e SEPs se comportam de forma diferente em momentos de aperto monetário.",
        ],
        "cautions": [
            ("Giro não corrige prejuízo",
             "Financiar déficit operacional recorrente com dívida apenas desloca o problema e aumenta a perda potencial. Se a margem é negativa, o problema é operacional, não financeiro."),
            ("Cuidado com dupla cessão",
             "Recebíveis já cedidos a outra operação não podem lastrear uma nova. Mapear o que já está comprometido evita a reprovação tardia, depois de semanas de processo."),
            ("Concentração encarece",
             "Receita concentrada em poucos clientes eleva o risco percebido e restringe prazo antes de restringir valor, mesmo com faturamento robusto."),
        ],
        "faq": [
            ("Qual a diferença entre giro rotativo e giro parcelado?",
             "O rotativo funciona como um limite disponível, com custo incidindo sobre o valor utilizado; o parcelado é contratado por valor e prazo definidos, com amortização programada. Rotativo serve para oscilação de curto prazo; parcelado, para necessidade estrutural."),
            ("Preciso oferecer garantia real?",
             "Nem sempre. Recebíveis, aval e fiança sustentam boa parte das operações, e mecanismos como Pronampe e PEAC FGI existem justamente para reduzir a exigência de garantia real para empresas elegíveis."),
            ("A empresa precisa ter balanço auditado?",
             "Não necessariamente, mas balanço e demonstrativos organizados ampliam bastante o conjunto de instituições dispostas a analisar e melhoram as condições ofertadas."),
            ("Por que nenhum banco publica uma taxa fixa de capital de giro?",
             "Porque ela não existe. Taxa, CET, tarifa e limite dependem de modalidade, relacionamento, garantia e perfil de risco, e só aparecem depois de login, simulação ou proposta de gerente, inclusive nos seis maiores bancos do país. É essa opacidade, repetida de instituição para instituição, que torna a comparação trabalhosa para quem não faz isso todos os dias."),
        ],
        "checklist_title": "Seis pontos que decidem se a proposta é boa, não só barata.",
        "checklist_lead": "A página do banco raramente mostra CET, garantia e carência lado a lado. Isso só aparece na simulação autenticada ou na proposta do gerente, e é aí que a comparação de verdade começa.",
        "checklist": [
            ("Produto-base ou programa público",
             "Confirme se a oferta é capital de giro convencional ou um programa como Pronampe, Procred 360 ou PEAC FGI. A regra de elegibilidade, o prazo e a taxa mudam inteiramente de um para o outro."),
            ("Simulação por escrito, de mais de uma instituição",
             "Peça valor líquido, prazo, carência e data da primeira parcela registrados, não apenas o que aparece na página comercial. Simule em pelo menos duas instituições antes de decidir."),
            ("CET, não a taxa mensal isolada",
             "Some juros, IOF, tarifa e seguro. Duas propostas com a mesma taxa mensal podem chegar a um custo efetivo total bem diferente."),
            ("Garantias e obrigações acessórias",
             "Aval, cessão de recebíveis, domicílio bancário e reforço de garantia mudam o risco real da operação, mesmo quando o preço parece igual no papel."),
            ("Capacidade de pagamento sob estresse",
             "Simule queda de receita e o valor da parcela depois da carência. Carência adia o desembolso; não elimina o juro acumulado no período."),
            ("Canal oficial de formalização",
             "Confirme domínio, aplicativo e telefone da instituição antes de assinar ou compartilhar qualquer credencial."),
        ],
        "checklist_link": ("Ver como funcionam Pronampe, Procred 360 e PEAC FGI, com simulador", "programas.html"),
        "related_articles": [
            ("Como calcular a necessidade de capital de giro da empresa", "como-calcular-necessidade-de-capital-de-giro"),
            ("Garantia para crédito empresarial: tipos, custo e risco real", "garantia-para-credito-empresarial"),
        ],
        "tool_link": ("Usar a calculadora de necessidade de capital de giro", "calculadora-capital-de-giro.html"),
    },

    # ------------------------------------------------------------ home equity
    "home-equity": {
        "h1": "O imóvel continua seu. A liquidez também.",
        "lead": "Crédito com garantia de imóvel permite obter capital mantendo posse e uso do bem. "
                "A eficiência da linha vem da garantia, e é exatamente por isso que a decisão exige "
                "mais critério do que qualquer outra.",
        "meta": [("Base legal", "Lei nº 9.514/1997, alienação fiduciária"),
                 ("LTV médio de mercado", "32,2% em março de 2026, Abecip"),
                 ("Prazo médio de mercado", "159 meses em março de 2026, Abecip")],
        "variant": 1,
        "context_title": "Por que a garantia muda o custo.",
        "context": [
            "Na alienação fiduciária, a propriedade resolúvel do imóvel é transferida ao credor no momento "
            "da contratação, sem que o devedor perca a posse ou o uso do bem. Cumprido o contrato, a "
            "propriedade plena retorna ao proprietário.",
            "Como a execução da garantia segue rito extrajudicial, e não uma ação judicial de hipoteca, a "
            "perda esperada do credor é menor.",
            "A contrapartida é séria: o bem oferecido passa a responder pela dívida. Por isso separamos, na "
            "análise, o risco da operação do risco de perda do imóvel familiar, e recomendamos a estrutura "
            "apenas quando prazo, finalidade e capacidade de pagamento tornam essa decisão defensável.",
        ],
        "pull": "É essa redução de risco, e não uma generosidade do mercado, que sustenta taxas menores e prazos mais longos.",
        "problems_title": "Quando essa estrutura faz sentido",
        "problems": [
            "Existe saldo relevante em linhas caras, como rotativo do cartão ou cheque especial, e um imóvel com margem disponível.",
            "O empresário precisa capitalizar a empresa sem diluir participação societária.",
            "Há um projeto de médio prazo, como reforma, expansão ou aquisição, que se paga dentro do horizonte do contrato.",
            "O patrimônio imobiliário está parado e o custo de oportunidade dele é maior do que o custo da operação.",
        ],
        "how": [
            ("Avaliação do imóvel",
             "Análise de matrícula, ônus, regularidade documental e valor de mercado. Documentação irregular é a causa mais frequente de operação travada."),
            ("Definição da margem",
             "Cálculo do LTV realista, considerando valor de mercado, saldo devedor existente e política de risco de cada instituição."),
            ("Comparação entre instituições",
             "Comparativo por custo efetivo total, incluindo avaliação, registro, IOF e seguros obrigatórios, além da taxa nominal."),
            ("Registro e liberação",
             "Formalização da alienação fiduciária em cartório de registro de imóveis e liberação pela instituição após o registro."),
        ],
        "audience": [
            ("Quem carrega dívida cara", "Saldo relevante em rotativo, cheque especial ou crédito pessoal, com imóvel disponível para lastro."),
            ("Empresários com patrimônio pessoal", "Necessidade de capitalizar a empresa sem abrir participação societária nem vender ativos."),
            ("Famílias com imóvel quitado", "Projetos de médio e longo prazo que não cabem em crédito pessoal e não justificam venda do bem."),
            ("Investidores imobiliários", "Portfólio pronto que pode ser mobilizado como garantia sem venda em momento desfavorável."),
        ],
        "benefits": [
            "<strong>Custo substancialmente menor que crédito sem garantia.</strong> Em março de 2026, o empréstimo pessoal tradicional estava em 6,67% ao mês, segundo o Banco Central, enquanto o crédito com garantia de imóvel era reportado entre 1,12% e 1,80% ao mês nos 5 maiores bancos, segundo levantamento divulgado pela Abecip.",
            "<strong>Prazos longos.</strong> O prazo médio das operações do mercado em março de 2026 foi de 159 meses, o que reduz o peso da parcela sobre o fluxo mensal.",
            "<strong>Uso livre do recurso.</strong> Quitação de dívidas, capitalização de empresa, obra, aquisição ou investimento.",
            "<strong>Aproveitamento de margem existente.</strong> Desde a Lei nº 14.711/2023 e sua regulamentação, um mesmo imóvel pode, em determinadas condições, lastrear mais de uma operação quando há margem disponível.",
        ],
        "cautions": [
            ("Não transforme dívida de consumo em risco sobre a moradia sem calcular",
             "A migração só compensa quando o saldo é relevante, existe margem de LTV e a parcela fixa cabe no fluxo por todo o prazo. Se qualquer uma dessas 3 condições falha, a operação troca um problema caro por um risco maior."),
            ("O custo não é só a taxa",
             "Avaliação do imóvel, registro em cartório, IOF, tarifas e seguros entram no custo efetivo total. 2 ofertas com a mesma taxa nominal podem ter custos finais bem diferentes."),
            ("Documentação irregular trava a operação",
             "Matrícula desatualizada, inventário pendente, averbação de construção ausente ou ônus não baixado são as causas mais comuns de atraso. Verificar isso antes economiza semanas."),
            ("Prazo longo é alívio de parcela, não de custo",
             "Alongar reduz o valor mensal e aumenta o total pago. Simular os 2 cenários antes de assinar é obrigatório, não opcional."),
        ],
        "faq": [
            ("Preciso ter o imóvel totalmente quitado?",
             "Não necessariamente. Quanto menor o saldo devedor, maior a margem disponível. Em determinadas condições, um imóvel já usado em outra operação pode voltar a gerar crédito quando há margem, conforme a regulamentação posterior à Lei nº 14.711/2023."),
            ("Qual a diferença entre home equity e financiamento imobiliário?",
             "No financiamento, o crédito é concedido para comprar um imóvel, que serve de garantia da própria compra. No home equity, o imóvel já pertence ao tomador e é usado como garantia para obter capital de uso livre."),
            ("Posso continuar morando no imóvel ou alugando?",
             "Sim. A posse e o uso permanecem com o proprietário durante todo o contrato, incluindo a possibilidade de locação, salvo restrição contratual específica da instituição."),
            ("Qual percentual do valor do imóvel é possível obter?",
             "Depende da instituição, do perfil do tomador e do imóvel. O mercado costuma trabalhar com limites que chegam a 50% ou 60% do valor de avaliação, e o LTV médio efetivamente contratado em março de 2026 foi de 32,2%, segundo a Abecip."),
        ],
        "checklist_title": "Sete pontos que decidem se a garantia vale a pena oferecer.",
        "checklist_lead": "O LTV e a taxa nominal aparecem na simulação. Avaliação, registro, seguro e a leitura de risco sobre o próprio imóvel só ficam claros quando alguém pergunta por eles.",
        "checklist": [
            ("Regularidade da matrícula",
             "Matrícula atualizada, sem ônus não baixado, inventário pendente ou construção não averbada. É a causa mais comum de operação travada, e vale confirmar antes de entrar em simulação."),
            ("LTV realista, não o teto anunciado",
             "O mercado costuma anunciar limites de até 50% ou 60% do valor de avaliação, mas o LTV médio efetivamente contratado foi de 32,2% em março de 2026, segundo a Abecip. Peça o LTV que a instituição realmente pratica para o seu perfil."),
            ("Custo efetivo total, não a taxa nominal",
             "Avaliação do imóvel, registro em cartório, IOF e seguros obrigatórios entram na conta. Duas ofertas com a mesma taxa podem ter custo final bem diferente."),
            ("Simule o cenário de prazo alongado",
             "Prazo mais longo reduz a parcela e aumenta o total pago. Peça os dois cenários lado a lado antes de decidir."),
            ("O que acontece em caso de inadimplência",
             "A execução da garantia em alienação fiduciária segue rito extrajudicial, e não uma ação judicial de hipoteca. Entender esse mecanismo antes de assinar evita surpresa."),
        ],
        "checklist_link": ("Ver o que mudou no Marco das Garantias e como isso afeta o seu imóvel", "conteudos/marco-das-garantias-o-que-mudou.html"),
        "related_articles": [
            ("Marco das Garantias: o que mudou", "marco-das-garantias-o-que-mudou"),
            ("Garantia para crédito empresarial: tipos, custo e risco real", "garantia-para-credito-empresarial"),
        ],
    },

    # ------------------------------------------------------------ auto equity
    "auto-equity": {
        "h1": "Rápido é uma vantagem real. Longo, quase nunca.",
        "lead": "Crédito com garantia de veículo transforma um bem quitado em liquidez, mantendo posse "
                "e uso. O ponto crítico não é a taxa anunciada: é o prazo, medido contra a curva de "
                "depreciação do próprio bem.",
        "meta": [("Base legal", "Lei nº 4.728/1965, alienação fiduciária de bens móveis"),
                 ("Registro", "Gravame junto ao Detran"),
                 ("Estatística pública", "Não há série do Banco Central isolando a modalidade")],
        "variant": 2,
        "context_title": "A diferença entre financiar e alavancar.",
        "context": [
            "Financiamento de veículo é crédito para comprar o bem.",
            "Como a garantia é móvel e deprecia, o prazo praticado é bem menor do que em operações "
            "imobiliárias, frequentemente limitado a algo em torno de 60 meses. O crédito sai rápido "
            "porque a avaliação é padronizada e o gravame é registrado eletronicamente.",
            "Não existe série pública do Banco Central que isole o auto equity de outras operações com "
            "garantia móvel. Qualquer número apresentado como “tamanho do mercado de auto equity” "
            "costuma, na prática, misturar financiamento de aquisição com empréstimo garantido, e por isso "
            "não usamos esse tipo de estimativa em recomendação.",
        ],
        "pull": "Auto equity é o inverso: o veículo já existe, está quitado ou tem margem disponível, e passa a lastrear um empréstimo de uso livre.",
        "problems_title": "Quando essa estrutura faz sentido",
        "problems": [
            "Há necessidade de liquidez em prazo curto e o custo do crédito pessoal sem garantia é proibitivo.",
            "Existe uma oportunidade com janela definida que não sobrevive ao rito de uma operação imobiliária.",
            "O veículo está quitado, é recente e tem boa liquidez de revenda na praça do proprietário.",
            "O valor necessário é compatível com um prazo curto ou médio de amortização.",
        ],
        "how": [
            ("Avaliação do bem",
             "Valor de mercado por tabela de referência, idade, quilometragem, histórico de sinistro, estado de conservação e liquidez de revenda na região."),
            ("Verificação de propriedade e ônus",
             "Checagem de titularidade, gravames existentes, restrições e autenticidade. É a etapa em que mais operações são interrompidas."),
            ("Dimensionamento de prazo",
             "Definição do prazo máximo defensável comparando a amortização com a curva de depreciação do veículo, para evitar saldo devedor maior que o bem."),
            ("Gravame e liberação",
             "Registro do gravame junto ao Detran e liberação do recurso pela instituição financeira."),
        ],
        "audience": [
            ("Autônomos e profissionais liberais", "Renda comprovável de forma menos convencional, com veículo quitado e necessidade de capital de curto prazo."),
            ("Microempresários", "Necessidade de giro pontual, em valor incompatível com a estruturação de uma operação empresarial completa."),
            ("Oportunidades com janela curta", "Situações em que o custo de perder a oportunidade supera o custo financeiro da operação."),
        ],
        "benefits": [
            "<strong>Prazo de liberação curto.</strong> A avaliação é padronizada e o registro do gravame é eletrônico, o que reduz o tempo entre a solicitação e o crédito.",
            "<strong>Custo menor que crédito pessoal sem garantia.</strong> A garantia real reduz a perda esperada do credor e, com ela, a taxa cobrada.",
            "<strong>Posse e uso preservados.</strong> O proprietário continua utilizando o veículo normalmente durante todo o contrato.",
            "<strong>Documentação enxuta.</strong> Menos exigências que uma operação com garantia imobiliária, sem registro em cartório de imóveis.",
        ],
        "cautions": [
            ("O prazo precisa caber sob a curva de depreciação",
             "Se a amortização for mais lenta do que a perda de valor do veículo, o saldo devedor pode superar o próprio bem. É o erro mais caro dessa modalidade, e o mais comum."),
            ("Custo efetivo total, não taxa nominal",
             "Vistoria, tarifas, IOF e seguro alteram significativamente o custo final em operações de valor menor, onde os custos fixos pesam proporcionalmente mais."),
            ("Uso profissional intensivo muda a avaliação",
             "Veículos de aplicativo, frota ou transporte têm depreciação acelerada e liquidez diferente, o que restringe prazo e LTV."),
            ("Não é substituto de capital de giro estrutural",
             "Usar um ativo que deprecia rápido para financiar uma necessidade recorrente é uma solução de prazo errado. Nesses casos, indicamos avaliar giro ou garantia imobiliária."),
        ],
        "faq": [
            ("Continuo podendo usar o veículo normalmente?",
             "Sim. A posse e o uso permanecem com o proprietário; o gravame apenas registra a restrição financeira junto ao Detran e impede a transferência até a quitação."),
            ("Veículos de qualquer ano são aceitos?",
             "Não. Cada instituição define limites de idade, e veículos mais antigos costumam ficar fora ou receber LTV bem menor, pela liquidez de revenda reduzida."),
            ("Posso usar um veículo financiado?",
             "Em algumas instituições sim, desde que exista margem entre o valor de mercado e o saldo devedor. A avaliação é caso a caso."),
        ],
        "checklist_title": "Cinco pontos que evitam o erro mais caro dessa modalidade.",
        "checklist_lead": "A vantagem do auto equity é a velocidade. O risco é decidir rápido demais sobre o único ponto que não se corrige depois: o prazo.",
        "checklist": [
            ("Prazo sob a curva de depreciação",
             "Se a amortização for mais lenta do que a perda de valor do veículo, o saldo devedor pode superar o próprio bem. Peça a simulação do saldo devedor projetado, não só a parcela."),
            ("Verificação de ônus antes de simular",
             "Gravame, restrição ou financiamento em aberto interrompem mais operações do que qualquer outro fator. Confirme a situação do veículo antes de entrar em processo."),
            ("Custo efetivo, com vistoria e seguro inclusos",
             "Em operações de valor menor, vistoria, tarifa, IOF e seguro pesam proporcionalmente mais sobre o custo final do que numa operação grande."),
            ("Uso do veículo declarado corretamente",
             "Veículo de aplicativo, frota ou transporte tem depreciação acelerada e liquidez diferente, o que muda prazo e LTV. Declarar isso desde o início evita reavaliação no meio do processo."),
            ("Compare com garantia imobiliária quando a necessidade é recorrente",
             "Usar um ativo que deprecia rápido para financiar uma necessidade de giro estrutural é solução de prazo errado. Se a necessidade se repete, vale avaliar outra estrutura."),
        ],
        "checklist_link": ("Ver o prazo médio de mercado e a curva de depreciação", "conteudos/auto-equity-prazo-e-depreciacao.html"),
        "related_articles": [
            ("Auto equity: prazo e depreciação", "auto-equity-prazo-e-depreciacao"),
            ("Comprar à vista ou financiar: como decidir", "comprar-a-vista-ou-financiar"),
        ],
    },

    # -------------------------------------------------------------- crédito pj
    "credito-pj": {
        "h1": "A instituição certa muda o resultado tanto quanto a taxa.",
        "lead": "2 propostas com a mesma taxa nominal podem ter comportamentos completamente "
                "diferentes ao longo do contrato. A natureza jurídica do credor, a base legal da garantia "
                "e o custo efetivo total explicam a maior parte dessa diferença.",
        "meta": [("Naturezas comparadas", "SCD, SEP, bancos, cooperativas e fintechs"),
                 ("Programas públicos", "Pronampe, Procred 360, PEAC FGI"),
                 ("Critério de escolha", "Custo Efetivo Total e previsibilidade")],
        "variant": 0,
        "context_title": "O que distingue um credor do outro.",
        "context": [
            "Sociedades de Crédito Direto operam com capital próprio, o que tende a produzir maior "
            "previsibilidade de condições em momentos de aperto monetário. Sociedades de Empréstimo entre "
            "Pessoas intermediam recursos de investidores, e podem oferecer condições muito competitivas "
            "quando há apetite forte, com maior sensibilidade a mudanças de cenário.",
            "Bancos universais trazem funding e relacionamento; cooperativas têm política própria e forte "
            "presença regional; fintechs competem em jornada, velocidade e distribuição.",
            "Sobre isso se somam os mecanismos públicos de garantia, que alteram a estrutura possível ao "
            "reduzir a exigência de garantia real para empresas elegíveis.",
        ],
        "pull": "Nenhuma dessas categorias é superior às outras em abstrato. A pergunta correta é qual delas se comporta melhor no prazo e no cenário da operação em questão.",
        "problems_title": "Quando essa comparação faz diferença",
        "problems": [
            "A empresa recebeu propostas de instituições diferentes e não tem como compará-las de forma justa.",
            "A taxa oferecida parece boa, mas as condições acessórias não estão claras.",
            "Há dúvida sobre enquadramento em Pronampe, Procred 360 ou PEAC FGI.",
            "A operação exige previsibilidade de renovação, e não apenas uma boa condição inicial.",
        ],
        "how": [
            ("Diagnóstico da necessidade",
             "Definição de valor, prazo, finalidade e tolerância a variação de condições ao longo do contrato."),
            ("Mapeamento de parceiros",
             "Seleção das instituições cujo perfil, apetite e política se encaixam naquela operação específica."),
            ("Avaliação de mecanismos de garantia",
             "Verificação de elegibilidade a programas públicos que reduzem a exigência de garantia real."),
            ("Comparativo e formalização",
             "Apresentação lado a lado por custo efetivo total, com as condições acessórias explicitadas, e condução da formalização."),
        ],
        "audience": [
            ("Empresas com propostas em mãos", "Negócios que já receberam ofertas e precisam de comparação técnica antes de decidir."),
            ("PMEs elegíveis a programas", "Empresas que podem se enquadrar em mecanismos públicos de garantia e desconhecem os critérios."),
            ("Empresas em renovação", "Operações que vencem e precisam ser recontratadas em condições melhores que as vigentes."),
            ("Empresas sem garantia real disponível", "Negócios cujo lastro está em recebíveis e histórico, não em patrimônio imobilizado."),
        ],
        "benefits": [
            "<strong>Comparação por custo efetivo total.</strong> IOF, tarifas, seguros e condições acessórias entram na conta, não apenas a taxa anunciada.",
            "<strong>Leitura de previsibilidade.</strong> Avaliamos como cada natureza de instituição tende a se comportar em cenário de aperto, não só a condição de hoje.",
            "<strong>Enquadramento em programas públicos.</strong> Pronampe, Procred 360 e PEAC FGI podem viabilizar operação sem garantia real para empresas elegíveis.",
            "<strong>Acesso amplo.</strong> Rede de mais de 74 instituições no Brasil e no exterior, o que torna possível recusar uma condição ruim.",
        ],
        "cautions": [
            ("Condição inicial não é condição de renovação",
             "Uma taxa promocional de entrada pode não se sustentar na recontratação. Para necessidade recorrente, previsibilidade vale mais do que o melhor número do primeiro contrato."),
            ("Cláusulas cruzadas restringem operações futuras",
             "Contratos com vencimento antecipado cruzado ou restrição de novo endividamento podem inviabilizar a operação seguinte. Lemos isso antes de recomendar."),
            ("Programa público não é aprovação automática",
             "Os mecanismos de garantia reduzem exigência de colateral, mas a análise de crédito da instituição continua valendo integralmente."),
        ],
        "faq": [
            ("SCD ou SEP: qual é melhor?",
             "Não há resposta única. A SCD tende a ser mais previsível em momentos de aperto monetário, por operar com capital próprio; a SEP pode oferecer condições mais competitivas quando há apetite forte de investidores. Comparamos as 2 para cada caso."),
            ("O que é o Custo Efetivo Total?",
             "É o custo total da operação para o tomador, incluindo taxa de juros, IOF, tarifas, seguros e demais encargos. É o único indicador que permite comparar propostas de instituições diferentes de forma justa."),
            ("Minha empresa se enquadra em Pronampe ou PEAC FGI?",
             "O enquadramento depende de porte, faturamento, setor e situação cadastral, e os critérios são revisados periodicamente. Verificamos a elegibilidade no diagnóstico, antes de estruturar qualquer alternativa."),
        ],
        "checklist_title": "Cinco pontos para comparar propostas de instituições diferentes de forma justa.",
        "checklist_lead": "Duas propostas com a mesma taxa nominal podem se comportar de formas completamente diferentes ao longo do contrato. É isso que essa comparação existe para revelar.",
        "checklist": [
            ("Natureza da instituição",
             "SCD, SEP, banco, cooperativa ou fintech se comportam de forma diferente em momento de aperto monetário. Pergunte, não presuma pelo nome ou pela marca."),
            ("Custo Efetivo Total completo",
             "Some juros, IOF, tarifa e seguro. É o único número que permite comparar propostas de instituições diferentes de forma justa."),
            ("Cláusulas cruzadas",
             "Vencimento antecipado cruzado ou restrição a novo endividamento podem inviabilizar a operação seguinte. Leia isso antes de assinar, não depois."),
            ("Enquadramento em programa público, quando aplicável",
             "Pronampe, Procred 360 e PEAC FGI reduzem a exigência de garantia real para empresas elegíveis, mas não substituem a análise de crédito da instituição."),
            ("Condição de renovação, não só de entrada",
             "Uma taxa promocional de entrada pode não se sustentar na recontratação. Para necessidade recorrente, pergunte sobre previsibilidade, não só sobre o número inicial."),
        ],
        "checklist_link": ("Ver como comparar propostas pelo Custo Efetivo Total", "conteudos/como-comparar-credito-empresarial-pelo-cet.html"),
        "related_articles": [
            ("Como comparar crédito empresarial pelo CET", "como-comparar-credito-empresarial-pelo-cet"),
            ("SCD e SEP: a natureza do credor", "scd-sep-e-a-natureza-do-credor"),
        ],
    },

    # ------------------------------------------------------ estruturação
    "estruturacao-de-credito": {
        "h1": "Quando nenhuma linha de prateleira responde, a operação é desenhada.",
        "lead": "Algumas operações não cabem em um produto único. Exigem combinação de fontes, "
                "garantias em camadas, cronograma próprio e uma formalização coordenada entre "
                "instituições diferentes.",
        "meta": [("Rede", "74+ instituições, Brasil e exterior"),
                 ("Alcance externo", "Inglaterra, Portugal, Suíça, EUA e EAU"),
                 ("Ticket", "A partir de R$ 500 mil")],
        "variant": 1,
        "context_title": "O que caracteriza uma operação estruturada.",
        "context": [
            "Uma operação é estruturada quando o desenho importa mais do que a escolha do produto: valor "
            "acima do apetite de um único credor, garantias de naturezas distintas, cronograma de "
            "desembolso vinculado a marcos, ou finalidade que combina aquisição, obra e capital de giro.",
            "O trabalho passa a ser desenhar a operação: definir a composição de fontes, a prioridade de "
            "cada garantia, os gatilhos de liberação e a sequência de formalização, de modo que cada "
            "instituição enxergue um risco que consegue aceitar.",
            "A rede ampla é o que torna isso possível. Braço financeiro próprio e conexão ativa com mais de "
            "74 instituições no Brasil e no exterior, incluindo Inglaterra, Portugal, Suíça, Estados Unidos "
            "e Emirados Árabes Unidos, permitem montar operações que nenhuma delas assumiria integralmente "
            "sozinha.",
        ],
        "pull": "Nesses casos, o trabalho não é comparar 2 propostas. É construir a operação.",
        "problems_title": "Quando essa estrutura faz sentido",
        "problems": [
            "O valor necessário excede o apetite individual das instituições consultadas.",
            "A operação combina finalidades distintas: aquisição, obra, equipamentos e capital de giro associado.",
            "Há garantias de naturezas diferentes que precisam ser hierarquizadas entre credores.",
            "O desembolso precisa acompanhar marcos de projeto, e não uma data única de liberação.",
            "A empresa precisa reorganizar o passivo e captar recursos novos na mesma operação.",
        ],
        "how": [
            ("Modelagem da operação",
             "Definição de valor total, composição de fontes, prazo de cada tranche, carência e cronograma de desembolso."),
            ("Arquitetura de garantias",
             "Distribuição das garantias entre credores, com definição de prioridade, margem, consentimentos necessários e efeitos cruzados."),
            ("Sondagem de mercado",
             "Apresentação estruturada da operação às instituições com perfil e apetite compatíveis, no Brasil e no exterior."),
            ("Coordenação da formalização",
             "Condução da negociação, alinhamento de condições precedentes e sequenciamento dos registros e assinaturas."),
        ],
        "audience": [
            ("Empresas de médio e grande porte", "Operações corporativas acima de R$ 500 mil com estrutura de capital a recompor."),
            ("Incorporadoras e construtoras", "Operações que combinam terreno, obra, capital de giro associado e recebíveis futuros."),
            ("Grupos com múltiplas empresas", "Estruturas societárias em que garantias e fluxos estão distribuídos entre CNPJs."),
            ("Operações de aquisição", "Compra de concorrente, de ativo produtivo ou de participação, com pagamento em etapas."),
        ],
        "benefits": [
            "<strong>Múltiplas fontes em uma só operação.</strong> Composição entre instituições nacionais, cooperativas, fundos e funding externo, conforme o perfil do risco.",
            "<strong>Garantias hierarquizadas.</strong> Uso eficiente do patrimônio disponível, com prioridade e margens definidas contratualmente.",
            "<strong>Cronograma sob medida.</strong> Desembolso vinculado a marcos verificáveis, e não a uma data arbitrária.",
            "<strong>Coordenação única.</strong> Uma interlocução para o cliente, mesmo quando há vários credores envolvidos.",
        ],
        "cautions": [
            ("Estruturar leva tempo",
             "Operações desenhadas envolvem due diligence, negociação e condições precedentes. Quem tem prazo curto costuma ser melhor atendido por uma linha padronizada, ainda que mais cara."),
            ("Complexidade cobra governança",
             "Múltiplos credores exigem controle rigoroso de prioridade, registro, consentimentos e vencimento cruzado. Sem isso, a operação fica frágil no primeiro imprevisto."),
            ("Nem toda operação deve ser estruturada",
             "Quando uma linha simples resolve, ela resolve. Recomendar estruturação onde não é necessário é encarecer o processo sem contrapartida."),
        ],
        "faq": [
            ("Qual o ticket mínimo?",
             "Para operações corporativas estruturadas, trabalhamos a partir de R$ 500 mil. Abaixo disso, o custo e o prazo da estruturação raramente se justificam frente às linhas padronizadas disponíveis."),
            ("O que significa ter funding no exterior?",
             "Significa acesso a instituições fora do Brasil, em jurisdições nas quais mantemos rede ativa, para operações que se beneficiam de custo ou prazo diferentes dos praticados internamente. A viabilidade depende do perfil da operação e da regulação aplicável."),
            ("Quanto tempo leva uma operação estruturada?",
             "Depende da complexidade, da qualidade da documentação e do número de instituições envolvidas. Apresentamos uma estimativa realista na modelagem, e revisamos essa estimativa sempre que uma condição precedente muda."),
        ],
        "checklist_title": "Quatro pontos que decidem se uma operação precisa ser desenhada.",
        "checklist_lead": "Nem toda necessidade de crédito exige estruturação. Esses pontos ajudam a diferenciar uma operação que precisa ser desenhada de uma que uma linha padronizada já resolve.",
        "checklist": [
            ("O valor excede o apetite de uma única instituição",
             "Quando nenhum credor sozinho assume o valor integral, a composição de fontes deixa de ser opção e passa a ser condição da operação."),
            ("As garantias são de naturezas diferentes",
             "Imóvel, recebível, aval e ativo produtivo pedem hierarquização entre credores. Definir prioridade e margem antes evita conflito na formalização."),
            ("O desembolso precisa seguir marcos, não uma data única",
             "Cronograma físico-financeiro vinculado a etapas verificáveis é característica de operação estruturada, não de linha de prateleira."),
            ("Existe tempo hábil para due diligence",
             "Estruturar leva tempo. Quem tem prazo curto costuma ser melhor atendido por uma linha padronizada, ainda que mais cara."),
        ],
        "checklist_link": ("Ver o processo completo, do diagnóstico à liberação", "como-funciona.html"),
        "related_articles": [
            ("Como conseguir crédito para a empresa", "como-conseguir-credito-para-a-empresa"),
            ("Documentos para solicitar crédito empresarial", "documentos-para-solicitar-credito-empresarial"),
        ],
    },

    # ----------------------------------------------------------- financiamento
    "financiamento": {
        "h1": "Preservar o caixa costuma valer mais do que quitar rápido.",
        "lead": "Financiamento não é o oposto de solidez financeira. É a decisão de manter capital "
                "próprio disponível para o que gera retorno, transferindo a aquisição para uma "
                "estrutura de prazo compatível.",
        "meta": [("Sistemas", "SFH, SBPE, FGTS e recursos de mercado"),
                 ("Prazos", "Até 420 meses conforme a linha e a instituição"),
                 ("Durante a obra", "Encargo incide sobre o valor já liberado")],
        "variant": 2,
        "context_title": "O custo de imobilizar capital próprio.",
        "context": [
            "Comprar à vista elimina o custo financeiro e cria outro, menos visível: o retorno que o capital "
            "deixou de gerar na operação.",
            "A escolha entre financiar e pagar à vista depende do custo efetivo da operação, do retorno "
            "marginal do capital na atividade e do horizonte da decisão. É uma conta, não uma preferência.",
            "A aquisição pode ocorrer por recursos do SBPE, do FGTS, de programas habitacionais ou de "
            "funding de mercado, com a alienação fiduciária como garantia predominante. Cada sistema tem "
            "critério de enquadramento, limite de comprometimento de renda e restrições próprias, e é isso "
            "que avaliamos antes de indicar um caminho.",
        ],
        "pull": "Para uma empresa com giro apertado ou um investidor com pipeline de oportunidades, imobilizar caixa é frequentemente a decisão mais cara das 2.",
        "problems_title": "Quando essa estrutura faz sentido",
        "problems": [
            "Existe uma aquisição relevante e o capital próprio rende mais dentro da operação do que fora dela.",
            "A empresa precisa de imóvel operacional próprio sem comprometer o capital de giro.",
            "A obra tem cronograma definido e o desembolso pode acompanhar o avanço físico.",
            "Há intenção de adquirir terreno e construir, e o custo cartorário de 2 contratos separados pesa.",
        ],
        "how": [
            ("Análise de capacidade",
             "Verificação de renda ou geração de caixa, limite de comprometimento aplicável e enquadramento no sistema pretendido."),
            ("Escolha da estrutura",
             "Definição entre aquisição pronta, construção em terreno próprio ou contrato único de terreno e construção."),
            ("Cronograma e documentação",
             "Em operações de obra, elaboração do cronograma físico-financeiro e designação de responsável técnico com ART ou RRT."),
            ("Formalização e liberação",
             "Registro da garantia e liberação, à vista na aquisição pronta ou por etapa na construção, mediante vistoria."),
        ],
        "audience": [
            ("Empresas adquirindo imóvel operacional", "Sede, galpão ou unidade produtiva, com preservação do capital de giro."),
            ("Investidores imobiliários", "Aquisição com alavancagem controlada, preservando caixa para novas oportunidades."),
            ("Quem vai construir", "Obra em terreno próprio, com liberação vinculada a etapas verificadas."),
            ("Compradores de imóvel comercial", "Operações que não se enquadram em linhas habitacionais tradicionais."),
        ],
        "benefits": [
            "<strong>Preservação de caixa.</strong> O capital próprio permanece disponível para giro, estoque ou novas aquisições.",
            "<strong>Prazos longos.</strong> Linhas habitacionais podem alcançar prazos bastante estendidos, reduzindo o peso da parcela sobre o fluxo mensal.",
            "<strong>Liberação por etapa na obra.</strong> Durante a construção, o encargo incide apenas sobre o valor já liberado, sem amortização de principal.",
            "<strong>Estrutura unificada quando aplicável.</strong> Contrato único de terreno e construção reduz custo cartorário e simplifica a garantia.",
        ],
        "cautions": [
            ("Enquadramento no sistema restringe opções",
             "Regras como a de não possuir outro financiamento ativo no Sistema Financeiro de Habitação podem eliminar alternativas. Verificamos isso no diagnóstico, antes de qualquer expectativa."),
            ("Parcela não é o custo",
             "Prazo longo reduz a parcela e aumenta o total pago. A comparação correta é entre custos efetivos totais, considerando também seguros obrigatórios e tarifas."),
            ("Obra tem risco de orçamento",
             "Insumos, mão de obra, licenciamento e atraso consomem margem. Financiar 100% de um orçamento apertado costuma terminar em aporte não planejado."),
        ],
        "faq": [
            ("Qual a diferença entre financiar a compra e construir?",
             "Na aquisição pronta, o recurso é liberado de uma vez contra a transferência do imóvel. Na construção, a liberação é progressiva e vinculada à validação do avanço físico da obra, com amortização iniciando após a conclusão."),
            ("Pessoa jurídica pode financiar imóvel?",
             "Sim, com estruturas e critérios próprios, diferentes das linhas habitacionais para pessoa física. O enquadramento depende do porte, da atividade e da finalidade do imóvel."),
            ("O que é a taxa que incide durante a obra?",
             "É o encargo aplicado sobre o valor já desembolsado enquanto a obra ocorre, antes do início da amortização do principal. O percentual varia por instituição e por linha."),
        ],
        "checklist_title": "Cinco pontos antes de comparar financiar com pagar à vista.",
        "checklist_lead": "A escolha entre financiar e pagar à vista é uma conta, não uma preferência. Esses pontos garantem que a conta está completa.",
        "checklist": [
            ("Retorno do capital fora da operação",
             "Compare o custo efetivo do financiamento com o retorno que o mesmo capital geraria mantido em giro ou em outra aplicação da empresa."),
            ("Enquadramento no sistema pretendido",
             "SFH, SBPE, FGTS e recursos de mercado têm critério, limite de comprometimento e restrições próprios. Confirme o enquadramento antes de comparar taxa."),
            ("Custo efetivo total, durante e depois da obra",
             "Durante a construção, o encargo incide sobre o valor já liberado, sem amortização de principal. Inclua isso na comparação, não só a taxa depois da conclusão."),
            ("Folga no orçamento da obra",
             "Financiar o limite de um orçamento apertado transfere qualquer variação de custo para aporte próprio não planejado."),
            ("Estrutura única de terreno e obra, quando viável",
             "Contrato único reduz custo cartorário e simplifica a garantia, mas exige que o projeto esteja maduro no momento da contratação."),
        ],
        "checklist_link": ("Ver como decidir entre comprar à vista ou financiar", "conteudos/comprar-a-vista-ou-financiar.html"),
        "related_articles": [
            ("Comprar à vista ou financiar: como decidir", "comprar-a-vista-ou-financiar"),
            ("Construção financiada: liberação por medição", "construcao-financiada-liberacao-por-medicao"),
        ],
    },

    # -------------------------------------------------- aquisição e construção
    "aquisicao-e-construcao": {
        "h1": "Terreno, obra e cronograma são uma operação só.",
        "lead": "Construir é mais complexo do que comprar pronto porque o desembolso precisa acompanhar "
                "avanço físico, orçamento, licenças e medição. Quando essas peças são contratadas "
                "separadamente, a margem escorre pelos vãos.",
        "meta": [("Estrutura", "Contrato único de terreno e obra, quando viável"),
                 ("Liberação", "Por vistoria de avanço físico"),
                 ("Exigência", "Responsável técnico com ART ou RRT")],
        "variant": 0,
        "context_title": "Por que o cronograma comanda a operação.",
        "context": [
            "Em uma aquisição pronta, o crédito é liberado contra um ativo que já existe. Em uma obra, o "
            "ativo é construído com o próprio crédito, e o credor libera contra avanço verificado. Isso muda "
            "tudo: orçamento, medição, licenciamento e responsabilidade técnica passam a fazer parte da "
            "estrutura financeira, não apenas da execução.",
            "Para pessoa física, existem linhas para construir em terreno próprio ou para adquirir terreno e "
            "construir. Para incorporadoras e empresas, a operação pode incluir aquisição de terreno, obras, "
            "equipamentos, instalações, despesas pré-operacionais e capital de giro associado ao "
            "empreendimento financiado.",
            "Insumos, mão de obra, licenciamento, atraso, distrato e baixa velocidade de vendas consomem "
            "margem antes que o custo financeiro apareça no resultado.",
        ],
        "pull": "O principal risco não é a taxa: é o descasamento entre orçamento e valor de venda.",
        "problems_title": "Quando essa estrutura faz sentido",
        "problems": [
            "Há terreno identificado e intenção de construir, com cronograma e orçamento definidos.",
            "A incorporação exige desembolso escalonado e o capital próprio não deve ser imobilizado no terreno.",
            "A empresa precisa expandir instalações produtivas sem interromper o giro.",
            "O empreendimento combina obra, equipamentos e capital de giro associado em uma mesma decisão.",
        ],
        "how": [
            ("Viabilidade da operação",
             "Análise de orçamento, cronograma físico-financeiro, licenciamento, velocidade de vendas esperada e cobertura de juros durante a obra."),
            ("Estrutura contratual",
             "Definição entre contratos separados de terreno e obra ou contrato único, comparando custo cartorário, prazo e exigências de garantia."),
            ("Responsabilidade técnica",
             "Designação do responsável técnico e emissão de ART ou RRT, obrigatórias durante toda a execução."),
            ("Liberação por medição",
             "Desembolsos condicionados a vistoria de avanço físico, com amortização do principal iniciando após a conclusão."),
        ],
        "audience": [
            ("Incorporadoras", "Empreendimentos com cronograma, VGV projetado e necessidade de casar desembolso com vendas."),
            ("Construtoras e empreiteiras", "Obras próprias e expansão de capacidade instalada."),
            ("Empresas em expansão física", "Galpões, unidades produtivas e ampliação de instalações operacionais."),
            ("Proprietários de terreno", "Quem já detém o terreno e precisa financiar exclusivamente a construção."),
        ],
        "benefits": [
            "<strong>Desembolso alinhado à obra.</strong> O recurso entra conforme o avanço, o que reduz custo financeiro ocioso.",
            "<strong>Capital próprio preservado.</strong> O terreno deixa de consumir integralmente o caixa disponível para a operação.",
            "<strong>Contrato único quando viável.</strong> Terreno e construção em uma só estrutura reduzem custo cartorário e simplificam a garantia.",
            "<strong>Amortização após a conclusão.</strong> Durante a obra incide apenas o encargo sobre o valor liberado, sem pagamento de principal.",
        ],
        "cautions": [
            ("Orçamento apertado é risco financeiro, não operacional",
             "Financiar o limite de um orçamento sem folga transfere qualquer variação de custo para aporte próprio não planejado, geralmente no pior momento do ciclo."),
            ("Atraso custa 2 vezes",
             "Prorrogação estende o período de incidência do encargo sobre o valor liberado e adia o início dos repasses, comprimindo o fluxo pelos dois lados."),
            ("Velocidade de vendas é premissa, não certeza",
             "Cronogramas financeiros construídos sobre absorção otimista são a causa mais frequente de renegociação em ciclo longo. Trabalhamos com cenário conservador na estruturação."),
            ("Licenciamento antecede o crédito",
             "Pendência de aprovação, regularização do terreno ou averbação inviabiliza liberação, mesmo com a operação aprovada."),
        ],
        "faq": [
            ("É melhor contratar terreno e obra separadamente ou em contrato único?",
             "Depende do caso. O contrato único tende a reduzir custo cartorário e simplificar a garantia, mas exige que o projeto esteja suficientemente maduro no momento da contratação. Comparamos as 2 estruturas na viabilidade."),
            ("O que é liberação por medição?",
             "É o desembolso condicionado à verificação do avanço físico da obra, feita por vistoria. Cada etapa concluída e validada libera a parcela correspondente do crédito."),
            ("O responsável técnico é obrigatório?",
             "Em operações de construção financiada, sim. A ART ou RRT acompanha toda a execução e é condição para as liberações e para a conclusão da operação."),
        ],
        "checklist_title": "Cinco pontos que decidem se o cronograma sustenta a operação.",
        "checklist_lead": "Numa obra, o crédito é liberado contra avanço verificado, não contra um ativo que já existe. Esses pontos evitam que o cronograma financeiro se descole da obra real.",
        "checklist": [
            ("Orçamento com folga, não no limite",
             "Financiar o limite de um orçamento sem margem transfere qualquer variação de custo para aporte próprio não planejado, geralmente no pior momento do ciclo."),
            ("Responsável técnico com ART ou RRT",
             "Obrigatório durante toda a execução, e condição para as liberações e para a conclusão da operação."),
            ("Estrutura contratual: separada ou única",
             "Contrato único de terreno e obra tende a reduzir custo cartorário, mas exige projeto suficientemente maduro no momento da contratação. Compare as 2 estruturas antes de escolher."),
            ("Cenário conservador de velocidade de vendas",
             "Cronogramas financeiros construídos sobre absorção otimista são a causa mais frequente de renegociação em ciclo longo."),
            ("Licenciamento resolvido antes da contratação",
             "Pendência de aprovação, regularização do terreno ou averbação inviabiliza liberação, mesmo com a operação já aprovada."),
        ],
        "checklist_link": ("Ver como funciona a liberação por medição", "conteudos/construcao-financiada-liberacao-por-medicao.html"),
        "related_articles": [
            ("Construção financiada: liberação por medição", "construcao-financiada-liberacao-por-medicao"),
            ("Documentos para solicitar crédito empresarial", "documentos-para-solicitar-credito-empresarial"),
        ],
    },

    # ------------------------------------------ recebíveis e mercado de capitais
    "mercado-de-capitais": {
        "h1": "O recebível pode virar caixa hoje, ou virar título amanhã.",
        "lead": "Antecipar um recebível troca desconto por liquidez imediata. Estruturar CRI, CRA ou "
                "uma emissão de debênture transforma a mesma carteira, ou o mesmo passivo, em acesso "
                "direto a investidores. São operações de naturezas diferentes, e a escolha entre elas "
                "depende do porte, do prazo e de quanto a empresa está disposta a expor ao mercado.",
        "meta": [("Regulação", "Lei nº 9.514/1997 (CRI), Lei nº 11.076/2004 (CRA), Lei nº 14.430/2022 (securitização)"),
                 ("Cessão de recebíveis", "Direta, ou via FIDC sob Resolução CVM nº 175/2022"),
                 ("Debênture por limitada", "Admitida pela Nota Técnica DREI nº 135/2026, sem registro uniforme ainda")],
        "variant": 1,
        "context_title": "Duas operações que resolvem problemas diferentes.",
        "context": [
            "Antecipação de recebíveis é cessão de crédito: a empresa transfere duplicatas, contratos ou "
            "faturas a um cessionário, uma instituição financeira, uma securitizadora ou um Fundo de "
            "Investimento em Direitos Creditórios, e recebe o valor à vista, descontada uma taxa. O "
            "recurso entra rápido porque o lastro já existe e já tem prazo definido.",
            "CRI, CRA e debênture são outra categoria. Em vez de vender um recebível que já existe, a "
            "empresa, ou uma securitizadora em nome dela, emite um título que remunera quem o compra. "
            "O CRI é lastreado em crédito imobiliário, o CRA em crédito do agronegócio, e a debênture é "
            "dívida direta da emissora, sem lastro específico. As 3 dão acesso a investidores "
            "institucionais e pessoa física, fora do balanço de um banco.",
            "A Lei nº 14.430/2022 unificou o regime das securitizadoras e ampliou quem pode emitir CRI e "
            "CRA, o que tornou essas estruturas mais acessíveis do que eram há poucos anos. Do lado da "
            "debênture, uma mudança recente: a Nota Técnica nº 135/2026 do DREI passou a admitir emissão "
            "por sociedade limitada, historicamente restrita a sociedades anônimas, desde que o contrato "
            "social preveja a aplicação supletiva da Lei das S.A., ainda sem normatização de registro "
            "uniforme entre as juntas comerciais.",
        ],
        "pull": "A antecipação troca desconto por velocidade. A emissão troca abertura por escala. Nenhuma das 2 é gratuita, e cada uma cobra de um jeito diferente.",
        "problems_title": "Quando essa estrutura faz sentido",
        "problems": [
            "A empresa tem uma carteira de recebíveis recorrente e usa desconto avulso e caro em vez de uma linha estruturada de cessão.",
            "Há um projeto ou uma dívida grande o bastante para justificar acesso direto ao mercado, e não só crédito bancário.",
            "A empresa já comprometeu boa parte das linhas bancárias tradicionais, mas tem patrimônio ou fluxo capaz de sustentar um título.",
            "Existe interesse em ampliar a base de credores para reduzir a dependência de um único banco ou de poucas instituições.",
        ],
        "how": [
            ("Leitura da carteira ou do passivo",
             "Levantamento dos recebíveis disponíveis, ou da necessidade de captação, para definir se o caminho é cessão simples, FIDC, CRI, CRA ou debênture."),
            ("Estruturação do veículo",
             "Escolha entre cessão direta, fundo ou emissão de título, com securitizadora, agente fiduciário e formato de oferta definidos conforme porte e prazo."),
            ("Precificação e distribuição",
             "Apresentação da operação a investidores institucionais, com taxa e condições definidas pela demanda real, não por tabela de balcão."),
            ("Formalização e liquidação",
             "Emissão do título ou fechamento da cessão, registro nos sistemas aplicáveis e liberação do recurso à empresa."),
        ],
        "audience": [
            ("Empresas com recebíveis recorrentes", "Faturamento com prazo concedido a clientes, hoje financiado por desconto avulso ou linha bancária cara."),
            ("Empresas de médio e grande porte", "Passivo ou projeto grande o bastante para justificar o custo e o prazo de uma estruturação de mercado de capitais."),
            ("Incorporadoras e produtores rurais", "Carteiras de recebíveis imobiliários ou do agronegócio, o lastro natural de CRI e CRA."),
            ("Empresas que buscam diversificar credores", "Negócios que já usam crédito bancário e querem reduzir a dependência de poucas instituições."),
        ],
        "benefits": [
            "<strong>Acesso direto a investidores.</strong> CRI, CRA e debênture chegam a quem investe sem depender do apetite de um banco específico.",
            "<strong>Isenção fiscal para o investidor pessoa física.</strong> CRI e CRA são isentos de Imposto de Renda para pessoa física, o que costuma reduzir a taxa exigida frente a título de risco comparável.",
            "<strong>Antecipação sem esperar o vencimento.</strong> A cessão de recebíveis converte prazo concedido a cliente em caixa imediato.",
            "<strong>Rede que cobre os 2 lados.</strong> Acesso a securitizadoras e FIDCs para cessão, e a investidores institucionais para emissão, dentro da mesma estruturação.",
        ],
        "cautions": [
            ("Emissão não é aprovação automática de mercado",
             "Um título mal precificado ou mal distribuído pode não encontrar comprador, ou só encontrar a um custo pior do que o crédito bancário que se pretendia substituir."),
            ("Debênture por limitada ainda é terreno novo",
             "A Nota Técnica do DREI abriu o caminho, mas a ausência de normatização registral uniforme entre juntas comerciais pode gerar divergência de interpretação. Recomendamos essa estrutura com essa ressalva explícita."),
            ("Recebível já cedido não pode lastrear outra operação",
             "Mapear o que já está comprometido evita a reprovação tardia, depois de semanas de processo."),
            ("Custo de estruturação pesa em operações pequenas",
             "Securitizadora, agente fiduciário e distribuição têm custo fixo, que só se dilui em operações de porte relevante. Abaixo de um certo valor, crédito bancário ou cessão direta costuma ser mais eficiente."),
        ],
        "faq": [
            ("Qual a diferença entre CRI, CRA e debênture?",
             "CRI e CRA são lastreados em créditos específicos, imobiliário e do agronegócio respectivamente, e emitidos por uma securitizadora. Debênture é dívida direta da empresa emissora, sem lastro específico, historicamente restrita a sociedades anônimas."),
            ("Uma sociedade limitada pode emitir debênture?",
             "Passou a ser admitido pela Nota Técnica SEI nº 135/2026 do DREI, desde que o contrato social preveja a aplicação supletiva da Lei das S.A. e a empresa adote os livros de registro exigidos. A matéria ainda não tem normatização registral padronizada entre todas as juntas comerciais."),
            ("Antecipação de recebíveis compromete o limite de crédito bancário da empresa?",
             "Não diretamente. A cessão de recebíveis é uma operação à parte e, bem estruturada, amplia a fonte de recurso disponível em vez de consumir limite bancário existente."),
            ("Que porte de operação justifica uma emissão de CRI, CRA ou debênture?",
             "Depende dos custos fixos da estruturação, que incluem securitizadora, agente fiduciário e distribuição. Avaliamos, no diagnóstico, se o porte da operação sustenta esses custos ou se cessão direta e crédito bancário resolvem com mais eficiência."),
        ],
        "checklist_title": "Quatro pontos antes de estruturar uma cessão ou uma emissão.",
        "checklist_lead": "Antecipar um recebível e emitir um título resolvem problemas diferentes, com riscos diferentes. Esses pontos ajudam a escolher, e a não superestimar o que o mercado vai pagar.",
        "checklist": [
            ("O que já está comprometido",
             "Recebível já cedido a outra operação não pode lastrear uma nova. Mapear isso antes evita reprovação tardia, depois de semanas de processo."),
            ("Porte que sustenta o custo fixo da estruturação",
             "Securitizadora, agente fiduciário e distribuição têm custo fixo, que só se dilui em operações de porte relevante. Abaixo de um certo valor, cessão direta ou crédito bancário costuma ser mais eficiente."),
            ("Precificação pela demanda real, não pela tabela de balcão",
             "Um título mal precificado pode não encontrar comprador, ou só encontrar a um custo pior do que o crédito bancário que se pretendia substituir."),
            ("Terreno novo pede ressalva explícita",
             "A emissão de debênture por sociedade limitada foi admitida pela Nota Técnica nº 135/2026 do DREI, mas ainda sem normatização registral uniforme entre juntas comerciais. Avalie essa estrutura com essa ressalva em mente."),
        ],
        "checklist_link": ("Ver a diferença entre SCD e SEP na natureza do credor", "conteudos/scd-sep-e-a-natureza-do-credor.html"),
        "related_articles": [
            ("SCD e SEP: a natureza do credor", "scd-sep-e-a-natureza-do-credor"),
            ("Custo real da dívida: rotativo e garantia real", "custo-real-da-divida-rotativo-e-garantia-real"),
        ],
    },
}


def _table_compare(path):
    rows = [
        ("Déficit de caixa recorrente", "Giro rotativo ou recebíveis, com reestruturação quando necessário", "Curto e médio"),
        ("Investimento ou expansão", "Giro associado a projeto ou financiamento de investimento", "Médio e longo"),
        ("Quitar dívida cara", "Home equity bem dimensionado", "Longo"),
        ("Obra residencial ou produtiva", "Financiamento de construção", "Médio e longo"),
        ("Comprar imóvel pronto", "Financiamento de aquisição", "Longo"),
        ("Liquidez com veículo próprio", "Auto equity", "Curto e médio"),
        ("Antecipar recebível ou acessar mercado de capitais", "Recebíveis e Mercado de Capitais", "Curto a longo"),
    ]
    trs = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return f"""<div class="prose" style="max-width:none"><div class="tablewrap">
      <table>
        <thead><tr><th>Necessidade</th><th>Estrutura mais aderente</th><th>Prazo relativo</th></tr></thead>
        <tbody>{trs}</tbody>
      </table>
    </div></div>"""


def hub():
    path = "solucoes.html"
    trail = [("Início", "index.html"), ("Soluções", None)]

    body = B.pagehead(
        path, trail, "Soluções",
        "8 estruturas. A dificuldade não é escolher, é dimensionar.",
        "Cada uma destas soluções resolve um problema específico e cria um risco específico. "
        "A página de cada uma descreve as 2 coisas.",
        meta=[("Estruturas", "Giro, PJ, garantia real, financiamento e obra"),
              ("Critério de escolha", "Prazo, lastro e finalidade"),
              ("Comparação", "Por Custo Efetivo Total")],
        variant=0, image_slot="solucoes")

    rows = ""
    for i, s in enumerate(SOLUTIONS, 1):
        chips = "".join(f'<span class="chip">{c}</span>' for c in s["chips"])
        rows += f"""<a class="artrow" href="{B.rel(path, 'solucoes/' + s['slug'] + '.html')}">
          <div class="artrow__meta">{B.artrow_img(path, s.get('image'), s['title'])}<b>{i:02d}</b>{s['kicker']}</div>
          <div>
            <h3>{s['title']}</h3>
            <p>{s['short']}</p>
            <div class="solpanel__facts" style="margin-top:1rem">{chips}</div>
          </div>
        </a>"""

    body += f"""<section class="band">
  <div class="shell">
    <h2 class="sr">As 8 estruturas</h2>
    <div class="artlist">{rows}</div>
  </div>
</section>"""

    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Adequação", "Qual estrutura para qual necessidade.",
               "A tabela abaixo é um ponto de partida, não uma recomendação. O que decide, em cada caso, é a combinação entre prazo, lastro e finalidade.")}
    <div data-reveal>{_table_compare(path)}</div>
    <p class="notice mt-3">Nenhuma estrutura é adequada por si mesma. A inadequação mais comum não é escolher o produto errado: é escolher o prazo errado para o produto certo.</p>
  </div>
</section>"""

    body += B.cta_band(path, "Descreva a operação. Indicamos a estrutura.",
                       "Se nenhuma das 7 responder ao seu caso, provavelmente a resposta é uma combinação delas.",
                       secondary=("Ver o processo", "como-funciona.html"), tone="ink")

    return {
        "path": path, "nav_key": "solucoes.html", "over": True,
        "title": "Soluções de crédito estruturado | Acrópole Capital",
        "desc": ("8 estruturas de crédito: capital de giro, home equity, auto equity, crédito PJ, "
                 "financiamento, construção e mercado de capitais. O que resolve, e onde falha."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail), {
            "@context": "https://schema.org", "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": s["title"],
                 "url": B.SITE["domain"] + "/solucoes/" + s["slug"]}
                for i, s in enumerate(SOLUTIONS)],
        }],
    }


def solution_page(slug):
    s = SOL_BY_SLUG[slug]
    d = DETAIL[slug]
    path = f"solucoes/{slug}.html"
    trail = [("Início", "index.html"), ("Soluções", "solucoes.html"), (s["title"], None)]

    body = B.pagehead(path, trail, s["kicker"], d["h1"], d["lead"], d["meta"], d["variant"],
                       image_slot="solucao-" + slug)

    # Quebra o bloco de parágrafos corridos com uma citação de destaque no meio
    # (mesmo recurso da home, B.pullquote) em vez de empilhar 3 parágrafos sem
    # respiro visual algum. A frase vem de dentro do próprio texto de contexto
    # de cada página (chave "pull"), nunca é copy nova.
    first, rest = d["context"][:1], d["context"][1:]
    ctx_top = "".join(f"<p>{p}</p>" for p in first)
    ctx_bottom = "".join(f"<p>{p}</p>" for p in rest)
    pull = B.pullquote(d["pull"]) if d.get("pull") else ""
    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("Contexto", d['context_title'])}
    <div data-reveal class="stack-2"><div class="lead">{ctx_top}</div>{pull}<div class="lead">{ctx_bottom}</div></div>
  </div>
</section>"""

    body += f"""<section class="band band--stone band--snug">
  <div class="shell">
    {B.sechead(d.get("problems_kicker", "Aplicação"), d["problems_title"])}
    <div>{B.pointlist(d["problems"], split=True)}</div>
  </div>
</section>"""

    body += f"""<section class="band">
  <div class="shell">
    {B.sechead("Como funciona", "Da avaliação à liberação.",
               note="O processo institucional completo, com documentação e critérios, está descrito na página dedicada.",
               link=("Ver o processo completo", "como-funciona.html"), path=path)}
    <div class="mt-4">{B.sequence(d["how"])}</div>
  </div>
</section>"""

    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Para quem é", "Perfis em que essa estrutura costuma ser a resposta certa.")}
    {B.deflist(d["audience"], split=True)}
    <div class="mt-4">
      {B.sechead("Benefícios", "O que a estrutura entrega.")}
      {B.benefits_cards(d["benefits"])}
    </div>
  </div>
</section>"""

    body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Cuidados", "O que costuma dar errado, e por quê.",
               "Esta seção existe em todas as páginas de solução. Uma recomendação que só apresenta vantagens não é uma recomendação.")}
    <div class="cols cols--1-1">
      <div>{B.deflist(d["cautions"][:2])}</div>
      <div>{B.deflist(d["cautions"][2:]) if len(d["cautions"]) > 2 else ""}</div>
    </div>
  </div>
</section>"""

    if d.get("checklist"):
        checklist_link = (f'<div class="mt-3">{B.tlink(*d["checklist_link"], path)}</div>'
                           if d.get("checklist_link") else "")
        body += f"""<section class="band band--stone">
  <div class="shell">
    {B.sechead("Antes de assinar", d["checklist_title"], d.get("checklist_lead"))}
    <div class="mt-4">{B.sequence(d["checklist"])}</div>
    {checklist_link}
  </div>
</section>"""

    others = [x for x in SOLUTIONS if x["slug"] != slug][:3]
    rel_rows = [
        (o["title"], o["short"], "solucoes/" + o["slug"] + ".html", "Ver a página") for o in others
    ]
    related_articles_html = ""
    if d.get("related_articles") or d.get("tool_link"):
        links = "".join(
            f'<div class="mt-2">{B.tlink(label, "conteudos/" + art_slug + ".html", path)}</div>'
            for label, art_slug in d.get("related_articles", [])
        )
        if d.get("tool_link"):
            links += f'<div class="mt-2">{B.tlink(d["tool_link"][0], d["tool_link"][1], path)}</div>'
        related_articles_html = f'<div class="mt-3">{links}</div>'
    body += f"""<section class="band">
  <div class="shell shell--tight">
    {B.sechead("Dúvidas frequentes", "Sobre " + s["title"] + ".")}
    {B.accordion(d["faq"], "faq-" + slug)}
    <p class="notice mt-3">{CONDITIONS_NOTICE}</p>
    {related_articles_html}
  </div>
</section>
<section class="band band--stone band--snug">
  <div class="shell">
    {B.sechead("Outras estruturas", "Frequentemente avaliadas em conjunto.")}
    {B.linkcards(path, rel_rows)}
  </div>
</section>"""

    body += B.cta_band(path, f"Avaliar {s['title']} para o seu caso.",
                       "A análise inicial não gera compromisso e não consulta bureau de crédito sem sua autorização expressa.",
                       secondary=("Ver todas as soluções", "solucoes.html"), tone="petrol")

    # Título de SEO com rótulo mais curto que o kicker exibido na página,
    # só para caber no limite de exibição do Google (~60 caracteres) nesta
    # estrutura, cujo título já é o mais longo das oito.
    seo_kicker = {
        "estruturacao-de-credito": "Sob medida",
        "mercado-de-capitais": "Cessão e emissão",
    }.get(slug, s["kicker"])
    # Título de SEO mais curto que o nome de exibição da estrutura, só para
    # esta caber no limite de exibição do Google (~62 caracteres) junto do
    # sufixo institucional, sem afetar o título exibido em nenhuma outra
    # parte do site (menu, h1, hub).
    seo_title = {
        "mercado-de-capitais": "Mercado de Capitais",
    }.get(slug, s["title"])

    return {
        "path": path, "nav_key": "solucoes.html", "over": True,
        "title": f"{seo_title}: {seo_kicker} | Acrópole Capital",
        # O Google corta a descrição por volta de 160 caracteres: o sufixo
        # institucional só entra se couber inteiro, senão a frase apareceria
        # truncada no meio no resultado da busca.
        "desc": B.fit_desc(s["short"], "Aplicações, benefícios e cuidados."),
        # Mesma lógica do artigo: identifica a estrutura de crédito de
        # origem para o CRM, como campo oculto no popup de captação.
        "lead_context": {"solution": slug, "category": s["kicker"]},
        "body": body,
        "schema": [B.breadcrumb_schema(trail), B.faq_schema(d["faq"]), {
            "@context": "https://schema.org", "@type": "Service",
            "name": s["title"], "serviceType": s["kicker"],
            "provider": {"@type": "FinancialService", "name": "Acrópole Capital"},
            "areaServed": "BR", "description": s["short"],
        }],
    }



# --------------------------------------------------- calculadora de giro
# Fórmula: ciclo financeiro (PME + PMR - PMP) em dias, multiplicado pelo
# custo operacional médio diário (custo mensal / 30). A mesma conta usada
# no exemplo ilustrativo do artigo "como calcular a necessidade de capital
# de giro". Roda inteiramente no navegador, sem envio de dado nenhum.
GIRO_CALC_JS = r"""
function acrGiroOnlyDigits(v) { return (v || '').replace(/\D+/g, ''); }
function acrGiroBRL(n) {
  return 'R$ ' + Math.round(n).toLocaleString('pt-BR');
}

function acrGiroInit() {
  const form = document.querySelector('[data-giro-form]');
  if (!form) return;
  const reducedMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  const result = document.querySelector('[data-giro-result]');
  const placeholder = document.querySelector('[data-giro-placeholder]');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const pme = Number(acrGiroOnlyDigits(form.querySelector('[name="pme"]').value || '0'));
    const pmr = Number(acrGiroOnlyDigits(form.querySelector('[name="pmr"]').value || '0'));
    const pmp = Number(acrGiroOnlyDigits(form.querySelector('[name="pmp"]').value || '0'));
    const custoMensal = Number(acrGiroOnlyDigits(form.querySelector('[name="custo"]').value || '0'));

    const ciclo = pme + pmr - pmp;
    const custoDiario = custoMensal / 30;
    const ncg = ciclo * custoDiario;

    result.querySelector('[data-giro-ciclo]').textContent = ciclo + ' dias';
    result.querySelector('[data-giro-custodia]').textContent = acrGiroBRL(custoDiario) + ' / dia';
    result.querySelector('[data-giro-ncg]').textContent = acrGiroBRL(Math.max(ncg, 0));
    result.querySelector('[data-giro-warn]').hidden = ciclo >= 0;

    if (placeholder) placeholder.hidden = true;
    result.hidden = false;
    if (window.matchMedia('(max-width: 899px)').matches) {
      result.scrollIntoView({ block: 'start', behavior: reducedMotion ? 'auto' : 'smooth' });
    }
  });

  const currencyFields = form.querySelectorAll('[data-mask="currency"]');
  currencyFields.forEach(function (input) {
    input.addEventListener('input', function () {
      // Descarta um sufixo de centavos (",50"/".50") antes de raspar os
      // dígitos — mesmo ajuste do simulador de programas: sem isso, digitar
      // "1.000,50" virava R$ 100.050 em vez de R$ 1.000.
      const d = acrGiroOnlyDigits(input.value.replace(/[.,]\d{1,2}$/, '')).slice(0, 12);
      input.value = d ? 'R$ ' + Number(d).toLocaleString('pt-BR') : '';
    });
  });

  const digitFields = form.querySelectorAll('[data-mask="digits"]');
  digitFields.forEach(function (input) {
    input.addEventListener('input', function () {
      input.value = acrGiroOnlyDigits(input.value).slice(0, 5);
    });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', acrGiroInit);
} else {
  acrGiroInit();
}
"""


def calculadora_giro():
    path = "calculadora-capital-de-giro.html"
    trail = [("Início", "index.html"), ("Soluções", "solucoes.html"), ("Calculadora de capital de giro", None)]

    body = B.pagehead(
        path, trail, "Ferramenta",
        "Calculadora de necessidade de capital de giro",
        "Informe o prazo médio de estoque, de recebimento e de pagamento, e o custo operacional "
        "médio mensal da empresa. O resultado é uma estimativa do ciclo financeiro e do valor "
        "aproximado de capital de giro que ele consome, calculada aqui mesmo, sem enviar nenhum dado.",
        meta=[("Cálculo", "Ciclo financeiro × custo operacional diário"),
              ("Uso", "Educativo, não substitui análise contábil"),
              ("Dado enviado", "Nenhum, a conta roda no navegador")],
        variant=0, image_slot="calculadora-giro")

    body += f"""<section class="band">
  <div class="shell">
  <div class="toolcard">
    {B.sechead("Calculadora", "Estimativa do ciclo financeiro e da necessidade de giro",
                "Preencha os três prazos médios e o custo operacional mensal aproximado. O resultado "
                "aparece ao lado, e dá para recalcular quantas vezes quiser.")}
    <div class="cols cols--1-1 mt-3">
      <div>
        <form data-giro-form novalidate>
          <div class="fgrid fgrid--2">
            <div class="field">
              <label for="giro-pme">Prazo médio de estoque (dias)</label>
              <input type="text" inputmode="numeric" id="giro-pme" name="pme" data-mask="digits" placeholder="Ex.: 45" required>
            </div>
            <div class="field">
              <label for="giro-pmr">Prazo médio de recebimento (dias)</label>
              <input type="text" inputmode="numeric" id="giro-pmr" name="pmr" data-mask="digits" placeholder="Ex.: 30" required>
            </div>
            <div class="field">
              <label for="giro-pmp">Prazo médio de pagamento a fornecedores (dias)</label>
              <input type="text" inputmode="numeric" id="giro-pmp" name="pmp" data-mask="digits" placeholder="Ex.: 20" required>
            </div>
            <div class="field">
              <label for="giro-custo">Custo operacional médio mensal</label>
              <input type="text" inputmode="numeric" id="giro-custo" name="custo" data-mask="currency" placeholder="R$ 0" required>
            </div>
          </div>
          <div class="formfoot formfoot--wide" style="border-top:0;padding-top:0;margin-top:1.5rem">
            <button type="submit" class="btn">Calcular estimativa</button>
          </div>
        </form>
      </div>

      <div class="callout">
        <div data-giro-placeholder>
          <span class="tag">Resultado</span>
          <p class="small muted mt-2" style="margin-bottom:0">Preencha os prazos e o custo ao lado e clique em "Calcular estimativa" para ver aqui o ciclo financeiro e a necessidade de giro estimada.</p>
        </div>
        <div data-giro-result hidden role="status" aria-live="polite">
          {B.sechead("Resultado", "Estimativa para o cenário informado")}
          <p data-giro-warn hidden class="notice mt-2">Ciclo financeiro negativo ou zero: nesse cenário, a operação tende a se financiar sozinha, sem gerar necessidade de capital de giro.</p>
          <div class="deflist mt-2">
            <div class="deflist__row"><dt>Ciclo financeiro</dt><dd data-giro-ciclo class="figures"></dd></div>
            <div class="deflist__row"><dt>Custo operacional diário</dt><dd data-giro-custodia class="figures"></dd></div>
            <div class="deflist__row"><dt>Necessidade de giro estimada</dt><dd data-giro-ncg class="figures"></dd></div>
          </div>
          <p class="xs muted mt-3">Cálculo ilustrativo: ciclo financeiro (prazo de estoque mais prazo de recebimento, menos prazo de pagamento) multiplicado pelo custo operacional médio diário. Não considera sazonalidade, variação de margem ao longo do ano nem o perfil de crédito da empresa, e não substitui uma análise contábil ou financeira detalhada.</p>
          <div class="mt-3">
            {B.btn("Avaliar as opções de capital de giro com um especialista", "contato.html", path, variant="btn--block", attrs=' data-lead-modal')}
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</section>"""

    body += f'<script>{GIRO_CALC_JS}</script>'

    body += f"""<section class="band band--stone band--snug">
  <div class="shell shell--tight">
    {B.sechead("Antes de usar o resultado", "O que essa estimativa não substitui.")}
    <p class="notice mt-2">Este cálculo é educativo e ilustrativo. Ele não considera sazonalidade, mudanças de margem, nem o perfil de crédito da empresa, e não constitui simulação de nenhuma instituição financeira nem promessa de aprovação. Para dimensionar a necessidade real de giro, o passo seguinte é uma análise do fluxo de caixa completo da empresa.</p>
    <div class="mt-3 stack-2">
      {B.tlink("Como calcular a necessidade de capital de giro da empresa", "conteudos/como-calcular-necessidade-de-capital-de-giro.html", path)}
      {B.tlink("Ver a página de Capital de Giro", "solucoes/capital-de-giro.html", path)}
    </div>
  </div>
</section>"""

    body += B.cta_band(
        path, "Quer transformar essa estimativa em uma proposta real?",
        "Levantamos o ciclo financeiro completo da empresa e comparamos as linhas disponíveis, sem custo e sem compromisso na primeira conversa.",
        secondary=("Ver Capital de Giro", "solucoes/capital-de-giro.html"), tone="petrol")

    return {
        "path": path, "nav_key": "solucoes.html", "over": True,
        "title": "Calculadora de capital de giro | Acrópole Capital",
        "desc": ("Calcule o ciclo financeiro e uma estimativa da necessidade de capital de giro da "
                 "sua empresa a partir dos prazos de estoque, recebimento e pagamento."),
        "body": body,
        "schema": [B.breadcrumb_schema(trail)],
    }


def pages():
    return [hub()] + [solution_page(s["slug"]) for s in SOLUTIONS] + [calculadora_giro()]
