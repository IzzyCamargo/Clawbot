#!/usr/bin/env python3
"""
Script para adicionar o agente_vendas_consultivo ao workflow Orquestrador.json
"""

import json
import uuid
import copy

# Ler o arquivo original
with open('/home/ti/Downloads/Orquestrador.json', 'r') as f:
    workflow = json.load(f)

# ID único para o novo agente e seu LLM
agente_id = str(uuid.uuid4())
gemin_id = str(uuid.uuid4())

# Posição para o novo agente (ao lado dos outros agentes de venda)
# agente_venda_seguros está em [-3040, -2496], agente_venda_rastreador em [-2752, -2496]
# Colocar o novo em [-2464, -2496] (continuando a linha)
posicao_agente = [-2464, -2496]
posicao_gemin = [-2464, -2336]  # LLM fica abaixo do agente (mesma coluna, linha +160)

# === CRIAR O NOVO AGENTE ===
agente_vendas_consultivo = {
    "parameters": {
        "toolDescription": "Chame esse agente quando o cliente demonstrar interesse em comprar, cotações, preços, planos, ou conversas comerciais gerais. Use também para qualificar leads e entender necessidades antes de vender.",
        "text": "={{ $('Edit Fields1').item.json['Mensagem de texto'] }}",
        "options": {
            "systemMessage": "🎯 AGENTE: VENDAS CONSULTIVO GERAL (VENDAS-EXPERT SKILL)\n\nDomínio: vendas de planos, produtos e serviços da Sempre Comigo\nTom: consultivo, humano, sem pressão, focado em soluções\n\n🎯 PROPÓSITO\n- Qualificar leads e entender necessidades\n- Conduzir pelo funil de vendas de forma natural\n- Fechar vendas usando técnicas suaves\n- Propor próximos passos (demo, proposta, pagamento)\n\n📋 REGRAS DE OURO\n\n✔️ Uma pergunta por vez - nunca bombardeie o cliente\n✔️ Entenda antes de propor - nunca venda no primeiro contato\n✔️ Foco em SOLUÇÕES, não em produtos\n✔️ Use técnicas de fechamento suaves (option close, summary close, future pacing)\n✔️ Sempre termine definindo o próximo passo\n\n🔍 FLUXO DE QUALIFICAÇÃO (se necessidade não estiver clara)\n1. \"Qual é o principal desafio que você quer resolver?\"\n2. \"Você já utilizou algo parecido antes?\"\n3. \"O que te motivou a procurar uma solução agora?\"\n\n💰 FLUXO DE OBJEÇÃO DE PREÇO\n- \"Entendo, quando você considera isso um bom investimento?\"\n- \"Qual retorno você espera obter com essa solução?\"\n- \"Vamos comparar o custo do problema atual vs. o investimento na solução?\"\n\n✅ FLUXO DE FECHAMENTO (quando mostrar intenção de compra)\n- \"Pelo que entendi, isso atende sua necessidade. Posso enviar uma proposta?\"\n- \"Quer agendar uma demo para ver na prática?\"\n- \"Posso reservar sua vaga/enviar o link de pagamento agora?\"\n\n📚 FLUXO PARA LEAD NÃO QUALIFICADO\n- \"Posso te encaminhar material explicativo para você decidir?\"\n- \"Vou te adicionar à lista para te avisar quando tivermos novidades.\"\n\n❌ PROIBIÇÕES\n- Técnicas agressivas de vendas (ABC tradicional)\n- Listas de perguntas BANT de uma vez\n- Pedir dados (CPF, placa) antes de estabelecer interesse\n- Repetir \"quer comprar?\" sem contexto\n- Reapresentar produto já apresentado\n\n🏁 ENCERRAMENTO\n- Sempre confirme o próximo passo\n- Deixe o cliente com a sensação de progresso\n- Nunca termine sem ação definida"
        }
    },
    "type": "@n8n/n8n-nodes-langchain.agentTool",
    "typeVersion": 2.2,
    "position": posicao_agente,
    "id": agente_id,
    "name": "agente_vendas_consultivo"
}

# === CRIAR O LLM PARA O AGENTE ===
gemin17 = {
    "parameters": {
        "model": {
            "__rl": True,
            "value": "models/gemini-2.5-flash",
            "mode": "list",
            "cachedResultName": "models/gemini-2.5-flash"
        },
        "options": {}
    },
    "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
    "typeVersion": 1.2,
    "position": posicao_gemin,
    "id": gemin_id,
    "name": "gemin17",
    "credentials": {
        "openAiApi": {
            "id": "mMR2LMepDYOlxAjn",
            "name": "Gemini"
        }
    }
}

# Adicionar os novos nodes
workflow['nodes'].append(agente_vendas_consultivo)
workflow['nodes'].append(gemin17)

# === ATUALIZAR CONEXÕES ===

# 1. Connection do gemin17 para agente_vendas_consultivo (ai_languageModel)
workflow['connections']['gemin17'] = {
    "ai_languageModel": [
        [
            {
                "node": "agente_vendas_consultivo",
                "type": "ai_languageModel",
                "index": 0
            }
        ]
    ]
}

# 2. Connection do agente_vendas_consultivo para Orchestrador (ai_tool)
workflow['connections']['agente_vendas_consultivo'] = {
    "ai_tool": [
        [
            {
                "node": "Orchestrador",
                "type": "ai_tool",
                "index": 0
            }
        ]
    ]
}

# === ATUALIZAR O SYSTEM MESSAGE DO ORQUESTRADOR ===
# Encontrar o node Orchestrador
orchestrator_node = None
for node in workflow['nodes']:
    if node['name'] == 'Orchestrador':
        orchestrator_node = node
        break

if orchestrator_node:
    system_message = orchestrator_node['parameters']['options']['systemMessage']
    
    # Adicionar a nova rota no mapeamento
    # Inserir após "Atendimento Geral" e antes de "🚨 REGRA DE USO DE TOOLS"
    nova_rota = """\nVendas / Interesse Comercial\n(cotação, preço, planos, quero comprar, tenho interesse, venda, comprar rastreador, seguro, consultoria)\n→ agente_vendas_consultivo\n"""
    
    # Encontrar onde inserir (antes de "🚨 REGRA DE USO DE TOOLS")
    if "🚨 REGRA DE USO DE TOOLS" in system_message:
        parts = system_message.split("🚨 REGRA DE USO DE TOOLS")
        system_message = parts[0] + nova_rota + "\n🚨 REGRA DE USO DE TOOLS" + parts[1]
    else:
        # Se não encontrar o marcador, adiciona antes das regras críticas
        if "⚠️ REGRA ESPECÍFICA" in system_message:
            parts = system_message.split("⚠️ REGRA ESPECÍFICA")
            system_message = parts[0] + nova_rota + "\n⚠️ REGRA ESPECÍFICA" + parts[1]
        else:
            system_message += nova_rota
    
    orchestrator_node['parameters']['options']['systemMessage'] = system_message
    print("✅ SystemMessage do Orchestrador atualizado")

# Salvar o novo arquivo
output_path = '/home/ti/Documentos/projects/claudio/jsons/Orquestrador_com_Vendas_Consultivo.json'
with open(output_path, 'w') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"✅ Workflow atualizado salvo em: {output_path}")
print(f"✅ Novo agente: agente_vendas_consultivo (ID: {agente_id})")
print(f"✅ Novo LLM: gemin17 (ID: {gemin_id})")
print("\n📋 Resumo das alterações:")
print("- Adicionado node: agente_vendas_consultivo")
print("- Adicionado node: gemin17")
print("- Adicionadas connections para o novo agente")
print("- Atualizado systemMessage do Orchestrador com rota de vendas")
