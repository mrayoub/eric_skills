/* Etapas do playbook e fontes de dados das aplicações oficiais no Layout Studio. */
(function (root) {
  const methods = {"four_d": {"label": "4D", "stages": [{"id": "d1", "label": "D1 Descongelar", "meaning": "Alinhar o contexto e explicitar percepções, tensões e expectativas."}, {"id": "d2", "label": "D2 Diagnosticar", "meaning": "Aprofundar a jornada e as causas, obstáculos e condições do desafio."}, {"id": "d3", "label": "D3 Desenhar", "meaning": "Gerar alternativas e consolidar propostas ligadas ao diagnóstico."}, {"id": "d4", "label": "D4 Decidir", "meaning": "Priorizar alternativas com regra explícita e registrar razões e encaminhamentos."}]}, "three_e": {"label": "3E", "stages": [{"id": "e1", "label": "E1 Esclarecer", "meaning": "Refinar a hipótese de solução, valor, escopo e critérios."}, {"id": "e2", "label": "E2 Estruturar", "meaning": "Definir componentes, construção, dependências, responsáveis e prazos."}, {"id": "e3", "label": "E3 Experimentar", "meaning": "Planejar testes com hipótese, teste, medida e critério, sem antecipar resultados."}]}, "five_c": {"label": "5C", "stages": [{"id": "c1", "label": "C1 Contextualizar", "meaning": "Apresentar o desafio, suas fontes, objetivo e combinados."}, {"id": "c2", "label": "C2 Compreender", "meaning": "Escutar experiências, dificuldades e oportunidades com episódios concretos."}, {"id": "c3", "label": "C3 Confirmar", "meaning": "Converter dores priorizadas em experiência desejada e critérios observáveis."}, {"id": "c4", "label": "C4 Cocriar", "meaning": "Gerar e desenvolver propostas em conjunto, ligadas às dores identificadas."}, {"id": "c5", "label": "C5 Conduzir", "meaning": "Apresentar propostas, priorizar com regra acordada e definir encaminhamentos."}]}};
  const types = Object.keys(methods).flatMap(m => [m + '_official_report', m + '_official_presentation']);
  function stages(type) {
    const method = methods[type.split('_official_')[0]];
    return method ? method.stages.map(s => ({...s, official_stage_ids: [s.id]})) : [];
  }
  function parseStages(text) {
    const value = JSON.parse(text);
    if (!Array.isArray(value) || !value.length) throw new Error('Informe ao menos uma etapa aplicada.');
    const ids = new Set();
    for (const stage of value) {
      if (!stage || typeof stage !== 'object' || !/^[A-Za-z][A-Za-z0-9_]*$/.test(stage.id || '') || ids.has(stage.id))
        throw new Error('Cada etapa precisa de ID único, com letras, números ou sublinhado.');
      if (typeof stage.label !== 'string' || !stage.label.trim() || typeof stage.meaning !== 'string' || !stage.meaning.trim())
        throw new Error('Cada etapa precisa de nome e significado.');
      if (!Array.isArray(stage.official_stage_ids) || stage.official_stage_ids.some(id => typeof id !== 'string'))
        throw new Error('Declare official_stage_ids, mesmo quando a correspondência for vazia.');
      ids.add(stage.id);
    }
    return value;
  }
  function sections(type, applied) {
    if (!types.includes(type)) return [];
    const ids = (applied == null ? stages(type) : applied).map(s => s.id);
    return type.endsWith('report')
      ? ['purpose','introduction','structuring',...ids.flatMap(id => [id+'_description',id+'_execution',id+'_outcome']),'conclusion','recommendations']
      : ['challenge_context','structuring',...ids.map(id => 'execution_'+id),'conclusion','recommendations','decision','call_to_action'];
  }
  const api = {types, stages, parseStages, sections};
  root.OfficialMethods = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
