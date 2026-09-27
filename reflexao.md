## Reflexão

1. Por que o assistente precisa citar a FONTE e o que aconteceria em uma empresa real se ele respondesse sem citar?

Porque em uma resposta extrativa sem fonte a pessoa não sabe se aquilo ainda é válido e nem onde ele pode conferir o original. Por exemplo, a POL-004 revogada armazenada junto com a POL-005 vigente o usuário não saberia qual das duas o assistente de perguntas tirou a informação.

Em uma empresa real, um colaborador que segue uma informação errada por causa de um erro assim pode gerar problema trabalhista ou financeiro. E sem a citação, ninguém pode confirmar ou auditar de onde veio o erro e nem corrigir na origem.


2. Qual foi a decisão mais difícil entre chunking, pré-processamento e threshold, e como você a tomou?

A mais difícil foi o threshold,  porque o intervalo era de 0.266 de uma pergunta sem resposta até 0.308 de uma resposta fraca mas válida, só com 0.042 de margem. Escolhi 0.28, pois fica bem no meio do intervalo, como margem de segurança para os dois lados. Se eu escolhesse um threshold mais alto arriscaria classificar a P04 como "não encontrado" indevidamente e se fosse mais baixo arrisca um dia responder estacionamento com um trecho de politica errada 

3. Se você tivesse acesso a um LLM, o que mudaria na Parte 4 e que novo risco apareceria?

Mudaria que não teria que desenvolver o chunk "cru", o LLM rescreveria ou resumiria a resposta das perguntas com base nos chunks recuperados. O novo risco seria a clássica alucinação, o modelo pode enfeitar  e afirmar algo que literalmente não está no chunk como por exemplo, inventar número de dias que não bate com o texto original, o que é pior numa politica interna do que devolver o trecho bruto, porque perde a garantia de que a resposta é totalmente rastreável ao documento fonte.